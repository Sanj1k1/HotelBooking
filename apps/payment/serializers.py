from rest_framework import serializers
from .models import Payment
from apps.users.serializers import UserSerializer
from apps.booking.serializers import BookingSerializer


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for Payment model."""
    user_info = UserSerializer(source='user', read_only=True)
    booking_info = BookingSerializer(source='booking', read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'user', 'user_info', 'booking', 'booking_info',
            'amount', 'payment_method', 'status', 'transaction_id',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']
    
    def validate(self, data):
        """Validate payment amount matches booking total."""
        booking = data.get('booking')
        amount = data.get('amount')
        
        if booking and amount:
            if amount != booking.total_price:
                raise serializers.ValidationError(
                    f"Payment amount ({amount}) must match booking total ({booking.total_price})"
                )
        
        return data
    
    def create(self, validated_data):
        """Set current user as payment creator."""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)