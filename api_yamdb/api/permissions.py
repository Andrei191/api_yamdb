from rest_framework import permissions


class IsAdminOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.role == "admin"
                or request.method in permissions.SAFE_METHODS)


