from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Изменять объекты могут только их владельцы.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
