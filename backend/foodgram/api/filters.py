from django_filters import rest_framework as filters

from recipes.models import Recipe, Tag


class RecipeFilterSet(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    is_favorited = filters.BooleanFilter(method='filter_by_user')
    is_in_shopping_cart = filters.BooleanFilter(method='filter_by_user')

    def filter_by_user(self, queryset, name, value):
        return queryset.filter(**{name: self.request.user})

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart']
