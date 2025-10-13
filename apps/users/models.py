#Python modules + Third party modules

#Djago modules
from django.db.models import Model,CharField,ManyToManyField
from django.contrib.auth.models import AbstractUser,Group,Permission

class User(AbstractUser):
    """
    User database (table) model.
    """
    FIRSTLASTNAMES_MAX_LENGTH = 100
    first_name = CharField(max_length=FIRSTLASTNAMES_MAX_LENGTH,blank=False)
    last_name = CharField(max_length=FIRSTLASTNAMES_MAX_LENGTH,blank=False)
    email = CharField(max_length=50,unique=True,blank=False)
    phone = CharField(max_length=50,blank=False)
    groups = ManyToManyField(
        Group,
        related_name="custom_user_groups",  
        blank=True
    )
    user_permissions = ManyToManyField(
        Permission,
        related_name="custom_user_permissions", 
        blank=True
    )
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"