import enum


class UserEnum(enum.Enum):
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

    FIRST_NAME_VERBOSE_NAME = 'Фамилия'
    FIRST_NAME_MAX_LENGTH = 150

    LAST_NAME_VERBOSE_NAME = 'Фамилия'
    LAST_NAME_MAX_LENGTH = 150

