from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return (
            request.user
            and request.user.is_authentificated
            and obj.author == request.user
        )


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return (
            request.user
            and request.user.is_authentificated
            and request.user.role == "admin"
        )


class IsAdminOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return (
            request.user
            and request.user.is_authentificated
            and (request.user.role == "admin" or obj == request.user)
        )
