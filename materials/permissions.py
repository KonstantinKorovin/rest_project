from rest_framework.permissions import BasePermission


class ThreeTierAccessPermission(BasePermission):
    """
    Общий permission для проверки является ли пользователь аутентифицированным,
    принадлежит ли он группе 'Managers',
    и является ли он  владельцем объекта.
    """

    def has_permission(self, request, view):
        user = request.user
        is_manager = request.user.groups.filter(name="Managers").exists()

        if not user.is_authenticated:
            return False

        if is_manager:
            if view.action in ["create", "destroy"]:
                return False
            return True

        if view.action == "list":
            return True

        if view.action == "create":
            return True

        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        is_manager = request.user.groups.filter(name="Managers").exists()

        if is_manager:
            return True

        return user == obj.owner
