#DRF modules
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
#Django modules
from django.shortcuts import get_object_or_404

#Python modules

#Project modules
from apps.hotels.models import Hotel, RoomType, Room
from apps.hotels.serializers import HotelSerializer, RoomTypeSerializer, RoomSerializer,RoomCreateSerializer
from apps.hotels.permissions import IsAdminOrManagerOrReadOnly


class HotelViewSet(ViewSet):
    """ViewSet for Hotel model operations."""
    
    lookup_value_regex = r'\d+' #для теста нужен 
    permission_classes = [IsAdminOrManagerOrReadOnly]
    
    @extend_schema(responses=HotelSerializer(many=True))
    def list(self, request):
        """Retrieve all hotels with optimized queries."""
        # OPTIMIZATION
        hotels = Hotel.objects.select_related('owner').all()
        serializer = HotelSerializer(hotels, many=True)
        return Response(serializer.data)

    @extend_schema(responses=HotelSerializer)
    def retrieve(self, request, pk=None):
        """Retrieve a specific hotel by ID with optimized query."""
        # OPTIMIZATION
        hotel = get_object_or_404(Hotel.objects.select_related('owner'), pk=pk)
        serializer = HotelSerializer(hotel)
        return Response(serializer.data)
        
    @extend_schema(request=HotelSerializer, responses=HotelSerializer)
    def create(self,request):
        """Create a new hotel with the authenticated user as owner."""
        
        serializer = HotelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    @extend_schema(request=HotelSerializer,responses=HotelSerializer)
    def update(self,request,pk=None):
        """Update an existing hotel (full update)."""
        
        hotel = get_object_or_404(Hotel,pk=pk)
        self.check_object_permissions(request, hotel)
        serializer = HotelSerializer(hotel,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    @extend_schema(request=HotelSerializer,responses=HotelSerializer)
    def partial_update(self,request,pk=None):
        """Update specific fields of an existing hotel (partial update)."""
        
        hotel = get_object_or_404(Hotel,pk=pk)
        self.check_object_permissions(request, hotel)
        serializer = HotelSerializer(hotel,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    
    @extend_schema(responses=None)
    def destroy(self,request,pk=None):
        """Delete a hotel."""
        
        hotel = get_object_or_404(Hotel,pk=pk)
        self.check_object_permissions(request, hotel)
        hotel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True,methods=["get"])
    def rooms(self,request,pk=None):
        """Retrieve all rooms belonging to a specific hotel."""
        
        hotel = get_object_or_404(Hotel,pk=pk)
        rooms = Room.objects.filter(hotel=hotel)
        serializer = RoomSerializer(rooms,many=True)
        return Response(serializer.data)
    
    @extend_schema(request=RoomCreateSerializer,responses=RoomSerializer,description="Создает новую комнату и привязывает её к текущему отелю")
    @action(detail=True, methods=["post"], url_path='add-room')
    def add_room(self, request, pk=None):
        """Create a new room and associate it with the current hotel."""
        
        hotel = get_object_or_404(Hotel, pk=pk)
        self.check_object_permissions(request, hotel)
        serializer = RoomCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(hotel=hotel)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    @extend_schema(responses=HotelSerializer)
    @action(detail=False,methods=["get"],url_path="my-hotels")
    def my_hotels(self,request):
        """Retrieve all hotels owned by the authenticated user."""

        queryset = Hotel.objects.filter(owner=request.user).all()
        serializer = HotelSerializer(queryset,many=True)
        return Response(serializer.data)
        
        
class RoomTypeViewSet(ViewSet):
    
    """ViewSet for RoomType model operations."""
    
    lookup_field = "pk"
    
    @extend_schema(responses=RoomTypeSerializer(many=True))
    def list(self,request):
        """Retrieve all room types."""
        queryset = RoomType.objects.all()
        serializer = RoomTypeSerializer(queryset,many=True)
        return Response(serializer.data)
    
    @extend_schema(request=RoomTypeSerializer,responses=RoomTypeSerializer)
    def create(self,request):
        """Create a new room type."""
        
        serializer = RoomTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    @extend_schema(request=RoomTypeSerializer,responses=RoomTypeSerializer)
    def partial_update(self,request,pk=None):
        """Update specific fields of an existing room type (partial update)."""
        
        roomtype = get_object_or_404(RoomType,pk=pk)
        serializer = RoomTypeSerializer(roomtype,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    @extend_schema(responses=None)
    def destroy(self,request,pk=None):
        """Delete a room type."""
        
        roomtype = get_object_or_404(RoomType,pk=pk)
        roomtype.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)