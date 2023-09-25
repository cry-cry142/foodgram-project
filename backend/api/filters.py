from django.db.models import Q
from django_filters import rest_framework as filters

from recipes.models import Ingredient, Recipe, Tag


class PartialNameFilter(filters.FilterSet):
    name = filters.CharFilter(
        method='partial_search_filter',
        field_name='name'
    )

    class Meta:
        model = Ingredient
        fields = (
            'name',
        )

    def partial_search_filter(self, queryset, name, value):
        filter_field = f'{name}__startswith'
        value = value.lower()
        return queryset.filter(Q(**{filter_field: value}))


class RecipeFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favorited = filters.BooleanFilter(
        method='favorited_method'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='shopping_cart_method'
    )

    class Meta:
        model = Recipe
        fields = (
            'author', 'tags'
        )

    def favorited_method(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated and value:
            return queryset.filter(favourite__user=user)
        return queryset

    def shopping_cart_method(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated and value:
            return queryset.filter(carts__user=user)
        return queryset
