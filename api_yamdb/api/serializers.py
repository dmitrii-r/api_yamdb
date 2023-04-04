from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Genre, Title, Comment, Review

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для пользователя с правами администратора.
    """

    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User


class NoAdminUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для пользователя без прав администратора.
    """

    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User
        read_only_fields = ('role',)


class RegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации пользователей.
    """

    class Meta:
        fields = ("username", "email")
        model = User


class TokenSerializer(serializers.Serializer):
    """
    Сериализатор для проверки токена.
    """
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class EmailSerializer(serializers.Serializer):
    """
    Сериализатор для проверки пользователя,
    зарегистрированного администратором.
    """
    username = serializers.CharField()
    email = serializers.EmailField()


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий произведений."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров произведений."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleListRetrieveSerializer(serializers.ModelSerializer):
    """
    Сериализатор для GET-запроса произведений.
    Категория и жанр в виде встроенного сериализатора с name и slug.
    Рейтинг рассчитывается среднее арифметическое всех оценок произведения.
    """
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(default=1)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')
        read_only_fields = ('id', 'name', 'year', 'rating', 'description',
                            'genre', 'category')


class TitleCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для POST, PATCH-, DELETE-запроса произведений.
    Год выхода не может быть больше дальше текущего года.
    Категорию и жанр надо указывать как slug из тех, что уже есть в базе.
    """
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    def validate_year(self, value):
        if value > datetime.now().year:
            raise serializers.ValidationError(
                'Нельзя добавлять произведения, которые еще не вышли '
                '(год выпуска не может быть больше текущего).'
            )
        return value

    def to_representation(self, instance):
        return TitleListRetrieveSerializer(instance).data


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
