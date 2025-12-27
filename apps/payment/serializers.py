#DRF modules
from rest_framework import serializers

#Project modules
from apps.payment.models import Payment
from apps.booking.models import Booking

class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for Payment model with booking association and validation."""
    
    booking_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'user', 'amount', 'payment_method', 
            'status', 'created_at', 'booking_id'
        ]
        read_only_fields = ['id', 'user', 'created_at']
    
    def validate_amount(self, value):
        """Validate that the payment amount is positive."""
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value
    
    def create(self, validated_data):
        """Create a payment and optionally associate it with a booking."""
        booking_id = validated_data.pop('booking_id', None)
        
        payment = Payment.objects.create(**validated_data)
        
        if booking_id:
            try:
                booking = Booking.objects.get(
                    id=booking_id, 
                    user=validated_data['user']
                )
                booking.payment = payment
                booking.save()
                
                if payment.status == 'completed':
                    booking.status = 'confirmed'
                    booking.save()
            except Booking.DoesNotExist:
                # Silently ignore if booking doesn't exist or doesn't belong to user
                pass 
        
        return payment
