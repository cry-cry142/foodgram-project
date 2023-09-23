from django.contrib.auth.hashers import make_password, check_password
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response


from recipes.models import (
    User, Tag, Ingredient, Recipe
)
from .serializers import (
    UserSerializer, AnonimusUserSerializer, ChangePasswordSerializer,
    TagSerializer, IngredientSerializer, RecipeSerializer,
    FavouriteRecipesSerializer, SubscriptionsSerializer
)
from .pagination import PageNumberLimitPagination
from .permissions import IsResponsibleUserOrReadOnly
from .filters import PartialNameFilter, RecipeFilter
from .decorators import not_allowed_put_method


class UserViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = PageNumberLimitPagination

    def perform_create(self, serializer):
        password = make_password(
            serializer.validated_data['password']
        )
        serializer.save(
            password=password
        )

    def get_permissions(self):
        if self.detail:
            self.permission_classes = (permissions.IsAuthenticated,)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return AnonimusUserSerializer
        return self.serializer_class

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        followers = self.queryset.filter(subscriptions__user=request.user)
        serializer = UserSerializer(
            request.user,
            context={
                'request': request,
                'followers': followers,
            }
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['POST'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def set_password(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data
        )
        user = request.user
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        if not check_password(
            serializer.validated_data['current_password'],
            user.password
        ):
            return Response(
                {'current_password': 'Пароль не верен.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.password = make_password(
            serializer.validated_data['new_password']
        )
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
            detail=False,
            methods=['GET'],
            permission_classes=(permissions.IsAuthenticated,),
            pagination_class=PageNumberLimitPagination,
    )
    def subscriptions(self, request):
        q = self.queryset.filter(subscribers__follower=request.user)

        page = self.paginate_queryset(q)
        context = {
            'request': request,
        }
        if page is not None:
            serializer = SubscriptionsSerializer(
                page,
                many=True,
                context=context
            )
            return self.get_paginated_response(serializer.data)

        serializer = SubscriptionsSerializer(
            q,
            many=True,
            context=context
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
            detail=True,
            methods=['POST', 'DELETE'],
            permission_classes=(permissions.IsAuthenticated,)
    )
    def subscribe(self, request, pk):
        pk = int(pk)
        user = get_object_or_404(self.queryset, pk=pk)
        if request.method == 'POST':
            if user.subscribers.filter(follower=request.user).exists():
                return Response(
                    {'errors': 'Пользователь уже подписан.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if user == request.user:
                return Response(
                    {'errors': 'Пользователь не может подписаться на себя.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = SubscriptionsSerializer(
                user,
                context={'request': request}
            )
            user.subscribers.create(
                follower=request.user
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            if not user.subscribers.filter(follower=request.user).exists():
                return Response(
                    {'errors': 'Пользователь не подписан.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.subscribers.filter(
                follower=request.user
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TagViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PartialNameFilter


@not_allowed_put_method
class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageNumberLimitPagination
    permission_classes = (IsResponsibleUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
        )

    def destroy(self, request, *args, **kwargs):
        recipe = get_object_or_404(self.queryset, id=kwargs.get('pk'))
        recipe.tags.clear()
        recipe.ingredients.clear()
        return super().destroy(request, *args, **kwargs)

    @action(
            detail=True,
            methods=['POST', 'DELETE'],
            permission_classes=(permissions.IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        pk = int(pk)
        recipe = get_object_or_404(self.queryset, pk=pk)
        if request.method == 'POST':
            if recipe.carts.filter(user=request.user).exists():
                return Response(
                    {'errors': 'Рецепт уже в корзине.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = FavouriteRecipesSerializer(
                recipe,
                context={'request': request}
            )
            recipe.carts.create(
                user=request.user
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            if not recipe.carts.filter(user=request.user).exists():
                return Response(
                    {'errors': 'Рецепта нет в корзине.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            recipe.carts.filter(
                user=request.user
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(
            detail=False,
            methods=['GET'],
            permission_classes=(permissions.IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        recipes = self.queryset.filter(carts__user=request.user)
        cart = dict()
        for recipe in recipes:
            ingredient_list = recipe.ingredients.all()
            for ingredient in ingredient_list:
                count = int(
                    recipe.m2m.get(
                        ingredient=ingredient
                    ).amount
                )

                if not cart.get(ingredient.id):
                    cart[ingredient.id] = {
                        'name': ingredient.name,
                        'measurement_unit': ingredient.measurement_unit,
                        'count': count
                    }
                else:
                    cart[ingredient.id]['count'] += count
        data = ''
        for key, value in cart.items():
            data += (f'[{key}] {value["name"]} - {value["count"]} '
                     f'{value["measurement_unit"]}\n')

        return Response(
            data=data,
            content_type='text/plain',
            headers={
                'Content-Disposition': 'attachment; filename=List_Buy.txt'
            },
            status=status.HTTP_200_OK
        )


@api_view(['POST', 'DELETE'])
@permission_classes((permissions.IsAuthenticated,))
def favorite(request, **kwargs):
    recipe = get_object_or_404(Recipe, id=kwargs['pk'])
    favorite_manager = recipe.favourite
    if request.method == 'POST':
        if favorite_manager.filter(user=request.user).exists():
            return Response(
                {'errors': 'Вы уже подписаны.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        favorite_manager.create(
            user=request.user,
            recipe=recipe
        )

        serializer = FavouriteRecipesSerializer(
            instance=recipe,
            context={
                'request': request
            }
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    if request.method == 'DELETE':
        if not favorite_manager.filter(user=request.user).exists():
            return Response(
                {'errors': 'Вы не подписаны на рецепт.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        favorite = favorite_manager.get(user=request.user)
        favorite.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
