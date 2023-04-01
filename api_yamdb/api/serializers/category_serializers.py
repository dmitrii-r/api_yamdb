from rest_framework import serializers

from reviews.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий произведений."""
    lookup_field = 'slug'

    class Meta:
        model = Category
        fields = ('name', 'slug')
