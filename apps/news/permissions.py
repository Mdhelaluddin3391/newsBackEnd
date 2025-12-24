from rest_framework.permissions import BasePermission


class IsJournalistOrAbove(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in ["journalist", "editor", "admin"]
        )


class IsEditorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in ["editor", "admin"]
        )
