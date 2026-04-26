from rest_framework.permissions import BasePermission


class UserIsObjPermissions(BasePermission):
    """Проверка соответствия пользователя."""

    def has_object_permission(self, request, view, obj):
        if obj == request.user:
            return True
        return False


class UserInObjPermissions(BasePermission):
    """Проверка принадлежности объекта пользователю."""

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return False
