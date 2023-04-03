from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Avg

from api.serializers import TitleSerializer
from api.permissions import IsAdminOrReadOnly
from reviews.models import Title


class TitleViewSet(viewsets.ViewSet):
    # serializer_class = TitleSerializer
    # queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly,)
    # добавить фильтры

        
    # - list(self, request)
    # - create(self, request)
    # - retrieve(self, request, pk=None)
    # - update(self, request, pk=None)
    # - partial_update(self, request, pk=None)
    # - destroy(self, request, pk=None)

    def list(self, request):
        queryset = Title.objects.annotate(rating=Avg('reviews__score'))
        serializer = TitleSerializer(queryset, many=True)
        return Response(serializer.data)
    
    # def get_permissions(self):
    #     """
    #     Instantiates and returns the list of permissions that this view requires.
    #     """
    #     return (IsAdminOrReadOnly,)
