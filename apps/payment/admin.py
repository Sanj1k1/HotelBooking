
#Django modules
from django.contrib import admin

#Project modules
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Payment model.

    This class defines how Payment objects are displayed and managed
    in the Django admin interface.
    """
    list_display: tuple[str, ...] = (
        "user", 
        "amount", 
        "payment_method", 
        "status", 
        "created_at"
    )
    list_filter: tuple[str, ...] = (
        "status", 
        "payment_method"
    )
    search_fields: tuple[str, ...] = (
        "user__username",
    )
    ordering: tuple[str, ...] = (
        "-created_at",
    )


