from rest_framework import permissions

class IsSelfOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == obj.ROLE_ADMIN:
            return True
        return obj.id == request.user.id