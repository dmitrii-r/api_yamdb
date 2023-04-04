from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.filters import TitleFilter
from api.mixins import CreateDestroyListViewSet
from api.permissions import (IsAdmin, IsAdminOrReadOnly,
                             IsAuthorModeratorAdminOrReadOnly)
from api.serializers import (RegisterSerializer, EmailSerializer,
                             TokenSerializer, NoAdminUserSerializer,
                             UserSerializer, CategorySerializer,
                             GenreSerializer, TitleListRetrieveSerializer,
                             TitleCreateSerializer, ReviewSerializer,
                             CommentSerializer)
from reviews.models import Category, Genre, Title, Review

User = get_user_model()


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    """
    Отправка кода верификации на email.
    """
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    if not User.objects.filter(username=username, email=email).exists():
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject=f'Registration code for {username}',
        message=f'Ваш код подтверждения для доступа: {confirmation_code}',
        from_email=None,
        recipient_list=[email],
    )

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_jwt_token(request):
    """
    Получение токена для авторизации.
    """
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )

    if default_token_generator.check_token(
        user, serializer.validated_data['confirmation_code']
    ):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    Создание и редактирование пользователя.
    """
    lookup_field = 'username'
    queryset = User.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=[
            'get',
            'patch',
        ],
        detail=False,
        url_path=settings.PROFILE_URL,
        permission_classes=(permissions.IsAuthenticated,),
    )
    def get_current_user_info(self, request):
        """
        В зависимости от роли используем нужный сериализатор,
        и изменяем данные пользователя.
        """
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UserSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:
                serializer = NoAdminUserSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class CategoryViewSet(CreateDestroyListViewSet):
    """
    Вьюсет для категорий произведений.
    Получение списка категорий доступно без аутентификации.
    Создание и удаление новых категорий доступно только администраторам при
    указании slug.
    Остальные действия запрещены.
    Поиск по названию категории.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CreateDestroyListViewSet):
    """
    Вьюсет для жанров произведений.
    Получение списка жанров доступно без аутентификации.
    Создание и удаление новых жанров доступно только администраторам при
    указании slug.
    Остальные действия запрещены.
    Поиск по названию жанра.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""
    serializer_class = TitleListRetrieveSerializer
    queryset = (Title.objects.select_related('category')
                .prefetch_related('genre')
                .annotate(rating=Avg('reviews__score'))
                )
    http_method_names = ["get", "post", "delete", "patch"]
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleListRetrieveSerializer
        return TitleCreateSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для отзывов.
    Любой пользователь может просматривать список всех отзывов
    или выбранный отзыв.
    Авторизованный пользователь может создавать свои отзывы.
    Автор отзыва может редактировать и удалять свои отзывы.
    Модератор или администратор могут редактировать и удалять любые отзывы.
    """
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для комментариев.
    Любой пользователь может просматривать список всех комментариев к отзыву
    или комментарий для выбранного отзыва по id.
    Авторизованный пользователь может создавать свои комментарии.
    Автор комментария может редактировать и удалять свои комментарии.
    Модератор или администратор могут редактировать и удалять любые
    комментарии.
    """
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def get_review(self):
        return get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
