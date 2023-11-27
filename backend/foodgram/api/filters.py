from typing import Any

from django.db.models import QuerySet
from django_filters import rest_framework as filters

from recipes.models import Recipe, Tag


class RecipeFilterSet(filters.FilterSet):
    """
    FilterSet for Recipe model to enable filtering based on various criteria.
    """

    tags = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tag.objects.all(),
        help_text="Filter recipes by tags.",
    )
    is_favorited = filters.BooleanFilter(method="filter_is_favorited", help_text="Filter favorited recipes.")
    is_in_shopping_cart = filters.BooleanFilter(
        method="filter_is_in_shopping_cart", help_text="Filter recipes in the shopping cart."
    )

    class Meta:
        model = Recipe
        fields = ["author", "tags", "is_favorited", "is_in_shopping_cart"]

    def filter_is_favorited(self, queryset: QuerySet, name: Any, value: Any) -> QuerySet:
        """
        Custom filter method to filter recipes that are favorited by the user.

        Parameters:
        - queryset (QuerySet): The initial queryset.
        - name (Any): The name of the filter field.
        - value (Any): The filter value.

        Returns:
        QuerySet: The filtered queryset.
        """
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(favorite__username=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset: QuerySet, name: Any, value: Any) -> QuerySet:
        """
        Custom filter method to filter recipes that are in the user's shopping cart.

        Parameters:
        - queryset (QuerySet): The initial queryset.
        - name (Any): The name of the filter field.
        - value (Any): The filter value.

        Returns:
        QuerySet: The filtered queryset.
        """
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(in_cart__username=user)
        return queryset
