from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import serializers

from recipes.models import Recipe


class ListRetrieveViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    """
    A viewset that provides default `list()` and `retrieve()` actions.
    """
    pass


class RecipeMixin(serializers.ModelSerializer):
    """
    A mixin for Recipe serializers to add custom fields related to user interactions.

    Attributes:
    - get_is_favorited(obj: Recipe) -> bool: Retrieve the boolean value of the 'is_favorite' field.
    - get_is_in_shopping_cart(obj: Recipe) -> bool: Retrieve the boolean value of the 'is_in_shopping_cart' field.
    """

    def get_is_favorited(self, obj: Recipe) -> bool:
        """
        Retrieve the boolean value of the 'is_favorite' field.

        Args:
        - obj (Recipe): The Recipe instance.

        Returns:
        bool: True if the recipe is favorited by the user, False otherwise.
        """
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(
            favorite__username=user.username, id=obj.id
        ).exists()

    def get_is_in_shopping_cart(self, obj: Recipe) -> bool:
        """
        Retrieve the boolean value of the 'is_in_shopping_cart' field.

        Args:
        - obj (Recipe): The Recipe instance.

        Returns:
        bool: True if the recipe is in the user's shopping cart, False otherwise.
        """
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(
            in_cart__username=user.username, id=obj.id
        ).exists()
