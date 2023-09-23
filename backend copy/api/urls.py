from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    UserViewSet, TagViewSet, IngredientViewSet, RecipeViewSet,
    favorite
)

app_name = 'api'

router = SimpleRouter()

router.register('users', UserViewSet, basename='user')
router.register('tags', TagViewSet, basename='tag')
router.register('ingredients', IngredientViewSet, basename='ingredient')
router.register('recipes', RecipeViewSet, basename='recipe')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('recipes/<int:pk>/favorite/', favorite, name='favorite'),
    path('', include(router.urls))
]
