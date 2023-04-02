from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers


username_validator = UnicodeUsernameValidator()


def validate_username(value):
    """
    Проверка соответсвия введённого имени,
    Username не может быть 'me'.
    """
    if value.lower() == 'me':
        raise serializers.ValidationError(
            'Username не может быть me'
        )
    return value
