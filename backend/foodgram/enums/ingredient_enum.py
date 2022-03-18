import enum


class IngredientEnum(enum.Enum):
    INGREDIENT_VERBOSE_NAME = 'Ингредиент'
    INGREDIENT_VERBOSE_NAME_PLURAL = 'Ингридиенты'

    NAME_MAX_LENGTH = 100
    NAME_VERBOSE_NAME = 'Название ингридиента'

    COUNT_VERBOSE_NAME = 'Количество ингридиентов'
    MEASUREMENT_UNIT_MAX_LENGTH = 50
    MEASUREMENT_UNIT_VERBOSE_NAME = 'Единица измерения'

