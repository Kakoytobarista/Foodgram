import enum

class IngredientRecipeEnum(enum.Enum):
    RECIPE_RELATED_NAME = 'ingredients_amount'
    RECIPE_AMOUNT_VERBOSE_NAME = 'Amount'
    INGREDIENTS_AMOUNT = 'ingredients_amount'

    VERBOSE_NAME = 'Ingredient - Recipe'
    PLURAL_VERBOSE_NAME = 'Ingredients - Recipes'

    CONSTRAINS_RECIPE_FIELDS = ['ingredient', 'recipe']
    CONSTRAINS_RECIPE_NAME = 'unique_ingredient_recipe'
