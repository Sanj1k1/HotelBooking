# DRF modules
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema

# Django modules
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

# Project modules
from .serializers import UserSerializer
from .permissions import IsSelfOrAdmin 

User = get_user_model()


class UserViewSet(ViewSet):
    """
    User ViewSet for managing users.
    Only admin can list all users, users can see only themselves.
    """
    permission_classes = [IsSelfOrAdmin]
    
    @extend_schema(responses=UserSerializer(many=True))
    def list(self, request):
        """
        GET /api/users/ - List users
        Admin: all users, Others: only themselves
        """
        user = request.user
        
        if user.role == User.ROLE_ADMIN:
            queryset = User.objects.all()
        else:
            queryset = User.objects.filter(id=user.id)
        
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @extend_schema(responses=UserSerializer)
    def retrieve(self, request, pk=None):
        """
        GET /api/users/{id}/ - Get user details
        """
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    @extend_schema(request=UserSerializer, responses=UserSerializer)
    def update(self, request, pk=None):
        """
        PUT /api/users/{id}/ - Update user (full update)
        """
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(request=UserSerializer, responses=UserSerializer)
    def partial_update(self, request, pk=None):
        """
        PATCH /api/users/{id}/ - Partial update user
        """
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(responses=None)
    def destroy(self, request, pk=None):
        """
        DELETE /api/users/{id}/ - Delete user
        Only admin or self can delete
        """
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @extend_schema(responses=UserSerializer)
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        GET /api/users/me/ - Get current user profile
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)