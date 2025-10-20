#Python modules + Third party modules

#Djago modules
from django.db.models import Model,CharField
from django.contrib.auth.models import AbstractUser

#Project modules

class User(AbstractUser):
    """
    User database (table) model.
    """
    ROLE_CUSTOMER = "customer"
    ROLE_ADMIN = "admin"
    ROLE_CHOICES = (
        (ROLE_ADMIN,"Admin"),
        (ROLE_CUSTOMER,"Customer"),
    )
    FIRSTLASTNAMES_MAX_LENGTH = 100
    first_name = CharField(max_length=FIRSTLASTNAMES_MAX_LENGTH,blank=False)
    last_name = CharField(max_length=FIRSTLASTNAMES_MAX_LENGTH,blank=False)
    email = CharField(max_length=50,unique=True,blank=False)
    phone = CharField(max_length=50,blank=False)
    role = CharField(max_length=20,choices=ROLE_CHOICES,default=ROLE_CUSTOMER)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"