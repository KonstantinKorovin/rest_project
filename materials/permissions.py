from rest_framework import permissions


class ThreeTierAccessPermission(permissions.BasePermission):
    """
    Общий permission для проверки является ли пользователь аутентифицированным,
    принадлежит ли он группе 'Managers',
    и является ли он  владельцем объекта.
    """

    def has_permission(self, request, view):
        user = request.user
        is_manager = user.groups.filter(name="Managers").exists()

        if not user.is_authenticated:
            return False

        if is_manager:
            return request.method not in ("POST", "DELETE")

        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        is_manager = request.user.groups.filter(name="Managers").exists()

        if is_manager:
            if request.method in permissions.SAFE_METHODS:
                return True

        return user == obj.owner
