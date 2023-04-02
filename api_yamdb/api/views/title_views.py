from rest_framework import viewsets
from django.db.models import Avg

from api.serializers import TitleSerializer
from api.permissions import IsAdminOrReadOnly
from reviews.models import Title


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly,)
    # добавить фильтры
