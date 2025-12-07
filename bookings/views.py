from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Booking
from .serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing bookings.
    
    Provides standard CRUD operations:
    - list: GET /bookings/
    - create: POST /bookings/
    - retrieve: GET /bookings/{id}/
    - update: PUT /bookings/{id}/
    - partial_update: PATCH /bookings/{id}/
    - destroy: DELETE /bookings/{id}/
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
