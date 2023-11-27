import enum

class UserEnum(enum.Enum):
    SUBSCRIBE_M2M = 'subscribe'

    USER_VERBOSE_NAME = 'User'
    USER_VERBOSE_NAME_PLURAL = 'Users'

    AUTH_USER = 'Authenticated User'
    ADMIN_USER = 'Administrator'
    ROLE_VERBOSE_NAME = 'User Role'

    BIO_VERBOSE_NAME = 'Biography'

    EMAIL_VERBOSE_NAME = 'Email'
    EMAIL_MAX_LENGTH = 254

    USERNAME_VERBOSE_NAME = 'Username'
    USERNAME_ERROR_MESSAGE = {
        'unique': 'A user with this username already exists.'
    }
    USERNAME_HELP_TEXT = 'No more than 150 characters, letters, digits, and @/./+/-/_ only.'
    USERNAME_MAXLENGTH = 150

    PASSWORD_VERBOSE_NAME = 'Password'
    PASSWORD_MAX_LENGTH = 100

    FIRST_NAME_VERBOSE_NAME = 'First Name'
    FIRST_NAME_MAX_LENGTH = 150

    LAST_NAME_VERBOSE_NAME = 'Last Name'
    LAST_NAME_MAX_LENGTH = 150

    USER_RESET_PASSWORD_ERR_MESSAGE = 'The current password must match the previous one'
    USER_AUTH_ERR_MESSAGE = 'Check the password or try again later'

    SUBSCRIBE_VERBOSE_NAME = 'Subscription'
    SUBSCRIBE_RELATED_NAME = 'subscribers'
    SUBSCRIBE_TO = 'self'

    SUBSCRIBE_ERROR_ON_YOURSELF = {
        "errors": "Cannot delete or subscribe to oneself"
    }
    SUBSCRIBE_ERROR_YET_SUBSCRIBED = {
        "errors": "Cannot subscribe to an already subscribed user"
    }
    SUBSCRIBE_ERROR_DELETE_NOTHING = {
        "errors": "Cannot delete if not subscribed"
    }
