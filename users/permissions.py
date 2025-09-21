from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.groups.filter(name='Manager').exists())

class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.groups.filter(name='Employee').exists())