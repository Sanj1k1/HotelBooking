from django.db import models
from django.utils import timezone

# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Room(models.Model):
    number = models.IntegerField(unique=True)
    price_per_night = models.IntegerField()
    description = models.TextField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Room {self.number}"
    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField(default=timezone.now)
    check_out = models.DateField()
    total_price = models.IntegerField()
    status = models.CharField(max_length=200, default='Pending')

    def __str__(self):
        return f"Booking {self.id} by {self.user}"