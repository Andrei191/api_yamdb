from rest_framework import permissions


class IsAdminOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_superuser
                or request.method in permissions.SAFE_METHODS
                or request.user.is_admin)


class IsAuthorOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                or request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        if (not request.user.is_authenticated or request.method
           in permissions.SAFE_METHODS):
            return True
        return obj.author == request.user


class IsModerOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                or request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return request.user.is_moderator


class AuthorOrModerPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_staff
        )


class IsAdminOrUserReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return (request.user.is_admin
                or request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_admin
        return False
