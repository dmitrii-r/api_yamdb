from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Avg

from api.serializers import TitleListRetrieveSerializer, TitleCreateSerializer
from api.permissions import IsAdminOrReadOnly
from reviews.models import Title


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleListRetrieveSerializer
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    http_method_names = ["get", "post", "delete", "patch"]
    permission_classes = (IsAdminOrReadOnly,)
    # добавить фильтры
    
    # def get_permissions(self):
    #     """
    #     Instantiates and returns the list of permissions that this view requires.
    #     """
    #     return (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleListRetrieveSerializer
        return TitleCreateSerializer
