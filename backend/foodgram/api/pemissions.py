from rest_framework import permissions
from rest_framework.request import Request


class IsAuthorOrStaffOrReadOnly(permissions.BasePermission):
    """
    GET - разрешено всем,
    POST - разрешено аутентифицированному пользователю
    PUT, PATCH, DELETE - резрешено автору или администратору
    """

    def has_permission(self, request: Request, view) -> bool:
        return (
            request.method in permissions.SAFE_METHODS or request.user.is_authenticated
        )

    def has_object_permission(self, request: Request, view, obj) -> bool:
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_staff
        )
