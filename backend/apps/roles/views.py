from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

from apps.users.permissions import IsAdminUser
from utils.viewset_mixins import CachedListMixin
from .models import Permission, Role
from .serializers import PermissionSerializer, RoleListSerializer, RoleSerializer


@extend_schema_view(
    list=extend_schema(summary='列出权限', description='获取权限列表（需要管理员权限）'),
    retrieve=extend_schema(summary='获取权限详情', description='获取单个权限的详细信息'),
    create=extend_schema(summary='创建权限', description='创建新权限（需要管理员权限）'),
    update=extend_schema(summary='更新权限', description='更新权限信息（需要管理员权限）'),
    partial_update=extend_schema(summary='部分更新权限', description='部分更新权限（需要管理员权限）'),
    destroy=extend_schema(summary='删除权限', description='删除权限（需要管理员权限）'),
)
class PermissionViewSet(CachedListMixin, viewsets.ModelViewSet):
    cache_key_prefix = 'permissions:list'
    cache_timeout = settings.CACHE_TTL['PERMISSION_LIST']
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


@extend_schema_view(
    list=extend_schema(summary='列出角色', description='获取角色列表（需要管理员权限）'),
    retrieve=extend_schema(summary='获取角色详情', description='获取单个角色的详细信息'),
    create=extend_schema(summary='创建角色', description='创建新角色（需要管理员权限）'),
    update=extend_schema(summary='更新角色', description='更新角色信息（需要管理员权限）'),
    partial_update=extend_schema(summary='部分更新角色', description='部分更新角色（需要管理员权限）'),
    destroy=extend_schema(summary='删除角色', description='删除角色（需要管理员权限）'),
)
class RoleViewSet(CachedListMixin, viewsets.ModelViewSet):
    cache_key_prefix = 'roles:list'
    cache_timeout = settings.CACHE_TTL['ROLE_LIST']
    queryset = Role.objects.prefetch_related('permissions')
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'list':
            return RoleListSerializer
        return RoleSerializer
