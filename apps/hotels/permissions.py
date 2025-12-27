# from Django REST framework modules 
from rest_framework.permissions import BasePermission,SAFE_METHODS

class IsAdminOrManagerOrReadOnly(BasePermission):
    """Permission class for admin, manager, or read-only access."""
    
    def has_permission(self, request, view):
        """Check if user has permission to access the view."""
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        
        return request.user.is_authenticated and (
            request.user.role in ['admin', 'manager']
        )

    def has_object_permission(self, request, view, obj):
        """Check if user has permission to access the specific object."""
        if request.method in SAFE_METHODS:
            return True
        
        if request.user.role == "admin":
            return True
        
        return obj.owner == request.user