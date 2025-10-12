#Python modules + Third party modules

#Django modules
from unfold.admin import ModelAdmin
from django.contrib.admin import register
from django.db import models

#Project modules
from apps.users.models import User

@register(User)
class UserAdmin(ModelAdmin):
    """
    User admin configuration class.
    """
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "phone",
    )
    
    list_per_page = 20