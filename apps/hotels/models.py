#Python modules + Third party modules

#Djago modules
from django.db.models import (
    Model,
    CharField,
    IntegerField,
    TextField,
    BooleanField,
    ForeignKey,
    CASCADE,
    )

# Create your models here.
class Hotel(Model):
    """
    Hotel database (table) model.
    """
    name = CharField(max_length=100)
    address = CharField(max_length=100)
    rating = IntegerField()
    
class RoomType(Model):
    """
    RoomType database (table) model.
    """
    name = CharField(max_length=50)
    capacity = IntegerField()
    
class Room(Model):
    """
    Room database (table) model.
    """
    number = IntegerField(unique=True)
    price_per_night = IntegerField()
    description = TextField()
    is_available = BooleanField(default = True)
    hotel = ForeignKey(to=Hotel,on_delete=CASCADE)
    RoomType = ForeignKey(to=RoomType,on_delete=CASCADE)
    