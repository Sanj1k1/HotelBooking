#DRF modules
from rest_framework import serializers

#Django modules
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration with password validation and role assignment."""
    
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    
    role = serializers.ChoiceField(
        choices=User.ROLE_CHOICES,
        default=User.ROLE_CUSTOMER,
        required=False,
        write_only=True 
    )

    class Meta:
        model = User
        fields = ('phone', 'email', 'first_name', 'last_name', 'password', 'password2', 'role')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
        }

    def validate(self, attrs):
        """Validate that both password fields match."""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields don't match."}
            )
        return attrs

    def create(self, validated_data):
        """Create a new user instance with the validated data."""
        validated_data.pop('password2')
        
        # Получаем роль или используем дефолтную
        role = validated_data.pop('role', User.ROLE_CUSTOMER)
        
        user = User.objects.create_user(
            phone=validated_data['phone'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            role=role  # передаем выбранную роль
        )
        
        return user