from rest_framework import serializers


def validate_username(value):
    """
    Проверка соответсвия введённого имени.
    """
    if value.lower() == "me":
        raise serializers.ValidationError("Username 'me' is not valid")
    return value
