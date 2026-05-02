from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

from apps.users.permissions import IsAdminUser
from utils.viewset_mixins import CachedListMixin
from .models import Permission, Role
from .serializers import PermissionSerializer, RoleListSerializer, RoleSerializer


class PermissionViewSet(CachedListMixin, viewsets.ModelViewSet):
    cache_key_prefix = 'permissions:list'
    cache_timeout = settings.CACHE_TTL['PERMISSION_LIST']
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class RoleViewSet(CachedListMixin, viewsets.ModelViewSet):
    cache_key_prefix = 'roles:list'
    cache_timeout = settings.CACHE_TTL['ROLE_LIST']
    queryset = Role.objects.prefetch_related('permissions')
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'list':
            return RoleListSerializer
        return RoleSerializer
