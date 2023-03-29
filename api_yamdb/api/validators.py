import re
from rest_framework import serializers


def validate_username(value):
    if value.lower() == "me":
        raise serializers.ValidationError("Username 'me' is not valid")
    if re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', value) is None:
        raise serializers.ValidationError("Недопустимые символы")
    return value
