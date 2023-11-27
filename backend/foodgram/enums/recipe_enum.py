import enum

class RecipeEnum(enum.Enum):
    RECIPE_VERBOSE_NAME = 'Recipe'
    RECIPE_VERBOSE_NAME_PLURAL = 'Recipes'

    RECIPE_ORDERING = ['-pub_date']

    AUTHOR_RELATED_NAME = 'recipes'
    AUTHOR_VERBOSE_NAME = 'Author'

    NAME_MAX_LENGTH = 100
    NAME_VERBOSE_NAME = 'Recipe Name'

    IMAGE_VERBOSE_NAME = 'Recipe Image'

    TEXT_VERBOSE_NAME = 'Recipe Text'
    TEXT_MAX_LENGTH = 1000

    INGREDIENTS_VERBOSE_NAME = 'Ingredients'
    INGREDIENTS_RELATED_NAME = 'ingredients'

    TAGS_RELATED_NAME = 'tags'
    TAGS_VERBOSE_NAME = 'Tags'

    COOKING_TIME = 'Cooking Time'

    RECIPE_PUB_DATE = 'Creation Date'

    FAVORITES_VERBOSE_NAME = 'Favorites'
    FAVORITES_RELATED_NAME = 'favorite'
    FAVORITES_TO = 'self'

    IN_CARD_VERBOSE_NAME = 'In Shopping Cart'
    IN_CARD_RELATED_NAME = 'cart'
    IN_CARD_TO = 'self'

    ERROR_MESSAGE_IS_FAVORITE_YET = {
        'message': 'Recipe already added to your favorites'
    }
    ERROR_MESSAGE_IS_NOT_FAVORITE = {
        'message': 'Recipe is not in your favorites'
    }

    ERROR_MESSAGE_IS_IN_CART_YET = {
        'message': 'Recipe already added to the shopping cart'
    }
    ERROR_MESSAGE_IS_NOT_IN_CART = {
        'message': 'Recipe is not in the shopping cart'
    }
    FOOD_READY_YET_MESSAGE = 'Your dish is ready!'
    TOO_MUCH_WAIT_MESSAGE = 'Too long to wait...'
