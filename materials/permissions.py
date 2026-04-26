from rest_framework.permissions import BasePermission


class UserIsModeratorPermissions(BasePermission):
    """Проверка вхождения в группу модераторы."""
    def has_permission(self, request, view):
        if request.user.groups.filter(name="Модераторы").exists():
            return True
        return False


class UserInObjOrModeratorPermissions(BasePermission):
    """Проверка принадлежности объекта пользователю."""
    def has_object_permission(self, request, view, obj):
        if request.method in ("PUT", "PATCH"):
            return obj.author == request.user or request.user.groups.filter(name="Модераторы").exists()
        elif request.method in ("DELETE",):
            return obj.author == request.user
        return False
