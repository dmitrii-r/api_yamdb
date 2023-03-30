from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Доступ разрешён только администратору.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser)


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    При небезопасном методе доступ разрешён только администратору.
    """
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and (
                    request.user.is_admin or request.user.is_superuser)))


class IsAuthorModeratorAdminOrReadOnly(permissions.BasePermission):
    """
    Доступ разрешён всем при безопасном методе,
    аутентифицированные пользователи могут использовать метод POST,
    остальные методы могут использовать автор,
    а также модератор, администратор и суперюзер.
    """
        def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)
                
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.method == 'POST' and request.user.is_authenticated
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
            or request.user.is_superuser
        )
