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
from apps.hotels.serializers import HotelSerializer, RoomTypeSerializer, RoomSerializer
from apps.core.permissions import IsHotelOwnerOrReadOnly, IsAdminOrReadOnly


class HotelViewSet(ViewSet):
    lookup_value_regex = r'[0-9]' #для теста нужен 
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    @extend_schema(responses=HotelSerializer(many=True))
    def list(self, request):
        # OPTIMIZATION
        hotels = Hotel.objects.select_related('owner').all()
        serializer = HotelSerializer(hotels, many=True)
        return Response(serializer.data)

    @extend_schema(responses=HotelSerializer)
    def retrieve(self, request, pk=None):
        # OPTIMIZATION
        hotel = get_object_or_404(Hotel.objects.select_related('owner'), pk=pk)
        serializer = HotelSerializer(hotel)
        return Response(serializer.data)
        
    @extend_schema(request=HotelSerializer, responses=HotelSerializer)
    def create(self,request):
        serializer = HotelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    @extend_schema(request=HotelSerializer,responses=HotelSerializer)
    def update(self,request,pk=None):
        hotel = get_object_or_404(Hotel,pk=pk)
        serializer = HotelSerializer(hotel,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    @extend_schema(request=HotelSerializer,responses=HotelSerializer)
    def partial_update(self,request,pk=None):
        hotel = get_object_or_404(Hotel,pk=pk)
        serializer = HotelSerializer(hotel,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    
    @extend_schema(responses=None)
    def destroy(self,request,pk=None):
        hotel = get_object_or_404(Hotel,pk=pk)
        hotel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True,methods=["get"])
    def rooms(self,request,pk=None):
        hotel = get_object_or_404(Hotel,pk=pk)
        rooms = Room.objects.filter(hotel=hotel)
        serializer = RoomSerializer(rooms,many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=["post"], url_path='add-room')
    def add_room(self, request, pk=None):
        hotel = get_object_or_404(Hotel, pk=pk)
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(hotel=hotel)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

class RoomTypeViewSet(ViewSet):
    lookup_field = "pk"
    
    @extend_schema(responses=RoomTypeSerializer(many=True))
    def list(self,request):
        queryset = RoomType.objects.all()
        serializer = RoomTypeSerializer(queryset,many=True)
        return Response(serializer.data)
    
    @extend_schema(request=RoomTypeSerializer,responses=RoomTypeSerializer)
    def create(self,request):
        serializer = RoomTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    @extend_schema(request=RoomTypeSerializer,responses=RoomTypeSerializer)
    def partial_update(self,request,pk=None):
        roomtype = get_object_or_404(RoomType,pk=pk)
        serializer = RoomTypeSerializer(roomtype,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    @extend_schema(responses=None)
    def destroy(self,request,pk=None):
        roomtype = get_object_or_404(RoomType,pk=pk)
        roomtype.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)