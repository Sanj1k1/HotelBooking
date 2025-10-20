from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from typing import Any


class Payment(models.Model):
    """
    Represents a payment transaction made by a user.

    Attributes:
        user (User): The user who made the payment.
        amount (Decimal): The amount of the payment.
        payment_method (str): The method used for payment 
            (e.g., credit card, PayPal, or cash).
        status (str): The current status of the payment 
            (e.g., pending, completed, or failed).
        created_at (datetime): The timestamp when the payment was created.
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

    user: User = models.ForeignKey(User, on_delete=models.CASCADE)
    amount: Decimal = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method: str = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status: str = models.CharField(max_length=20, choices=STATUSES)
    created_at: Any = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Return a readable string representation of the payment."""
        return f"{self.user.username} - {self.amount} ({self.status})"
    
