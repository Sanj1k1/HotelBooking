from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from bookings.models import Booking

from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing payments.
    
    Provides standard CRUD operations plus custom actions:
    - list: GET /payments/
    - create: POST /payments/
    - retrieve: GET /payments/{id}/
    - update: PUT /payments/{id}/
    - partial_update: PATCH /payments/{id}/
    - destroy: DELETE /payments/{id}/
    - create_for_booking: POST /payments/create_for_booking/{booking_id}/
    - confirm: POST /payments/{id}/confirm/
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    @action(detail=False, methods=['post'], url_path='create_for_booking/(?P<booking_id>[^/.]+)')
    def create_for_booking(self, request, booking_id=None):
        """
        Create a payment for a specific booking.
        POST /payments/create_for_booking/{booking_id}/
        """
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response(
                {'error': 'Booking not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        payment, created = Payment.objects.get_or_create(
            booking=booking,
            defaults={
                'provider': request.data.get('provider', 'mock'),
                'amount': booking.amount,
                'status': 'pending',
            },
        )

        if not created:
            payment.provider = request.data.get('provider', payment.provider)
            payment.amount = booking.amount
            payment.status = 'pending'
            payment.transaction_id = ''
            payment.save()

        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """
        Confirm a payment.
        POST /payments/{id}/confirm/
        """
        try:
            payment = self.get_object()
        except Payment.DoesNotExist:
            return Response(
                {'error': 'Payment not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        payment.status = 'paid'
        payment.transaction_id = request.data.get('transaction_id', 'TXN123456')
        payment.save()

        booking = payment.booking
        booking.is_paid = True
        booking.save()

        return Response(
            {'message': 'Payment successful'},
            status=status.HTTP_200_OK
        )
