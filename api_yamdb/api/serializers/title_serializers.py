from datetime import datetime
from rest_framework import serializers
from api.serializers import CategorySerializer, GenreSerializer

from reviews.models import Title, Category, Genre


class TitleListRetrieveSerializer(serializers.ModelSerializer):
    """"
    Сериализатор для произведений.
    Год выхода не может быть больше дальше текущего года.
    Категория и жанр в виде встроенного сериализатора с name и slug.
    Рейтинг рассчитывается среднее арифметическое всех оценок произведения.
    """
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=1,
                                      read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')


class TitleCreateSerializer(serializers.ModelSerializer):
    """"
    Сериализатор для произведений.
    Год выхода не может быть больше дальше текущего года.
    Категория и жанр в виде встроенного сериализатора с name и slug.
    Рейтинг рассчитывается среднее арифметическое всех оценок произведения.
    """
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    def validate_year(self, value):
        if value > datetime.now().year:
            raise serializers.ValidationError(
                'Нельзя добавлять произведения, которые еще не вышли '
                '(год выпуска не может быть больше текущего).'
            )
        return value
