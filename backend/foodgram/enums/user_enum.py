import enum


class UserEnum(enum.Enum):
    SUBSCRIBE_M2M = 'subscribe'

    USER_VERBOSE_NAME = 'Пользователь'
    USER_VERBOSE_NAME_PLURAL = 'Пользователи'

    AUTH_USER = 'Авторизованный пользователь'
    ADMIN_USER = 'Администратор'
    ROLE_VERBOSE_NAME = 'Пользовательская роль'

    BIO_VERBOSE_NAME = 'Биография'

    EMAIL_VERBOSE_NAME = 'Электронная почта'
    EMAIL_MAX_LENGTH = 254

    USERNAME_VERBOSE_NAME = 'Имя пользователя'
    USERNAME_ERROR_MESSAGE = {
        'unique': 'Пользователь с таким именем уже существует.'
    }
    USERNAME_HELP_TEXT = 'Не более 150 символов, буквы, цифры и @/./+/-/_ только.'
    USERNAME_MAXLENGTH = 150

    PASSWORD_VERBOSE_NAME = 'Паспорт'
    PASSWORD_MAX_LENGTH = 100

    FIRST_NAME_VERBOSE_NAME = 'Имя'
    FIRST_NAME_MAX_LENGTH = 150

    LAST_NAME_VERBOSE_NAME = 'Фамилия'
    LAST_NAME_MAX_LENGTH = 150

    USER_RESET_PASSWORD_ERR_MESSAGE = ('Текущий пароль должен совпадать '
                                       'с предыдущим')
    USER_AUTH_ERR_MESSAGE = ('Проверьте пароль или '
                             'попробуйте позже')

    SUBSCRIBE_VERBOSE_NAME = 'Подписка'
    SUBSCRIBE_RELATED_NAME = 'subscribers'
    SUBSCRIBE_TO = 'self'

    SUBSCRIBE_ERROR_ON_YOURSELF = {
                                      "errors": "Нельзя удалить или подписаться на самого себя"
                                  },
    SUBSCRIBE_ERROR_YET_SUBSCRIBED = {
                                      "errors": "Нельзя подписаться на уже подписанного"
                                  },
    SUBSCRIBE_ERROR_DELETE_NOTHING = {
                                      "errors": "Нельзя удалить если не подписан"
                                  },

