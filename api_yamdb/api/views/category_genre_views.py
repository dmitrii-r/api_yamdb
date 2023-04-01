from rest_framework import filters

from api.mixins import CreateDestroyListViewSet
from api.serializers import CategorySerializer
from api.permissions import IsAdminOrReadOnly
from reviews.models import Category


class CategoryViewSet(CreateDestroyListViewSet):
    """
    Вьюсет для категорий произведений.
    Получение списка категорий доступно без аутентификации.
    Создание и удаление новых категорий доступно только администраторам при
    указании slug.
    Остальные действия запрещены.
    Поиск по названию категории.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
