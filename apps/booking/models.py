#Python Modules

#Django Modules
from django.db import models
from django.utils import timezone

#Project Modules
from apps.users.models import User
from apps.hotels.models import Room


class Booking(models.Model):
    """
    Represents a booking made by a user for a room.
    """
    user: User = models.ForeignKey(User, on_delete=models.CASCADE)
    room: Room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in: timezone.datetime = models.DateField(default=timezone.now)
    check_out: timezone.datetime = models.DateField()
    total_price: int = models.IntegerField()
    status: str = models.CharField(max_length=200, default="Pending")

    def __str__(self) -> str:
        """Return a string representation of the booking."""
        return f"Booking {self.id} by {self.user}"
