from rest_framework import viewsets, permissions
from apps.booking.models import Booking
from apps.booking.serializers import BookingSerializer

class IsAdminOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin' or obj.user == request.user

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrOwner]

    def get_queryset(self):
        """Optimized queryset with select_related to reduce SQL queries."""
        user = self.request.user
        
        # OPTIMIZATION: select_related reduces N+1 query problem
        queryset = Booking.objects.select_related(
            'user',           # Load user data in same query
            'room',           # Load room data
            'room__hotel',    # Load hotel through room
            'room__room_type' # Load room_type through room
        ).all()
        
        if user.role == 'admin':
            return queryset
        return queryset.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)