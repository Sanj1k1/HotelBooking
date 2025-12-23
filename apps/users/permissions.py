from rest_framework import permissions


class IsSelfOrAdmin(permissions.BasePermission):
    """
    Permission to allow users to see/edit only themselves.
    Admin can see/edit everyone.
    """ 
    
    def has_object_permission(self, request, view, obj):
        # Admin can do anything
        if request.user.role == 'admin':
            return True
        # User can only access their own data
        return obj == request.user