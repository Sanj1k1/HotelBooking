from rest_framework import serializers
from .models import Hotel, RoomType, Room
from apps.users.serializers import UserSerializer


class HotelSerializer(serializers.ModelSerializer):
    """Serializer for Hotel model."""
    owner_info = UserSerializer(source='owner', read_only=True)
    
    class Meta:
        model = Hotel
        fields = ['id', 'name', 'address', 'rating', 'description', 'owner', 'owner_info']
        read_only_fields = ['id']


class RoomTypeSerializer(serializers.ModelSerializer):
    """Serializer for RoomType model."""
    class Meta:
        model = RoomType
        fields = ['id', 'name', 'capacity']
        read_only_fields = ['id']


class RoomSerializer(serializers.ModelSerializer):
    """Serializer for Room model."""
    hotel_name = serializers.CharField(source='hotel.name', read_only=True)
    room_type_name = serializers.CharField(source='room_type.name', read_only=True)
    
    class Meta:
        model = Room
        fields = [
            'id', 'number', 'price_per_night', 'description', 
            'is_available', 'hotel', 'hotel_name', 'room_type', 'room_type_name'
        ]
        read_only_fields = ['id']