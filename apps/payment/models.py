from decimal import Decimal
from django.db import models
from apps.users.models import User
from apps.booking.models import Booking


class Payment(models.Model):
    """
    Represents a payment transaction for a booking.
    """

    PAYMENT_METHODS = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
    ]

    STATUSES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    # Меняем на OneToOneField для связи 1:1 с Booking
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name='payment_link',  # Изменяем related_name чтобы не конфликтовать
        null=True,  # Временно для миграции
        blank=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=STATUSES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.booking:
            return f"Payment {self.id} for Booking {self.booking.id} - {self.amount} ({self.status})"
        return f"Payment {self.id} - {self.amount} ({self.status})"
    
    def save(self, *args, **kwargs):
        """Auto-update booking status when payment is completed."""
        if self.booking and self.status == 'completed' and self.booking.status == 'pending':
            self.booking.status = 'confirmed'
            self.booking.save()
        
        # Автоматически связываем payment с booking если booking указан
        if self.booking and not self.booking.payment:
            self.booking.payment = self
            self.booking.save()
            
        super().save(*args, **kwargs)