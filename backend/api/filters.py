from django_filters import rest_framework as filters
from django.db.models import Q

from recipes.models import Ingredient


def partial_search_filter(queryset, name, value):
    filter_field = f'{name}__startswith'
    value = value.lower()
    return queryset.filter(Q(**{filter_field: value}))


class PartialNameFilter(filters.FilterSet):
    name = filters.CharFilter(
        method=partial_search_filter,
        field_name='name'
    )

    class Meta:
        model = Ingredient
        fields = (
            'name',
        )
