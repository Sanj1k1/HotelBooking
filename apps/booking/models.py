#Python Modules

#Django Modules
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
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
    
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE,related_name='bookings')
    check_in = models.DateField(default=timezone.now)
    check_out = models.DateField()
    total_price = models.IntegerField(default=0,validators=[MinValueValidator(0)])
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default=PENDING
    )
    
    payment = models.ForeignKey(
        'payment.Payment', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='bookings'
    )

    def __str__(self):
        return f"Booking {self.id} by {self.user}"