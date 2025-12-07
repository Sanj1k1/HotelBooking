#Python modules
from typing import Any
from datetime import datetime, timedelta
from random import choice, randint

#Django modules
from django.core.management.base import BaseCommand
from django.db.models import QuerySet
from django.utils import timezone
from django.db import connection

#Project modules
from apps.booking.models import Booking
from apps.users.models import User
from apps.hotels.models import Hotel, Room


class Command(BaseCommand):
    help = "Generate booking data for testing purposes."
    
    def reset_booking_id_sequence(self):
        """Сброс автоинкремента ID (SQLite)."""
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='booking_booking';")
        self.stdout.write(self.style.WARNING("Booking ID sequence reset."))
    
    def __clear_bookings(self):
        """Очистка всех бронирований и сброс ID."""
        Booking.objects.all().delete()
        self.reset_booking_id_sequence()
        self.stdout.write(self.style.WARNING("All bookings deleted."))
        
    def __generate_booking(self) -> None:
        # Очистка таблицы и сброс ID
        Booking.objects.all().delete()
        self.reset_booking_id_sequence()

        created_booking: list[Booking] = []
        booking_before = Booking.objects.count()
        all_users: QuerySet[User] = User.objects.all()
        existing_hotel: Hotel = Hotel.objects.first()
        all_rooms: QuerySet[Room] = Room.objects.filter(hotel=existing_hotel)

        for user in all_users:
            room = choice(all_rooms)
            check_in = timezone.now().date() + timedelta(days=randint(0, 10))
            check_out = check_in + timedelta(days=randint(1, 5))
            total_price = (check_out - check_in).days * room.price_per_night

            created_booking.append(
                Booking(
                    user=user,
                    room=room,
                    check_in=check_in,
                    check_out=check_out,
                    total_price=total_price,
                    status="Confirmed",
                )
            )

        Booking.objects.bulk_create(created_booking)
        booking_after = Booking.objects.count()

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {booking_after - booking_before} new bookings."
            )
        )

    def handle(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        start_time = datetime.now()
        self.__generate_booking()
        self.stdout.write(
            f"The whole process took {(datetime.now() - start_time).total_seconds()} seconds."
        )
