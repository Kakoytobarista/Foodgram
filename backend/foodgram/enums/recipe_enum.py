import enum


class RecipeEnum(enum.Enum):
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


