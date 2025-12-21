#DRF modules
from rest_framework.serializers import CharField,ModelSerializer
from rest_framework.serializers import ValidationError
#Python modules

#Project modules
from apps.booking.models import Booking
from apps.hotels.models import Room

class BookingSerializer(ModelSerializer):
    room_number = CharField(source='room.number', read_only=True)
    hotel_name = CharField(source='room.hotel.name', read_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'user', 'room', 'room_number', 'hotel_name', 'check_in', 'check_out', 'status']
        read_only_fields = ['id', 'user', 'room_number', 'hotel_name']
        
    def validate(self,attrs):
        room = attrs['room']
        check_in = attrs['check_in']
        check_out = attrs['check_out']

        if check_out <= check_in:
            raise ValidationError("Check-out date must be after check-in.")