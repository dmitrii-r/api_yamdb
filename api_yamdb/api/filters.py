import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='contains')
    category = django_filters.CharFilter(field_name='category__slug',
                                         lookup_expr='iexact')
    genre = django_filters.CharFilter(field_name='genre__slug',
                                      lookup_expr='iexact')
    year = django_filters.NumberFilter(field_name='year',
                                       lookup_expr='iexact')

    class Meta:
        model = Title
        fields = ['name', 'category', 'genre', 'year']
