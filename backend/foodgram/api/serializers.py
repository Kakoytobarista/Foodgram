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
    """Serializer for working with the User model.

    Attributes:
        is_subscribed (SerializerMethodField): A method field to determine if the current user is subscribed to the viewed user.
    """
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
        """Check user subscription.

        Determines whether the current user is subscribed to the viewed user.

        Args:
            obj (User): The user to check for subscription.

        Returns:
            bool: True if there is a subscription, False otherwise.
        """
        user = self.context.get('request').user
        if user.is_anonymous or (user == obj):
            return False
        return user.subscribe.filter(id=obj.id).exists()

    def create(self, validated_data):
        """Create a new user with the requested fields.

        Args:
            validated_data (dict): Validated data received.

        Returns:
            User: The created user.
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
    """Serializer for the Recipe model with a shortened set of fields."""
    class Meta:
        model = Recipe
        fields = 'id', 'name', 'image', 'cooking_time'
        read_only_fields = ('__all__',)

class TagSerializer(serializers.ModelSerializer):
    """Serializer for displaying tags."""
    class Meta:
        model = Tag
        fields = '__all__'

class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for the Ingredient model."""
    measurement_unit = serializers.CharField(required=False)
    name = serializers.CharField(required=False)

    class Meta:
        model = Ingredient
        fields = 'id', 'name', 'measurement_unit'

class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Serializer for the RecipeSerializer class attribute."""

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
        """Validate the amount of ingredients.

        Validates that the amount of ingredients is not negative.

        Args:
            value (int): The amount of ingredients.

        Raises:
            serializers.ValidationError: If the amount is negative.

        Returns:
            int: The validated amount.
        """
        if value <= 0:
            raise serializers.ValidationError(
                'Negative ingredient amounts are not allowed.'
            )
        return value

class RecipeCreateSerializer(RecipeMixin):
    """Serializer for the Recipe model."""

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
        """Method to add ingredient rows to the IngredientRecipe table."""
        for ingredient_data in ingredients_data:
            IngredientRecipe.objects.create(
                recipe=recipe,
                amount=ingredient_data.get('amount'),
                ingredient=ingredient_data.get('ingredient'),
            )

    def create(self, validated_data):
        """Overridden create method for correctly adding ingredients and tags."""
        ingredients_data = validated_data.pop('ingredients_amount')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.add(*tags)
        self.add_ingredients(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        """Overridden update method for correctly patching the recipe."""
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
    """Serializer for reading recipes."""

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
    """Serializer for adding a recipe to the cart/favorites."""

    class Meta:
        model = Recipe
        fields = 'id', 'name', 'image', 'cooking_time'


class UserSubscribeSerializer(UserSerializer):
    """Serializer for displaying authors subscribed by the current user."""

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
        """Check user subscription.

        Overridden method of the parent class to reduce the load, as it will always return `True`.

        Returns:
            bool: True
        """
        return True

    @staticmethod
    def get_recipes_count(obj):
        """Show the total number of recipes for each author.

        Args:
            obj (User): Requested user.

        Returns:
            int: Number of recipes created by the requested user.
        """
        return obj.recipes.count()
