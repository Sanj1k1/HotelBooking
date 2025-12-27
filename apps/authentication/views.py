#DRF modules
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

#Django modules
from django.contrib.auth import get_user_model

#Project modules
from .serializers import RegisterSerializer

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer to use phone instead of username for authentication.
    """
    username_field = 'phone'
    
    def validate(self, attrs):
        """
        Override validate method to use phone field.
        """
        # Use phone as username
        attrs['username'] = attrs.get('phone')
        return super().validate(attrs)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view to use phone instead of username for authentication.
    """
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    """
    View for user registration.
    """
    serializer_class = RegisterSerializer
    permission_classes = []  # Allow anyone to register
    
    def create(self, request, *args, **kwargs):
        """Handle user registration and return user data without sensitive information."""
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Return user data without password
        return Response({
            'user': {
                'id': user.id,
                'phone': user.phone,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
            },
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)