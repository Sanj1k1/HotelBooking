from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Payment
from .serializers import PaymentSerializer
from apps.core.permissions import IsOwnerOrReadOnly


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Payment model.
    Users can only see their own payments.
    """
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_method', 'booking']
    ordering_fields = ['created_at', 'amount']
    
    def get_queryset(self):
        """Optimized queryset with select_related."""
        # OPTIMIZATION: select_related reduces multiple queries
        queryset = Payment.objects.select_related(
            'user',                    # Load user
            'booking',                 # Load booking
            'booking__room',           # Load room through booking
            'booking__room__hotel',    # Load hotel through room
            'booking__room__room_type' # Load room_type through room
        ).all()
        
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        
        return queryset
    
    def perform_create(self, serializer):
        """Set current user as payment creator."""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        """Mark payment as completed (admin only)."""
        payment = self.get_object()
        
        if not request.user.is_staff:
            return Response(
                {'error': 'Only admins can mark payments as completed'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if payment.status == 'completed':
            return Response(
                {'error': 'Payment is already completed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        payment.status = 'completed'
        payment.save()
        
        return Response({
            'message': 'Payment marked as completed',
            'payment_id': payment.id,
            'status': payment.status
        })