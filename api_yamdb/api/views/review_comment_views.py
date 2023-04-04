from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from api.permissions import IsAuthorModeratorAdminOrReadOnly
from api.serializers import CommentSerializer, ReviewSerializer
from reviews.models import Review, Title


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
