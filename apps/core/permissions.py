from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Others can only view.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        # GET, HEAD or OPTIONS requests are always allowed
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner
        # Check if object has 'user' attribute (Booking, Review, etc.)
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # Check if object has 'owner' attribute (Hotel, etc.)
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        
        # For other objects, allow only if user is staff
        return request.user.is_staff


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to create/edit/delete.
    Others can only view.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request
        # GET, HEAD or OPTIONS requests are always allowed
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to admins
        return request.user and request.user.is_staff


class IsHotelOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission for Hotel objects.
    Anyone can view, only owner can edit/delete.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only to hotel owner
        return obj.owner == request.user


class IsBookingOwner(permissions.BasePermission):
    """
    Custom permission for Booking objects.
    Only booking owner can view/edit/delete their bookings.
    Admin can view all bookings.
    """
    def has_object_permission(self, request, view, obj):
        # Admin can do anything
        if request.user and request.user.is_staff:
            return True
        
        # User can only access their own bookings
        return obj.user == request.user


class IsReviewOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission for Review objects.
    Anyone can read, only review author can edit/delete.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only to review author
        return obj.user == request.user