from rest_framework import serializers
from recipes.models import Recipe


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe.
    Определён укороченный набор полей для некоторых эндпоинтов.
    """
    class Meta:
        model = Recipe
        fields = 'id', 'name', 'image', 'cooking_time'
        read_only_fields = '__all__',
