from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ReviewViewSet, UserViewSet, get_jwt_token, register


app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(r"users", UserViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', register, name='register'),
    path('v1/auth/token/', get_jwt_token, name='token')
]
