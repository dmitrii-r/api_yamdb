from datetime import datetime
from rest_framework import serializers
from api.serializers import CategorySerializer, GenreSerializer

from reviews.models import Title


class TitleSerializer(serializers.ModelSerializer):
    """"
    Сериализатор для произведений.
    Год выхода не может быть больше дальше текущего года.
    Категория и жанр в виде встроенного сериализатора с name и slug.
    Рейтинг рассчитывается среднее арифметическое всех оценок произведения.
    """
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=1, read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')

    def validate_year(self, value):
        if value > datetime.now().year:
            raise serializers.ValidationError(
                'Нельзя добавлять произведения, которые еще не вышли '
                '(год выпуска не может быть больше текущего).'
            )
        return value
