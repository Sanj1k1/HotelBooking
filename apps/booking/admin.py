#Python Modules

#Django Modules
from django.contrib import admin

#Project Modules
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Django admin configuration for the Booking model.

    Displays and manages hotel room bookings with user, room,
    date, and total price details.
    """

    list_display: tuple[str, ...] = (
        "id",
        "user",
        "room",
        "check_in",
        "check_out",
        "total_price",
        "status",
    )

    list_display_links: tuple[str, ...] = (
        "id",
        "user",
    )

    list_filter: tuple[str, ...] = (
        "status",
        "check_in",
        "check_out",
    )

    search_fields: tuple[str, ...] = (
        "user__first_name",
        "user__last_name",
        "room__number",
    )

    date_hierarchy: str = "check_in"
    list_per_page: int = 50