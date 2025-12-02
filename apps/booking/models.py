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
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (CANCELLED, 'Cancelled'),
        (COMPLETED, 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField(default=timezone.now)
    check_out = models.DateField()
    total_price = models.IntegerField()
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default=PENDING
    )

    def __str__(self):
        return f"Booking {self.id} by {self.user}"