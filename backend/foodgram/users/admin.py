from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'password',
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


admin.site.register(User, UserAdmin)
