from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()


class IsAdminOrSelf(permissions.BasePermission):
    """
    Custom permission: only admin or user themselves can access.
    """
    def has_object_permission(self, request, view, obj):
        # Admin can do anything
        if request.user.is_staff:
            return True
        
        # User can only access their own data
        return obj == request.user


class UserViewSet(viewsets.ModelViewSet):
    """
    User ViewSet for managing users.
    Only admin can list all users, users can see only themselves.
    """
    queryset = User.objects.all()  # Users usually don't need select_related
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSelf]
    
    def get_queryset(self):
        """
        Non-admin users can only see themselves.
        """
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=user.id)
    
    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        """
        Get or update current user profile.
        """
        user = request.user
        
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        
        elif request.method in ['PUT', 'PATCH']:
            serializer = self.get_serializer(
                user, 
                data=request.data, 
                partial=request.method == 'PATCH'
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    
    # Отключаем стандартные create/update/delete для non-admin
    def create(self, request, *args, **kwargs):
        # Создание пользователей через /api/auth/register/
        return Response(
            {'detail': 'Method "POST" not allowed. Use /api/auth/register/'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    def destroy(self, request, *args, **kwargs):
        # Удаление только для админов
        if not request.user.is_staff:
            return Response(
                {'detail': 'You do not have permission to perform this action.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)