from django.conf import settings
from rest_framework import serializers


def validate_username(value):
    """
    Проверка соответсвия введённого имени,
    Username не может быть 'me'.
    """
    if value.lower() == settings.PROFILE_URL:
        raise serializers.ValidationError(
            f'Username не может быть {settings.PROFILE_URL}'
        )
    return value
