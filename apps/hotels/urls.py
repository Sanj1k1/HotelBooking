from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HotelViewSet, RoomTypeViewSet, RoomViewSet

router = DefaultRouter()
router.register(r'hotels', HotelViewSet, basename='hotel')
router.register(r'room-types', RoomTypeViewSet, basename='roomtype')
router.register(r'rooms', RoomViewSet, basename='room')

urlpatterns = [
    path('', include(router.urls)),
]