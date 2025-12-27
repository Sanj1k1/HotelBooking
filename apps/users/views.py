#Python modules
from typing import Any
from drf_spectacular.utils import extend_schema

# DRF modules
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.decorators import action


# Django modules
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.contrib.auth.models import User

# Project modules
from apps.users.serializers import UserSerializer
from apps.users.permissions import IsSelfOrAdmin

User = get_user_model()


class UserViewSet(ViewSet):
    """
    User ViewSet for managing users.
    Only admin can list all users, users can see only themselves.
    """
    permission_classes: list[BasePermission] = [IsSelfOrAdmin]

    @extend_schema(responses=UserSerializer(many=True))
    def list(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        GET /api/users/ - List users
        Only admin can see everyone
        """
        user: User = request.user

        if user.role == User.ROLE_ADMIN:
            queryset: QuerySet[User] = User.objects.all()
        else:
            queryset: QuerySet[User] = User.objects.filter(id=user.id)

        serializer: UserSerializer = UserSerializer(queryset, many=True)
        return DRFResponse(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(responses=UserSerializer)
    def retrieve(self, request: DRFRequest, pk: int = None, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        GET /api/users/{id}/ - Get user details
        """
        user: User = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)

        serializer: UserSerializer = UserSerializer(user)
        return DRFResponse(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=UserSerializer, responses=UserSerializer)
    def update(self, request: DRFRequest, pk: int = None, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        PUT /api/users/{id}/ - Update user (full update)
        """
        user: User = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)

        serializer: UserSerializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return DRFResponse(serializer.data, status=status.HTTP_200_OK)
        return DRFResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=UserSerializer, responses=UserSerializer)
    def partial_update(self, request: DRFRequest, pk: int = None, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        PATCH /api/users/{id}/ - Partial update user
        """
        user: User = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)

        serializer: UserSerializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return DRFResponse(serializer.data, status=status.HTTP_200_OK)
        return DRFResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses=None)
    def destroy(self, request: DRFRequest, pk: int = None, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        DELETE /api/users/{id}/ - Delete user
        Only admin or self can delete
        """
        user: User = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        user.delete()
        return DRFResponse(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(responses=UserSerializer)
    @action(detail=False, methods=['get'])
    def me(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        GET /api/users/me/ - Get current user profile
        """
        serializer: UserSerializer = UserSerializer(request.user)
        return DRFResponse(serializer.data, status=status.HTTP_200_OK)
