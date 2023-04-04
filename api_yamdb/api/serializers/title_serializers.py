from datetime import datetime
from rest_framework import serializers
from api.serializers import CategorySerializer, GenreSerializer

from reviews.models import Title, Category, Genre


class TitleListRetrieveSerializer(serializers.ModelSerializer):
    """"
    Сериализатор для GET-запроса произведений.
    Категория и жанр в виде встроенного сериализатора с name и slug.
    Рейтинг рассчитывается среднее арифметическое всех оценок произведения.
    """
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(default=1)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')
        read_only_fields = ('id', 'name', 'year', 'rating', 'description',
                            'genre', 'category')


class TitleCreateSerializer(serializers.ModelSerializer):
    """"
    Сериализатор для POST, PATCH-, DELETE-запроса произведений.
    Год выхода не может быть больше дальше текущего года.
    Категорию и жанр надо указывать как slug из тех, что уже есть в базе.
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

    def to_representation(self, instance):
        return TitleListRetrieveSerializer(instance).data
