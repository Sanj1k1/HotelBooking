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
from django.db.models import QuerySet, Sum

# Project modules
from .models import Payment
from .serializers import PaymentSerializer
from apps.booking.models import Booking


class PaymentViewSet(ViewSet):
    """
    ViewSet for managing Payments.
    """
    permission_classes: list[IsAuthenticated] = [IsAuthenticated]

    @extend_schema(responses=PaymentSerializer(many=True))
    def list(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        GET /api/payments/ - List all payments (admin) or user's payments
        """
        if request.user.is_staff:
            payments: QuerySet[Payment] = Payment.objects.select_related('user').all()
        else:
            payments: QuerySet[Payment] = Payment.objects.select_related('user').filter(user=request.user)

        serializer: PaymentSerializer = PaymentSerializer(payments, many=True)
        return DRFResponse(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(responses=PaymentSerializer)
    def retrieve(self, request: DRFRequest, pk: int = None, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        GET /api/payments/{id}/ - Retrieve a specific payment
        """
        payment: Payment = get_object_or_404(Payment.objects.select_related('user'), pk=pk)
        if not request.user.is_staff and payment.user != request.user:
            return DRFResponse({"detail": "No permission"}, status=status.HTTP_403_FORBIDDEN)

        serializer: PaymentSerializer = PaymentSerializer(payment)
        return DRFResponse(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=PaymentSerializer, responses=PaymentSerializer)
    def create(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        POST /api/payments/ - Create a new payment and link to booking if provided
        """
        serializer: PaymentSerializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment: Payment = serializer.save(user=request.user)

            booking_id: int | None = request.data.get('booking_id')
            if booking_id:
                try:
                    booking: Booking = Booking.objects.get(id=booking_id, user=request.user)
                    booking.payment = payment
                    if payment.status == 'completed':
                        booking.status = 'confirmed'
                    booking.save()
                except Booking.DoesNotExist:
                    pass

            return DRFResponse(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)
        return DRFResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=PaymentSerializer, responses=PaymentSerializer)
    def update(self, request: DRFRequest, pk: int = None, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        PUT /api/payments/{id}/ - Update a payment
        """
        payment: Payment = get_object_or_404(Payment, pk=pk)
        if not request.user.is_staff and payment.user != request.user:
            return DRFResponse({"detail": "No permission"}, status=status.HTTP_403_FORBIDDEN)

        serializer: PaymentSerializer = PaymentSerializer(payment, data=request.data)
        if serializer.is_valid():
            updated_payment: Payment = serializer.save()

            if updated_payment.status == 'completed' and hasattr(updated_payment, 'bookings'):
                for booking in updated_payment.bookings.all():
                    booking.status = 'confirmed'
                    booking.save()

            return DRFResponse(serializer.data, status=status.HTTP_200_OK)
        return DRFResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses=None)
    def destroy(self, request: DRFRequest, pk: int = None, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        DELETE /api/payments/{id}/ - Delete payment (admin only)
        """
        payment: Payment = get_object_or_404(Payment, pk=pk)
        if not request.user.is_staff:
            return DRFResponse({"detail": "Admin only"}, status=status.HTTP_403_FORBIDDEN)
        payment.delete()
        return DRFResponse(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='my-payments')
    @extend_schema(responses=PaymentSerializer(many=True))
    def my_payments(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        GET /api/payments/my-payments/ - Get current user's payments
        """
        payments: QuerySet[Payment] = Payment.objects.select_related('user').filter(user=request.user)
        serializer: PaymentSerializer = PaymentSerializer(payments, many=True)
        return DRFResponse(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='process')
    @extend_schema(responses=PaymentSerializer)
    def process_payment(self, request: DRFRequest, pk: int = None, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        POST /api/payments/{id}/process/ - Mark payment as completed and update bookings
        """
        payment: Payment = get_object_or_404(Payment, pk=pk)
        if not request.user.is_staff and payment.user != request.user:
            return DRFResponse({"detail": "No permission"}, status=status.HTTP_403_FORBIDDEN)

        payment.status = 'completed'
        payment.save()

        if hasattr(payment, 'bookings'):
            for booking in payment.bookings.all():
                booking.status = 'confirmed'
                booking.save()

        serializer: PaymentSerializer = PaymentSerializer(payment)
        return DRFResponse(serializer.data, status=status.HTTP_200_OK)
