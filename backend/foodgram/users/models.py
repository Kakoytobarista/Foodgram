import django.contrib.auth.validators
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.password_validation import validate_password

from enums.user_enum import UserEnum


class User(AbstractUser):
    AUTH_USER = 'auth_user'
    ADMIN = 'admin'
    USER_ROLE_CHOICES = [
        (AUTH_USER, UserEnum.AUTH_USER.value),
        (ADMIN, UserEnum.ADMIN_USER.value),
    ]
    username = models.CharField(
        error_messages=UserEnum.USERNAME_ERROR_MESSAGE.value,
        help_text=UserEnum.USERNAME_HELP_TEXT.value,
        max_length=UserEnum.USERNAME_MAXLENGTH.value,
        unique=True,
        validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
        verbose_name=UserEnum.USERNAME_VERBOSE_NAME.value,
    )
    password = models.CharField(
        max_length=UserEnum.PASSWORD_MAX_LENGTH.value,
        verbose_name=UserEnum.PASSWORD_VERBOSE_NAME.value,
        validators=[validate_password],
    )
    email = models.EmailField(
        max_length=UserEnum.EMAIL_MAX_LENGTH.value,
        verbose_name=UserEnum.EMAIL_VERBOSE_NAME.value,
    )
    bio = models.TextField(
        blank=True,
        verbose_name=UserEnum.BIO_VERBOSE_NAME.value,
    )
    role = models.TextField(
        choices=USER_ROLE_CHOICES,
        default=AUTH_USER,
        verbose_name=UserEnum.ROLE_VERBOSE_NAME.value,
    )
    first_name = models.CharField(
        blank=True,
        max_length=UserEnum.FIRST_NAME_MAX_LENGTH.value,
        verbose_name=UserEnum.FIRST_NAME_VERBOSE_NAME.value
    )
    last_name = models.CharField(
        blank=True,
        max_length=UserEnum.LAST_NAME_MAX_LENGTH.value,
        verbose_name=UserEnum.LAST_NAME_VERBOSE_NAME.value
    )
    subscribe = models.ManyToManyField(
        verbose_name='Подписка',
        related_name='subscribers',
        to='self',
        symmetrical=False,
    )

    class Meta:
        verbose_name = UserEnum.USER_VERBOSE_NAME.value
        verbose_name_plural = UserEnum.USER_VERBOSE_NAME_PLURAL.value

