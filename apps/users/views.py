#DRF modules
from rest_framework.viewsets import ModelViewSet 
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

#Django modules
from django.contrib.auth import get_user_model

#Python modules

#Project modules
from apps.users.serializers import UserSerializer
from apps.users.permissions import IsSelfOrAdmin

User = get_user_model()


class UserViewSet(ModelViewSet):
    """
    User ViewSet for managing users.
    Only admin can list all users, users can see only themselves.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,IsSelfOrAdmin]
    
    def get_queryset(self):
        """
        Non-admin users can only see themselves.
        """
        user = self.request.user
        if user.role==User.ROLE_ADMIN:
            return User.objects.all()
        
        return User.objects.filter(id=user.id)