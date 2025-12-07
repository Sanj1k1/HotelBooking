from django.apps import AppConfig


class PaymentConfig(AppConfig):
    """
    Configuration class for the Payment application.

    This class defines metadata for the 'apps.payment' app,
    such as its name and default settings for auto-created primary keys.
    """

    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'apps.payment'
