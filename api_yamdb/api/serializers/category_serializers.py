from rest_framework import serializers

from reviews.models import Category


class CategorySerializer(serializers.Serializer):
    """Сериализатор для категорий произведений."""

    class Meta:
        model = Category
        fields = ('name', 'slug')
