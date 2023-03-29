from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .validators import validate_username

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для пользователя с правами администратора.
    """
    username = serializers.CharField(
        max_length=150,
        validators=[validate_username,
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
        validators=[validate_username])

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
