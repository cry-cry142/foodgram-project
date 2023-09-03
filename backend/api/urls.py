from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import UserViewSet

app_name = 'api'

router = SimpleRouter()

router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls))
]
