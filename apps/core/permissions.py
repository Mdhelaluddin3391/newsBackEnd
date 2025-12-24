from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"


class IsEditor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["editor", "admin"]


class IsJournalist(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [
            "journalist", "editor", "admin"
        ]


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return hasattr(obj, "author") and obj.author == request.user
