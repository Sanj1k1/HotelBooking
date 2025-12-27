#DRF modules
from rest_framework.serializers import (
    CharField, 
    ModelSerializer, 
    ValidationError, 
    IntegerField,
    PrimaryKeyRelatedField
)

#Python modules
from django.utils import timezone

#Project modules
from apps.booking.models import Booking

class BookingSerializer(ModelSerializer):
    """
    Booking serializer with validation logic and related field representation.
    """
    room_number = CharField(source='room.number', read_only=True)
    hotel_name = CharField(source='room.hotel.name', read_only=True)
    total_price = IntegerField(read_only=True)  # We do read_only, because in the default=0 model
    payment = PrimaryKeyRelatedField(read_only=True) 
    
    class Meta:
        model = Booking
        fields = ['id', 'user', 'room', 'room_number', 'hotel_name', 
                'check_in', 'check_out', 'total_price', 'status', 'payment']
        read_only_fields = ['id', 'user', 'room_number', 'hotel_name', 'total_price', 'payment']
        
    def validate(self, attrs):
        """
        Validate booking dates and room availability.
        """
        check_in = attrs.get('check_in')
        check_out = attrs.get('check_out')
        room = attrs.get('room')

        if not check_in or not check_out:
            return attrs
            
        if check_out <= check_in:
            raise ValidationError({"check_out": "The departure date must be later than the arrival date."})
        
        if check_in < timezone.now().date():
            raise ValidationError({"check_in": "The arrival date cannot be in the past."})
        
        if room:
            overlapping = Booking.objects.filter(
                room=room,
                check_out__gt=check_in,
                check_in__lt=check_out,
                status__in=['confirmed', 'pending']
            ).exists()
            
            if overlapping:
                raise ValidationError({"room": "The room is already booked for the specified dates"})
        
        return attrs
    
    def create(self, validated_data):
        """
        Create booking with current user as owner.
        """
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
