import enum


class IngredientRecipeEnum(enum.Enum):
    RECIPE_RELATED_NAME = 'ingredients_amount'
    RECIPE_AMOUNT_VERBOSE_NAME = 'Количество'
    INGREDIENTS_AMOUNT = 'ingredients_amount'

    VERBOSE_NAME = 'Ингредиент - Рецепт'
    PLURAL_VERBOSE_NAME = 'Ингредиенты - Рецепты'

    CONSTRAINS_RECIPE_FIELDS = ['ingredient', 'recipe']
    CONSTRAINS_RECIPE_NAME = 'unique_ingredient_recipe'
