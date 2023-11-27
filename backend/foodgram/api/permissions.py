from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.viewsets import ViewSetMixin


class IsAuthorOrStaffOrReadOnly(permissions.BasePermission):
    """
    Custom permission class that allows read-only access to any user,
    allows authenticated users to create (POST) objects,
    and allows authors or staff/admins to update (PUT, PATCH, DELETE) their own objects.

    Methods:
    - has_permission(request: Request, view) -> bool: Check if the user has permission for the given request.
    - has_object_permission(request: Request, view, obj) -> bool: Check if the user has permission for the given object.
    """

    def has_permission(self, request: Request, view: ViewSetMixin) -> bool:
        """
        Check if the user has permission for the given request.

        Args:
        - request (Request): The incoming request.
        - view (ViewSetMixin): The view associated with the request.

        Returns:
        bool: True if the user has permission, False otherwise.
        """
        return (
            request.method in permissions.SAFE_METHODS or request.user.is_authenticated
        )

    def has_object_permission(self, request: Request, view: ViewSetMixin, obj) -> bool:
        """
        Check if the user has permission for the given object.

        Args:
        - request (Request): The incoming request.
        - view (ViewSetMixin): The view associated with the request.
        - obj: The object being accessed.

        Returns:
        bool: True if the user has permission, False otherwise.
        """
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_staff
        )
