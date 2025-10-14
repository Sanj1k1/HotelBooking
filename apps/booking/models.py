from django.db import models
from django.utils import timezone


# class User(models.Model):
#     """
#     Represents a user who can book rooms.

#     Attributes:
#         first_name (str): The user's first name.
#         last_name (str): The user's last name.
#         email (str): The user's unique email address.
#         phone (str): The user's phone number.
#     """
#     first_name: str = models.CharField(max_length=100)
#     last_name: str = models.CharField(max_length=100)
#     email: str = models.EmailField(unique=True)
#     phone: str = models.CharField(max_length=20)

#     def __str__(self) -> str:
#         """Return the user's full name."""
#         return f"{self.first_name} {self.last_name}"


# class Room(models.Model):
#     """
#     Represents a hotel room that can be booked.

#     Attributes:
#         number (int): The room number (unique).
#         price_per_night (int): Price per night for the room.
#         description (str): Description of the room.
#         is_available (bool): Availability status of the room.
#     """
#     number: int = models.IntegerField(unique=True)
#     price_per_night: int = models.IntegerField()
#     description: str = models.TextField()
#     is_available: bool = models.BooleanField(default=True)

#     def __str__(self) -> str:
#         """Return the room number as a string."""
#         return f"Room {self.number}"


class Booking(models.Model):
    """
    Represents a booking made by a user for a room.

    Attributes:
        user (User): The user who made the booking.
        room (Room): The booked room.
        check_in (date): The check-in date.
        check_out (date): The check-out date.
        total_price (int): Total price for the stay.
        status (str): The booking status (e.g., Pending, Confirmed).
    """
    user: User = models.ForeignKey(User, on_delete=models.CASCADE)
    room: Room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in: timezone.datetime = models.DateField(default=timezone.now)
    check_out: timezone.datetime = models.DateField()
    total_price: int = models.IntegerField()
    status: str = models.CharField(max_length=200, default="Pending")

    def __str__(self) -> str:
        """Return a string representation of the booking."""
        return f"Booking {self.id} by {self.user}"
