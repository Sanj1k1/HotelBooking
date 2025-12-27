#Python modules
from typing import Any
from drf_spectacular.utils import extend_schema

#Django modules
from django.shortcuts import get_object_or_404
from django.db.models import QuerySet

#DRF modules
from rest_framework.permissions import BasePermission
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.decorators import action

#Project modules
from apps.hotels.models import Hotel, RoomType, Room
from apps.hotels.serializers import (
    HotelSerializer,
    RoomTypeSerializer,
    RoomSerializer,
    RoomCreateSerializer,
)
from apps.hotels.permissions import IsAdminOrManagerOrReadOnly


class HotelViewSet(ViewSet):
    lookup_value_regex: str = r'\d+'
    permission_classes: list[BasePermission] = [IsAdminOrManagerOrReadOnly]

    @extend_schema(responses=HotelSerializer(many=True))
    def list(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        hotels: QuerySet[Hotel] = Hotel.objects.select_related('owner').all()
        serializer: HotelSerializer = HotelSerializer(hotels, many=True)
        return DRFResponse(serializer.data, status=HTTP_200_OK)

    @extend_schema(responses=HotelSerializer)
    def retrieve(self, request: DRFRequest, pk: int = None, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        hotel: Hotel = get_object_or_404(Hotel.objects.select_related('owner'), pk=pk)
        serializer: HotelSerializer = HotelSerializer(hotel)
        return DRFResponse(serializer.data, status=HTTP_200_OK)

    @extend_schema(request=HotelSerializer, responses=HotelSerializer)
    def create(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        serializer: HotelSerializer = HotelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return DRFResponse(serializer.data, status=HTTP_201_CREATED)
        return DRFResponse(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @extend_schema(request=HotelSerializer, responses=HotelSerializer)
    def update(self, request: DRFRequest, pk: int = None, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        hotel: Hotel = get_object_or_404(Hotel, pk=pk)
        self.check_object_permissions(request, hotel)
        serializer: HotelSerializer = HotelSerializer(hotel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return DRFResponse(serializer.data, status=HTTP_200_OK)
        return DRFResponse(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @extend_schema(request=HotelSerializer, responses=HotelSerializer)
    def partial_update(self, request: DRFRequest, pk: int = None, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        hotel: Hotel = get_object_or_404(Hotel, pk=pk)
        self.check_object_permissions(request, hotel)
        serializer: HotelSerializer = HotelSerializer(hotel, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return DRFResponse(serializer.data, status=HTTP_200_OK)
        return DRFResponse(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @extend_schema(responses=None)
    def destroy(self, request: DRFRequest, pk: int = None, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        hotel: Hotel = get_object_or_404(Hotel, pk=pk)
        self.check_object_permissions(request, hotel)
        hotel.delete()
        return DRFResponse(status=HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["get"])
    def rooms(self, request: DRFRequest, pk: int = None, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        hotel: Hotel = get_object_or_404(Hotel, pk=pk)
        rooms: QuerySet[Room] = Room.objects.filter(hotel=hotel)
        serializer: RoomSerializer = RoomSerializer(rooms, many=True)
        return DRFResponse(serializer.data, status=HTTP_200_OK)

    @extend_schema(request=RoomCreateSerializer, responses=RoomSerializer, description="Создает новую комнату и привязывает её к текущему отелю")
    @action(detail=True, methods=["post"], url_path='add-room')
    def add_room(self, request: DRFRequest, pk: int = None, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        hotel: Hotel = get_object_or_404(Hotel, pk=pk)
        self.check_object_permissions(request, hotel)
        serializer: RoomCreateSerializer = RoomCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(hotel=hotel)
            return DRFResponse(serializer.data, status=HTTP_201_CREATED)
        return DRFResponse(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @extend_schema(responses=HotelSerializer)
    @action(detail=False, methods=["get"], url_path="my-hotels")
    def my_hotels(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        queryset: QuerySet[Hotel] = Hotel.objects.filter(owner=request.user).all()
        serializer: HotelSerializer = HotelSerializer(queryset, many=True)
        return DRFResponse(serializer.data, status=HTTP_200_OK)


class RoomTypeViewSet(ViewSet):
    lookup_field = "pk"

    @extend_schema(responses=RoomTypeSerializer(many=True))
    def list(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        queryset: QuerySet[RoomType] = RoomType.objects.all()
        serializer: RoomTypeSerializer = RoomTypeSerializer(queryset, many=True)
        return DRFResponse(serializer.data, status=HTTP_200_OK)

    @extend_schema(request=RoomTypeSerializer, responses=RoomTypeSerializer)
    def create(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        serializer: RoomTypeSerializer = RoomTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return DRFResponse(serializer.data, status=HTTP_201_CREATED)
        return DRFResponse(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @extend_schema(request=RoomTypeSerializer, responses=RoomTypeSerializer)
    def partial_update(self, request: DRFRequest, pk: int = None, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        roomtype: RoomType = get_object_or_404(RoomType, pk=pk)
        serializer: RoomTypeSerializer = RoomTypeSerializer(roomtype, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return DRFResponse(serializer.data, status=HTTP_200_OK)
        return DRFResponse(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @extend_schema(responses=None)
    def destroy(self, request: DRFRequest, pk: int = None, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        roomtype: RoomType = get_object_or_404(RoomType, pk=pk)
        roomtype.delete()
        return DRFResponse(status=HTTP_204_NO_CONTENT)
