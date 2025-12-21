from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HotelViewSet, RoomTypeViewSet

router = DefaultRouter()
router.register(r'hotels', HotelViewSet, basename='hotel')
router.register(r'room-type', RoomTypeViewSet, basename='roomtype')

urlpatterns = [
    path('', include(router.urls)),
]