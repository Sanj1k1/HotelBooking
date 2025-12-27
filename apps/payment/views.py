# DRF modules
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

# Django modules
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from django.db.models import Sum

# Project modules
from .models import Payment
from .serializers import PaymentSerializer
from apps.booking.models import Booking


class PaymentViewSet(ViewSet):
    """ViewSet for Payment model operations with user-specific access control."""
    
    permission_classes = [IsAuthenticated]
    
    @extend_schema(responses=PaymentSerializer(many=True))
    def list(self, request):
        """Retrieve all payments with optimized queries."""
        if request.user.is_staff:
            payments = Payment.objects.select_related('user').all()
        else:
            payments = Payment.objects.select_related('user').filter(user=request.user)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)
    
    @extend_schema(responses=PaymentSerializer)
    def retrieve(self, request, pk=None):
        """Retrieve a specific payment by ID with permission check."""
        payment = get_object_or_404(Payment.objects.select_related('user'), pk=pk)
        if not request.user.is_staff and payment.user != request.user:
            return Response(
                {"detail": "No permission"},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)
    
    @extend_schema(request=PaymentSerializer, responses=PaymentSerializer)
    def create(self, request):
        """Create a new payment for the authenticated user with optional booking association."""
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment = serializer.save(user=request.user)
            
            booking_id = request.data.get('booking_id')
            if booking_id:
                try:
                    booking = Booking.objects.get(id=booking_id, user=request.user)
                    booking.payment = payment
                    booking.save()
                    
                    if payment.status == 'completed':
                        booking.status = 'confirmed'
                        booking.save()
                except Booking.DoesNotExist:
                    # Silently ignore if booking doesn't exist or doesn't belong to user
                    pass
            
            return Response(
                PaymentSerializer(payment).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(request=PaymentSerializer, responses=PaymentSerializer)
    def update(self, request, pk=None):
        """Update an existing payment with permission check."""
        payment = get_object_or_404(Payment, pk=pk)
        if not request.user.is_staff and payment.user != request.user:
            return Response(
                {"detail": "No permission"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = PaymentSerializer(payment, data=request.data)
        if serializer.is_valid():
            updated_payment = serializer.save()
            
            # Update associated bookings if payment is completed
            if updated_payment.status == 'completed' and hasattr(updated_payment, 'bookings'):
                for booking in updated_payment.bookings.all():
                    booking.status = 'confirmed'
                    booking.save()
            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(responses=None)
    def destroy(self, request, pk=None):
        """Delete a payment (admin only)."""
        payment = get_object_or_404(Payment, pk=pk)
        if not request.user.is_staff:
            return Response(
                {"detail": "Admin only"},
                status=status.HTTP_403_FORBIDDEN
            )
        payment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'], url_path='my-payments')
    @extend_schema(responses=PaymentSerializer(many=True))
    def my_payments(self, request):
        """Retrieve all payments of the authenticated user."""
        payments = Payment.objects.select_related('user').filter(user=request.user)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], url_path='process')
    @extend_schema(responses=PaymentSerializer)
    def process_payment(self, request, pk=None):
        """Mark a payment as completed and update associated bookings."""
        payment = get_object_or_404(Payment, pk=pk)
        if not request.user.is_staff and payment.user != request.user:
            return Response(
                {"detail": "No permission"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        payment.status = 'completed'
        payment.save()
        
        # Update status of associated bookings
        if hasattr(payment, 'bookings'):
            for booking in payment.bookings.all():
                booking.status = 'confirmed'
                booking.save()
        
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)
