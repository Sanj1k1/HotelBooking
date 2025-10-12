#Python modules + Third party modules

#Django modules
from unfold.admin import ModelAdmin
from django.contrib.admin import register
from django.db import models
from unfold.contrib.forms.widgets import WysiwygWidget

#Project modules
from apps.hotels.models import Hotel,Room,RoomType

@register(Room)
class RoomAdmin(ModelAdmin):
    """
    """
    list_display = (
        'id',
        'number',
        'description',
        'is_available',
    )
    
    list_per_page = 50
    
    formfield_overrides = {
        models.TextField: {
            "widget":WysiwygWidget
        }
    }
    
    search_fields = (
        "id",
        "number",
    )
    
    
@register(RoomType)
class RoomTypeAdmin(ModelAdmin):
    """
    """
    list_display = (
        'id',
        'name',
        'capacity',
    )
    
    list_per_page = 20
    
    search_fields = (
        "id",
        "capacity",
    )
    
@register(Hotel)
class HotelAdmin(ModelAdmin):
    """
    """
    list_display = (
        "id",
        "address",
    )
    
    list_per_page = 20
    
    search_fields = (
        "address",
    )