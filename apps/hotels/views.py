from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Hotel, RoomType, Room
from .serializers import HotelSerializer, RoomTypeSerializer, RoomSerializer
from apps.core.permissions import IsHotelOwnerOrReadOnly, IsAdminOrReadOnly


class HotelViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Hotel model.
    Anyone can view hotels, only owners can edit/delete.
    """
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsHotelOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['rating', 'owner']
    search_fields = ['name', 'address', 'description']
    ordering_fields = ['name', 'rating']
    
    def perform_create(self, serializer):
        """Set the current user as hotel owner when creating."""
        serializer.save(owner=self.request.user)


class RoomTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for RoomType model.
    Anyone can view, only admins can edit/delete.
    """
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'capacity']


class RoomViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Room model.
    Anyone can view rooms, only admins/hotel owners can edit/delete.
    """
    queryset = Room.objects.select_related('hotel', 'room_type').all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['hotel', 'room_type', 'is_available', 'price_per_night']
    search_fields = ['description', 'hotel__name']
    ordering_fields = ['number', 'price_per_night']
    
    def get_permissions(self):
        """Custom permission logic for rooms."""
        if self.action in ['update', 'partial_update', 'destroy']:
            # For editing rooms, check if user is hotel owner
            return [IsHotelOwnerOrReadOnly()]
        return super().get_permissions()