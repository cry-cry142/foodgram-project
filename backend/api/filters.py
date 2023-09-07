import operator
from functools import reduce
from django_filters import rest_framework as filters
from django.db.models import Q

from recipes.models import Ingredient


def filter_name(queryset, name, value):
    lookups = [name + '__startswith', ]

    or_queries = []

    search_terms = value.split()

    for search_term in search_terms:
        or_queries += [Q(**{lookup: search_term}) for lookup in lookups]

    return queryset.filter(reduce(operator.or_, or_queries))


class ParticalNameFilter(filters.FilterSet):
    name = filters.CharFilter(method=filter_name, field_name='name')

    class Meta:
        model = Ingredient
        fields = (
            'name',
        )
