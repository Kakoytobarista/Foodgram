from djoser.serializers import UserSerializer
from rest_framework import serializers

from drf_extra_fields.fields import Base64ImageField

from recipes.models import Recipe, Tag, Ingredient, IngredientRecipe


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe.
    Определён укороченный набор полей для некоторых эндпоинтов.
    """

    class Meta:
        model = Recipe
        fields = 'id', 'name', 'image', 'cooking_time'
        read_only_fields = '__all__',


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Tag"""

    class Meta:
        model = Tag
        fields = 'id', 'name', 'color', 'slug'


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ingredient"""
    measurement_unit = serializers.CharField(required=False)
    name = serializers.CharField(required=False)

    class Meta:
        model = Ingredient
        fields = 'id', 'name', 'measurement_unit'


class IngredientRecipeSerializer(serializers.ModelSerializer):

    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )
    name = serializers.StringRelatedField(
        source='ingredient.name'
    )
    measurement_unit = serializers.StringRelatedField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ['id', 'amount', 'name', 'measurement_unit']

    @staticmethod
    def validate_amount(value):
        if value < 1:
            raise serializers.ValidationError(
                'Нельзя указывать отрицательное количество ингредиентов.')
        return value


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe"""
    author = UserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = IngredientRecipeSerializer(
        many=True,
        source='ingredients_amount'
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    def get_is_favorited(self, obj):
        """Достаем булово значение поля is_favorite"""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(favorite__username=user.username, id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        """Достаем булово значение поля is_in_shopping_cart"""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(in_cart__username=user.username, id=obj.id).exists()

    @staticmethod
    def add_ingredients(recipe, ingredients_data):
        """Метод для добавления строк ингридиентов в
        таблицу IngredientRecipe"""
        for ingredient_data in ingredients_data:
            IngredientRecipe.objects.create(
                recipe=recipe,
                amount=ingredient_data.get('amount'),
                ingredient=ingredient_data.get('ingredient')
            )

    def create(self, validated_data):
        """Переопределенный метод create для корректного
        добавления ингридиентов и тегов"""
        tags = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients_amount')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.add(*tags)
        self.add_ingredients(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        """Переопределенный метод update для корректного
        патча рецепта"""
        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
            instance.tags.clear()
            instance.tags.add(*tags)
        if 'ingredients_amount' in validated_data:
            ingredients_data = validated_data.pop('ingredients_amount')
            IngredientRecipe.objects.filter(recipe=instance).delete()
            self.add_ingredients(instance, ingredients_data)
        return super().update(instance, validated_data)

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time', 'id', 'ingredients'
                  )
        extra_kwargs = {'pub_date': {'write_only': True}}
