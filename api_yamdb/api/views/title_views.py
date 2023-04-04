from rest_framework import viewsets
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend

from api.serializers import TitleListRetrieveSerializer, TitleCreateSerializer
from api.permissions import IsAdminOrReadOnly
from reviews.models import Title
from api.filters import TitleFilter


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""
    serializer_class = TitleListRetrieveSerializer
    queryset = (Title.objects.select_related('category')
                .prefetch_related('genre')
                .annotate(rating=Avg('reviews__score'))
                )
    http_method_names = ["get", "post", "delete", "patch"]
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleListRetrieveSerializer
        return TitleCreateSerializer
