from django.contrib import admin
from .models import User, Room, Booking


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Django admin configuration for the User model.

    Defines how user records are displayed, searched, and paginated
    within the Django admin interface.
    """

    list_display: tuple[str, ...] = (
        "id",
        "first_name",
        "last_name",
        "email",
        "phone",
    )

    list_display_links: tuple[str, ...] = (
        "id",
        "first_name",
    )

    search_fields: tuple[str, ...] = (
        "first_name",
        "last_name",
        "email",
        "phone",
    )

    list_per_page: int = 50


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """
    Django admin configuration for the Room model.

    Controls how hotel room data (number, price, and availability)
    is displayed and managed through the Django admin panel.
    """

    list_display: tuple[str, ...] = (
        "id",
        "number",
        "price_per_night",
        "is_available",
    )

    list_display_links: tuple[str, ...] = (
        "id",
        "number",
    )

    list_filter: tuple[str, ...] = (
        "is_available",
    )

    search_fields: tuple[str, ...] = (
        "number",
        "description",
    )

    list_per_page: int = 50


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
