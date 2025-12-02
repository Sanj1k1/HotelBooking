from rest_framework import serializers
from apps.booking.models import Booking
from apps.hotels.models import Room

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    room = serializers.StringRelatedField(read_only=True)
    room_id = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(),source='room',write_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'user', 'room', 'room_id', 'check_in', 'check_out', 'total_price', 'status']
        read_only_fields = ['id', 'user', 'status']
        
        