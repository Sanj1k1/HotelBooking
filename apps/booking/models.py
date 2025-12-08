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
    payment = models.OneToOneField(
        'payment.Payment',  # Ссылка на Payment модель
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='booking_payment'
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Можно добавить для отслеживания
    updated_at = models.DateTimeField(auto_now=True)      

    def __str__(self):
        return f"Booking {self.id} by {self.user}"
    
    def save(self, *args, **kwargs):
        """Можно добавить логику при сохранении"""
        # Например, автоматически рассчитывать total_price если не указан
        if not self.total_price and self.room and self.check_in and self.check_out:
            nights = (self.check_out - self.check_in).days
            self.total_price = self.room.price_per_night * nights
        super().save(*args, **kwargs)