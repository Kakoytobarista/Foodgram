from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import serializers

from recipes.models import Recipe


class ListRetrieveViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    pass


class RecipeMixin(serializers.ModelSerializer):

    def get_is_favorited(self, obj: Recipe) -> bool:
        """Достаем булово значение поля is_favorite"""
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(
            favorite__username=user.username, id=obj.id
        ).exists()

    def get_is_in_shopping_cart(self, obj) -> bool:
        """Достаем булово значение поля is_in_shopping_cart"""
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(
            in_cart__username=user.username, id=obj.id
        ).exists()
