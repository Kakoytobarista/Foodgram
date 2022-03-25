from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.validators import UniqueValidator

from enums.ingredient_recipe_enum import IngredientRecipeEnum
from enums.tag_enum import TagEnum
from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag
from users.models import User

from api.mixins import RecipeMixin


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для использования с моделью User."""
    username = serializers.CharField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'password',
        )
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('is_subscribed',)

    def get_is_subscribed(self, obj):
        """Проверка подписки пользователей.
        Определяет - подписан ли текущий пользователь
        на просматриваемого пользователя.
        Args:
            obj (User): Пользователь, на которого проверяется подписка.
        Returns:
            bool: True, если подписка есть. Во всех остальных случаях False.
        """
        user = self.context.get('request').user
        if user.is_anonymous or (user == obj):
            return False
        return user.subscribe.filter(id=obj.id).exists()

    def create(self, validated_data):
        """Создаёт нового пользователя с запрошенными полями.
        Args:
            validated_data (dict): Полученные проверенные данные.
        Returns:
            User: Созданный пользователь.
        """
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe.
    Определён укороченный набор полей для некоторых эндпоинтов.
    """

    class Meta:
        model = Recipe
        fields = 'id', 'name', 'image', 'cooking_time'
        read_only_fields = ('__all__',)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода тэгов.
    """

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ingredient"""
    measurement_unit = serializers.CharField(required=False)
    name = serializers.CharField(required=False)

    class Meta:
        model = Ingredient
        fields = 'id', 'name', 'measurement_unit'


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для атрибута класса RecipeSerializer"""
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient', queryset=Ingredient.objects.all()
    )
    name = serializers.StringRelatedField(source='ingredient.name')
    measurement_unit = serializers.StringRelatedField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ['id', 'amount', 'name', 'measurement_unit']

    @staticmethod
    def validate_amount(value):
        if value <= 0:
            raise serializers.ValidationError(
                'Нельзя указывать отрицательное количество ингредиентов.'
            )
        return value


class RecipeCreateSerializer(RecipeMixin):
    """Сериализатор для модели Recipe"""
    author = UserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = IngredientRecipeSerializer(many=True, source='ingredients_amount')
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'author',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
            'id',
            'ingredients',
        )
        extra_kwargs = {'pub_date': {'write_only': True}}

    @staticmethod
    def add_ingredients(recipe, ingredients_data):
        """Метод для добавления строк ингридиентов в
        таблицу IngredientRecipe"""
        for ingredient_data in ingredients_data:
            IngredientRecipe.objects.create(
                recipe=recipe,
                amount=ingredient_data.get('amount'),
                ingredient=ingredient_data.get('ingredient'),
            )

    def create(self, validated_data):
        """Переопределенный метод create для корректного
        добавления ингридиентов и тегов"""
        ingredients_data = validated_data.pop('ingredients_amount')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.add(*tags)
        self.add_ingredients(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        """Переопределенный метод update для корректного
        патча рецепта"""
        if TagEnum.TAGS_NAME.value in validated_data:
            tags = validated_data.pop('tags')
            instance.tags.clear()
            instance.tags.add(*tags)
        if IngredientRecipeEnum.INGREDIENTS_AMOUNT.value in validated_data:
            ingredients_data = validated_data.pop('ingredients_amount')
            IngredientRecipe.objects.filter(recipe=instance).delete()
            self.add_ingredients(instance, ingredients_data)
        return super().update(instance, validated_data)


class RecipeSerializer(RecipeMixin):
    """Сериализатор для чтения рецептов"""
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientRecipeSerializer(read_only=True,
                                             many=True,
                                             source=IngredientRecipeEnum.INGREDIENTS_AMOUNT.value)
    image = Base64ImageField()
    author = UserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )


class RecipeFavoriteCartSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления в корзину/в избранное рецепта"""

    class Meta:
        model = Recipe
        fields = 'id', 'name', 'image', 'cooking_time'


class UserSubscribeSerializer(UserSerializer):
    """Сериализатор для вывода авторов на которых подписан текущий пользователь."""
    recipes = ShortRecipeSerializer(many=True,
                                    read_only=True)
    recipes_count = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
        read_only_fields = ('__all__',)

    @staticmethod
    def get_is_subscribed(*args):
        """Проверка подписки пользователей.
        Переопределённый метод родительского класса для уменьшения нагрузки,
        так как в текущей реализации всегда вернёт `True`.
        Returns:
            bool: True
        """
        return True

    @staticmethod
    def get_recipes_count(obj):
        """Показывает общее количество рецептов у каждого автора.
        Args:
            obj (User): Запрошенный пользователь.
        Returns:
            int: Количество рецептов созданных запрошенным пользователем.
        """
        return obj.recipes.count()
