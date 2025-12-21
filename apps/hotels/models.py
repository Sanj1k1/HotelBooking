#Django modules
from django.db.models import (
    Model,
    CharField,
    IntegerField,
    TextField,
    BooleanField,
    ForeignKey,
    FloatField,
    CASCADE,
)
from django.core.validators import MinValueValidator,MaxValueValidator

#Python modules

#Project modules

class Hotel(Model):
    """
    Hotel database (table) model.
    """
    name = CharField(max_length=100)
    address = CharField(max_length=100)
    rating = IntegerField(default=3,validators=[MinValueValidator(1),MaxValueValidator(5)])
    description = TextField(blank=True, null=True)
    # Добавляем null=True и blank=True для существующих записей
    owner = ForeignKey('users.User', on_delete=CASCADE, related_name='hotels', null=True, blank=True)
    
    def __str__(self):
        return self.name


class RoomType(Model):
    """
    RoomType database (table) model.
    """
    name = CharField(max_length=50)
    capacity = IntegerField(validators=[MinValueValidator(1)])
    
    def __str__(self):
        return f"{self.name} до {self.capacity} человек"


class Room(Model):
    """
    Room database (table) model.
    """
    number = IntegerField()
    price_per_night = FloatField(validators=[MinValueValidator(3)])
    description = TextField(blank=True, null=True)
    is_available = BooleanField(default=True)
    hotel = ForeignKey(to=Hotel, on_delete=CASCADE)
    # ИСПРАВЛЯЕМ: RoomType -> room_type
    room_type = ForeignKey(to=RoomType, on_delete=CASCADE)
    
    class Meta:
        unique_together = ('hotel','number')
        
    def __str__(self):
        return f"Номер {self.number} - {self.hotel.name}"