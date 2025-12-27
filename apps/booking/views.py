# Python modules
from typing import Any

# DRF modules
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema

# Django modules
from django.shortcuts import get_object_or_404
from django.db.models import QuerySet

# Project modules
from apps.booking.models import Booking
from apps.booking.serializers import BookingSerializer
from apps.hotels.models import Room
from apps.hotels.serializers import RoomSerializer


class BookingViewSet(ViewSet):
    """
    ViewSet for managing Bookings.
    """
    permission_classes: list[IsAuthenticated] = [IsAuthenticated]

    @extend_schema(responses=BookingSerializer(many=True))
    def list(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        GET /api/bookings/ - List bookings (admin sees all, users see their own)
        """
        if request.user.is_staff:
            bookings: QuerySet[Booking] = Booking.objects.select_related(
                'user', 'room', 'room__hotel', 'room__room_type'
            ).all()
        else:
            bookings: QuerySet[Booking] = Booking.objects.select_related(
                'user', 'room', 'room__hotel', 'room__room_type'
            ).filter(user=request.user)

        serializer: BookingSerializer = BookingSerializer(bookings, many=True)
        return DRFResponse(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(responses=BookingSerializer)
    def retrieve(self, request: DRFRequest, pk: int = None, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        GET /api/bookings/{id}/ - Retrieve a specific booking
        """
        booking: Booking = get_object_or_404(
            Booking.objects.select_related('user', 'room', 'room__hotel', 'room__room_type'), pk=pk
        )
        if not request.user.is_staff and booking.user != request.user:
            return DRFResponse({"detail": "No permission"}, status=status.HTTP_403_FORBIDDEN)

        serializer: BookingSerializer = BookingSerializer(booking)
        return DRFResponse(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=BookingSerializer, responses=BookingSerializer)
    def create(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        POST /api/bookings/ - Create a new booking
        """
        serializer: BookingSerializer = BookingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            booking: Booking = serializer.save()
            return DRFResponse(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)
        return DRFResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=BookingSerializer, responses=BookingSerializer)
    def update(self, request: DRFRequest, pk: int = None, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        PUT /api/bookings/{id}/ - Full update of booking
        """
        booking: Booking = get_object_or_404(Booking, pk=pk)
        if not request.user.is_staff and booking.user != request.user:
            return DRFResponse({"detail": "No permission"}, status=status.HTTP_403_FORBIDDEN)

        if booking.status in ['completed', 'cancelled']:
            return DRFResponse({"error": "Cannot modify"}, status=status.HTTP_400_BAD_REQUEST)

        serializer: BookingSerializer = BookingSerializer(booking, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return DRFResponse(serializer.data, status=status.HTTP_200_OK)
        return DRFResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=BookingSerializer, responses=BookingSerializer)
    def partial_update(self, request: DRFRequest, pk: int = None, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        PATCH /api/bookings/{id}/ - Partial update of booking
        """
        booking: Booking = get_object_or_404(Booking, pk=pk)
        if not request.user.is_staff and booking.user != request.user:
            return DRFResponse({"detail": "No permission"}, status=status.HTTP_403_FORBIDDEN)

        if booking.status in ['completed', 'cancelled']:
            return DRFResponse({"error": "Cannot modify"}, status=status.HTTP_400_BAD_REQUEST)

        serializer: BookingSerializer = BookingSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return DRFResponse(serializer.data, status=status.HTTP_200_OK)
        return DRFResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses=None)
    def destroy(self, request: DRFRequest, pk: int = None, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        DELETE /api/bookings/{id}/ - Delete booking (admin only)
        """
        booking: Booking = get_object_or_404(Booking, pk=pk)
        if not request.user.is_staff:
            return DRFResponse({"detail": "Admin only"}, status=status.HTTP_403_FORBIDDEN)
        booking.delete()
        return DRFResponse(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], url_path='cancel')
    @extend_schema(responses=BookingSerializer)
    def cancel_booking(self, request: DRFRequest, pk: int = None, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        POST /api/bookings/{id}/cancel/ - Cancel a booking
        """
        booking: Booking = get_object_or_404(Booking, pk=pk)
        if not request.user.is_staff and booking.user != request.user:
            return DRFResponse({"detail": "No permission"}, status=status.HTTP_403_FORBIDDEN)

        if booking.status == 'cancelled':
            return DRFResponse({"error": "Already cancelled"}, status=status.HTTP_400_BAD_REQUEST)
        if booking.status == 'completed':
            return DRFResponse({"error": "Cannot cancel completed booking"}, status=status.HTTP_400_BAD_REQUEST)

        booking.status = 'cancelled'
        booking.save()
        serializer: BookingSerializer = BookingSerializer(booking)
        return DRFResponse(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='my-bookings')
    @extend_schema(responses=BookingSerializer(many=True))
    def my_bookings(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        GET /api/bookings/my-bookings/ - Get current user's bookings
        """
        bookings: QuerySet[Booking] = Booking.objects.select_related(
            'user', 'room', 'room__hotel', 'room__room_type'
        ).filter(user=request.user)

        status_filter: str | None = request.query_params.get('status')
        if status_filter:
            bookings = bookings.filter(status=status_filter)

        serializer: BookingSerializer = BookingSerializer(bookings, many=True)
        return DRFResponse(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='available-rooms')
    def available_rooms(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        GET /api/bookings/available-rooms/ - List available rooms for given dates and optional filters
        """
        check_in: str | None = request.query_params.get('check_in')
        check_out: str | None = request.query_params.get('check_out')
        hotel_id: str | None = request.query_params.get('hotel_id')
        capacity: str | None = request.query_params.get('capacity')

        if not check_in or not check_out:
            return DRFResponse(
                {"error": "check_in and check_out required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        rooms_query: QuerySet[Room] = Room.objects.select_related('hotel', 'room_type').filter(is_available=True)

        if hotel_id:
            rooms_query = rooms_query.filter(hotel_id=hotel_id)

        if capacity:
            rooms_query = rooms_query.filter(room_type__capacity__gte=capacity)

        booked_room_ids = Booking.objects.filter(
            check_out__gt=check_in,
            check_in__lt=check_out,
            status__in=['confirmed', 'pending']
        ).values_list('room_id', flat=True)

        available_rooms: QuerySet[Room] = rooms_query.exclude(id__in=booked_room_ids)

        serializer: RoomSerializer = RoomSerializer(available_rooms, many=True)

        return DRFResponse({
            'check_in': check_in,
            'check_out': check_out,
            'available_rooms': serializer.data,
            'count': available_rooms.count()
        }, status=status.HTTP_200_OK)
