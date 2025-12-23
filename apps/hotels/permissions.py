from rest_framework.permissions import BasePermission,SAFE_METHODS

class IsAdminOrManagerOrReadOnly(BasePermission):
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