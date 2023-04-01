from django.core.validators import MinValueValidator, MaxValueValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Comment, Review, Title


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отзывов.
    Оценка может быть в пределах от 1 до 10.
    Пользователь может оставить только один отзыв на произведение.
    """
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    score = serializers.IntegerField(
        validators=[
            MinValueValidator(
                1, 'Минимальная оценка должна быть не меньше 1'),
            MaxValueValidator(
                10, 'Максимальная оценка должна быть не больше 10')
        ],
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')
        model = Review

    def validate(self, data):
        """
        Проверка на наличие в БД отзыва пользователя.
        Пользователь может оставить только один отзыв на произведение.
        """
        request = self.context['request']
        if request.method == 'POST':
            author = request.user
            view = self.context['view']
            title_id = view.kwargs.get('title_id')
            title = get_object_or_404(Title, id=title_id)
            if Review.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError(
                    'Можно оставить только один отзыв на произведение.'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для комментариев.
    """
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')
        model = Comment
