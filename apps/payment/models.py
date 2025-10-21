#Project Modules
from decimal import Decimal
from typing import Any

#Django modules
from django.db import models

#Project Modules
from apps.users.models import User

class Payment(models.Model):
    """
    Represents a payment transaction made by a user.
    """

    PAYMENT_METHODS: list[tuple[str, str]] = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('cash', 'Cash'),
    ]

    STATUSES: list[tuple[str, str]] = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method= models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=STATUSES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Return a readable string representation of the payment."""
        return f"{self.user.username} - {self.amount} ({self.status})"
    
