from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


class CustomUserAdmin(DjangoUserAdmin):
    """
    Admin class for custom User model.

    Attributes:
    - list_display (tuple): Fields to be displayed in the list view.
    - list_editable (tuple): Fields that can be edited directly in the list view.
    """

    list_display = (
        'username',
        'email',
        'bio',
        'role',
        'first_name',
        'last_name',
    )
    list_editable = (
        'first_name',
        'last_name',
        'role',
        'bio',
    )


admin.site.register(User, CustomUserAdmin)
