import enum

class IngredientEnum(enum.Enum):
    INGREDIENT_VERBOSE_NAME = 'Ingredient'
    INGREDIENT_VERBOSE_NAME_PLURAL = 'Ingredients'

    NAME_MAX_LENGTH = 100
    NAME_VERBOSE_NAME = 'Ingredient Name'

    COUNT_VERBOSE_NAME = 'Number of Ingredients'
    MEASUREMENT_UNIT_MAX_LENGTH = 50
    MEASUREMENT_UNIT_VERBOSE_NAME = 'Measurement Unit'
