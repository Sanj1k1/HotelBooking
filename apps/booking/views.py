#DRF modules
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

#Project modules
from apps.booking.models import Booking
from apps.booking.serializers import BookingSerializer

class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)