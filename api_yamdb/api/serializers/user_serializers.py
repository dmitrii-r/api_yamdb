from django.contrib.auth import get_user_model
from rest_framework import serializers

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
