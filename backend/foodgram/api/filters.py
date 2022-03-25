from typing import Any

from django.db.models import QuerySet
from django_filters import rest_framework as filters

from recipes.models import Recipe, Tag


class RecipeFilterSet(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tag.objects.all(),
    )
    is_favorited = filters.BooleanFilter(method="filter_is_favorited")
    is_in_shopping_cart = filters.BooleanFilter(method="filter_is_in_shopping_cart")

    class Meta:
        model = Recipe
        fields = ["author", "tags", "is_favorited", "is_in_shopping_cart"]

    def filter_is_favorited(self, queryset: QuerySet, name: Any, value: Any) -> QuerySet:
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(favorite__username=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset: QuerySet, name: Any, value: Any):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(in_cart__username=user)
        return queryset
