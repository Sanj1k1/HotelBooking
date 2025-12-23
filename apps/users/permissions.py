from rest_framework import permissions


class IsSelfOrAdmin(permissions.BasePermission):
    """
    Permission to allow users to see/edit only themselves.
    Admin can see/edit everyone.
    """ 
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
    
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True 
        
        return obj == request.user
        
    