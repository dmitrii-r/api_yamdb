from rest_framework import viewsets, mixins

from api.permissions import IsAdmin
from api.serializers import CategorySerializer
from reviews.models import Category


class CreateRetrieveDestroyListViewSet(mixins.CreateModelMixin,
                                       mixins.RetrieveModelMixin,
                                       mixins.DestroyModelMixin,
                                       mixins.ListModelMixin,
                                       viewsets.GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `destroy()` and
    `list()` actions.
    """
    pass


class CategoryViewSet(CreateRetrieveDestroyListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = (IsAdmin,)
    # lookup_field = 'slug'
