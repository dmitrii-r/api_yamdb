import re
from rest_framework import serializers


def validate_username(value):
    """
    Проверка соответсвия введённого имени.
    """
    if value.lower() == "me":
        raise serializers.ValidationError("Username 'me' is not valid")
    if re.search(r'^[\w.@+-]+\Z$', value) is None:
        raise serializers.ValidationError("Недопустимые символы")
    return value
