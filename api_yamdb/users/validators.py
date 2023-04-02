from rest_framework import serializers


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
