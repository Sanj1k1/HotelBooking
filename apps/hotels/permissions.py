# From DRF modules
from rest_framework.permissions import BasePermission,SAFE_METHODS

class IsAdminOrManagerOrReadOnly(BasePermission):
    """
    Custom permission class that allows:
    - Read access for authenticated users
    - Full access for admin and manager roles
    - Object-level write access for object owners (for non-admin/managers)
    """
    
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        
        return request.user.is_authenticated and (
            request.user.role in ['admin', 'manager']
        )

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        if request.user.role =="admin":
            return True
        
        return obj.owner == request.user