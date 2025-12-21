#Python modules + Third party modules

#Django modules
from django.db.models import Model,CharField,EmailField
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

#Project modules

class CustomUserManager(BaseUserManager):
    """Custom manager for User model with phone as username field."""
    
    def create_user(self, phone, email, password=None, **extra_fields):
        """Create and save a regular User with the given phone and password."""
        if not phone:
            raise ValueError(_('The Phone field must be set'))
        
        email = self.normalize_email(email)
        user = self.model(phone=phone, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given phone and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', self.model.ROLE_ADMIN)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(phone, email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User database (table) model with phone as username field.
    """
    ROLE_CUSTOMER = "customer"
    ROLE_ADMIN = "admin"
    ROLE_MANAGER = "manager"
    
    ROLE_CHOICES = (
        (ROLE_ADMIN, "Admin"),
        (ROLE_MANAGER, "Manager"),
        (ROLE_CUSTOMER, "Customer"),
    )
    
    FIRSTLASTNAMES_MAX_LENGTH = 100
    
    # Убираем username, используем phone вместо него
    username = None
    # Делаем phone уникальным и используем для аутентификации
    phone = CharField(
        max_length=20, 
        unique=True,
        blank=False,
        verbose_name=_("Phone Number")
    )
    
    # Остальные поля
    first_name = CharField(max_length=FIRSTLASTNAMES_MAX_LENGTH, blank=False)
    last_name = CharField(max_length=FIRSTLASTNAMES_MAX_LENGTH, blank=False)
    email = EmailField(max_length=50, unique=True, blank=False)
    role = CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_CUSTOMER)
    
    # Указываем, что поле для аутентификации - phone
    USERNAME_FIELD = 'phone'
    # Обязательные поля при создании суперпользователя
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    
    # Используем кастомный менеджер
    objects = CustomUserManager()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone})"