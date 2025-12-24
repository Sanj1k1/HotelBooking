# DRF modules
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

# Project modules
from django.shortcuts import get_object_or_404
from apps.booking.models import Booking
from apps.booking.serializers import BookingSerializer
from apps.hotels.models import Room
from apps.hotels.serializers import RoomSerializer


class BookingViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(responses=BookingSerializer(many=True))
    def list(self, request):
        if request.user.is_staff:
            bookings = Booking.objects.select_related('user', 'room', 'room__hotel', 'room__room_type').all()
        else:
            bookings = Booking.objects.select_related('user', 'room', 'room__hotel', 'room__room_type').filter(user=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
    
    @extend_schema(responses=BookingSerializer)
    def retrieve(self, request, pk=None):
        booking = get_object_or_404(Booking.objects.select_related('user', 'room', 'room__hotel', 'room__room_type'), pk=pk)
        if not request.user.is_staff and booking.user != request.user:
            return Response({"detail": "No permission"}, status=status.HTTP_403_FORBIDDEN)
        serializer = BookingSerializer(booking)
        return Response(serializer.data)
    
    @extend_schema(request=BookingSerializer, responses=BookingSerializer)
    def create(self, request):
        serializer = BookingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            booking = serializer.save()
            return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(request=BookingSerializer, responses=BookingSerializer)
    def update(self, request, pk=None):
        booking = get_object_or_404(Booking, pk=pk)
        if not request.user.is_staff and booking.user != request.user:
            return Response({"detail": "No permission"}, status=status.HTTP_403_FORBIDDEN)
        
        if booking.status in ['completed', 'cancelled']:
            return Response({"error": "Cannot modify"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = BookingSerializer(booking, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(request=BookingSerializer, responses=BookingSerializer)
    def partial_update(self, request, pk=None):
        booking = get_object_or_404(Booking, pk=pk)
        if not request.user.is_staff and booking.user != request.user:
            return Response({"detail": "No permission"}, status=status.HTTP_403_FORBIDDEN)
        
        if booking.status in ['completed', 'cancelled']:
            return Response({"error": "Cannot modify"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = BookingSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(responses=None)
    def destroy(self, request, pk=None):
        booking = get_object_or_404(Booking, pk=pk)
        if not request.user.is_staff:
            return Response({"detail": "Admin only"}, status=status.HTTP_403_FORBIDDEN)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'], url_path='cancel')
    @extend_schema(responses=BookingSerializer)
    def cancel_booking(self, request, pk=None):
        booking = get_object_or_404(Booking, pk=pk)
        if not request.user.is_staff and booking.user != request.user:
            return Response({"detail": "No permission"}, status=status.HTTP_403_FORBIDDEN)
        
        if booking.status == 'cancelled':
            return Response({"error": "Already cancelled"}, status=status.HTTP_400_BAD_REQUEST)
        
        if booking.status == 'completed':
            return Response({"error": "Cannot cancel completed booking"}, status=status.HTTP_400_BAD_REQUEST)
        
        booking.status = 'cancelled'
        booking.save()
        serializer = BookingSerializer(booking)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='my-bookings')
    @extend_schema(responses=BookingSerializer(many=True))
    def my_bookings(self, request):
        bookings = Booking.objects.select_related('user', 'room', 'room__hotel', 'room__room_type').filter(user=request.user)
        status_filter = request.query_params.get('status')
        if status_filter:
            bookings = bookings.filter(status=status_filter)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='available-rooms')
    def available_rooms(self, request):
        check_in = request.query_params.get('check_in')
        check_out = request.query_params.get('check_out')
        hotel_id = request.query_params.get('hotel_id')
        capacity = request.query_params.get('capacity')

        if not check_in or not check_out:
            return Response(
                {"error": "check_in and check_out required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        rooms_query = Room.objects.select_related('hotel', 'room_type').filter(is_available=True)

        if hotel_id:
            rooms_query = rooms_query.filter(hotel_id=hotel_id)
        
        if capacity:
            rooms_query = rooms_query.filter(room_type__capacity__gte=capacity)

        booked_room_ids = Booking.objects.filter(
            check_out__gt=check_in,
            check_in__lt=check_out,
            status__in=['confirmed', 'pending']
        ).values_list('room_id', flat=True)

        available_rooms = rooms_query.exclude(id__in=booked_room_ids)

        serializer = RoomSerializer(available_rooms, many=True)
        
        return Response({
            'check_in': check_in,
            'check_out': check_out,
            'available_rooms': serializer.data,
            'count': available_rooms.count()
        })