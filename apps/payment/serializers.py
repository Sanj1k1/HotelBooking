#DRF modules
from rest_framework.serializers import ModelSerializer

#Project modules
from apps.payment.models import Payment

class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        