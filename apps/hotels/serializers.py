#DRF modules
from rest_framework.serializers import (
    SerializerMethodField,
    ModelSerializer,
    CharField,
    IntegerField,
    PrimaryKeyRelatedField,
    DecimalField
    )

#Project modules
from apps.hotels.models import Hotel, RoomType, Room
from apps.users.serializers import UserSerializer

#Python modules

class HotelSerializer(ModelSerializer):
    """Serializer for Hotel model."""
    owner = SerializerMethodField()
    owner_info = UserSerializer(source='owner', read_only=True)
    
    class Meta:
        model = Hotel
        fields = ['id', 'name', 'address', 'rating', 'description', 'owner', 'owner_info']
        read_only_fields = ['id']
        
    def get_owner(self,obj):
        if obj.owner:
            return f"{obj.owner.first_name} {obj.owner.last_name}"
        return None


class RoomTypeSerializer(ModelSerializer):
    """Serializer for RoomType model."""
    class Meta:
        model = RoomType
        fields = ['id', 'name', 'capacity']
        read_only_fields = ['id']


class RoomSerializer(ModelSerializer):
    """Serializer for Room model."""
    hotel_name = CharField(source='hotel.name', read_only=True)
    room_type_name = CharField(source='room_type.name', read_only=True)
    
    class Meta:
        model = Room
        fields = [
            'id', 'number', 'price_per_night', 'description', 
            'is_available', 'hotel', 'hotel_name', 'room_type', 'room_type_name'
        ]
        read_only_fields = ['id']
        
class RoomCreateSerializer(ModelSerializer):
    
    """
    Room creation serializer.
    """
    class Meta:
        model = Room
        fields = [
            'id', 'number', 'price_per_night', 'description', 
            'is_available', 'room_type'
        ]
        read_only_fields = ['id']
        