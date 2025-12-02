from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer for safe data exposure.
    """
    class Meta:
        model = User
        fields = ('id', 'phone', 'email', 'first_name', 'last_name', 'role', 'date_joined')
        read_only_fields = ('id', 'date_joined', 'role')