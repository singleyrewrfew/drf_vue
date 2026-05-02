from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.users.permissions import IsAdminUser
from utils.cache_utils import get_cache_key
from .models import Permission, Role
from .serializers import PermissionSerializer, RoleListSerializer, RoleSerializer


CACHE_KEY_ROLES = 'roles:list'
CACHE_KEY_PERMISSIONS = 'permissions:list'


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def list(self, request, *args, **kwargs):
        cache_key = get_cache_key(CACHE_KEY_PERMISSIONS)
        cached_data = cache.get(cache_key)
        if cached_data:
            from utils.response import StandardResponse
            return StandardResponse(cached_data)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, 300)
        return response


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.prefetch_related('permissions')
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'list':
            return RoleListSerializer
        return RoleSerializer

    def list(self, request, *args, **kwargs):
        cache_key = get_cache_key(CACHE_KEY_ROLES)
        cached_data = cache.get(cache_key)
        if cached_data:
            from utils.response import StandardResponse
            return StandardResponse(cached_data)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, 300)
        return response

    def perform_create(self, serializer):
        serializer.save()
        cache.delete(get_cache_key(CACHE_KEY_ROLES))

    def perform_update(self, serializer):
        serializer.save()
        cache.delete(get_cache_key(CACHE_KEY_ROLES))

    def perform_destroy(self, instance):
        instance.delete()
        cache.delete(get_cache_key(CACHE_KEY_ROLES))
