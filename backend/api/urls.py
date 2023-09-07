from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import UserViewSet, TagViewSet, IngredientViewSet

app_name = 'api'

router = SimpleRouter()

router.register('users', UserViewSet, basename='user')
router.register('tags', TagViewSet, basename='tag')
router.register('ingredients', IngredientViewSet, basename='ingredient')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls))
]
