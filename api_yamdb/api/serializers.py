from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Review, Title
from .validators import validate_username

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для пользователя с правами администратора.
    """
    username = serializers.CharField(
        max_length=150,
        validators=[validate_username,
                    UnicodeUsernameValidator(),
                    UniqueValidator(queryset=User.objects.all())
                    ], required=True,
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User


class NoAdminUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для пользователя без прав администратора.
    """
    username = serializers.CharField(
        max_length=150,
        validators=[
            validate_username,
            UnicodeUsernameValidator()
        ])

    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User
        read_only_fields = ('role',)


class RegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации пользователей.
    """
    username = serializers.CharField(
        max_length=150,
        validators=[validate_username,
                    UnicodeUsernameValidator(),
                    UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

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


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отзывов.
    Оценка может быть в пределах от 1 до 10.
    Пользователь может оставить только один отзыв на произведение.
    """
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
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
        request = self.context['request']
        if request.method == 'POST':
            author = request.user
            view = self.context['view']
            title_id = view.kwargs.get('title_id')
            title = get_object_or_404(Title, id=title_id)
            if Review.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError(
                    'Можно оставить только один отзыв на произведение')
            return data
