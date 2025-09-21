from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsManagerOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Manager has full access
        if request.user.groups.filter(name='Manager').exists():
            return True
        
        # Employee has just read-only access
        if request.user.groups.filter(name='Employee').exists():
            return request.method in SAFE_METHODS