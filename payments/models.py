from django.db import models
from bookings.models import Booking

class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    provider = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="pending")
    transaction_id = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
