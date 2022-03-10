import enum


class RecipeEnum(enum.Enum):
    RECIPE_VERBOSE_NAME = 'Рецепт'
    RECIPE_VERBOSE_NAME_PLURAL = 'Рецепты'

    AUTHOR_RELATED_NAME = 'recipes'
    AUTHOR_VERBOSE_NAME = 'Автор'

    NAME_MAX_LENGTH = 100
    NAME_VERBOSE_NAME = 'Название рецепта'

    IMAGE_VERBOSE_NAME = 'Картинка рецепта'

    TEXT_VERBOSE_NAME = 'Текст рецепта'

    INGREDIENTS_VERBOSE_NAME = 'Ингридиенты'
    INGREDIENTS_RELATED_NAE = 'ingredients'

    TAGS_RELATED_NAME = 'tags'
    TAGS_VERBOSE_NAME = ' Теги'

    COOKING_TIME = 'Время приготовления'

    RECIPE_PUB_DATE = 'Дата создания'


