from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Title
from .serializers import (RegisterSerializer,
                          EmailSerializer,
                          TokenSerializer,
                          NoAdminUserSerializer,
                          UserSerializer, ReviewSerializer)
from .permissions import IsAdmin, IsAuthorModeratorAdminOrReadOnly

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
        url_path='me',
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
