from django.contrib import admin
from apps.core.models import User

from .models import Permission, Role


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'description', 'created_at']
    search_fields = ['code', 'name']
    ordering = ['code']


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_system', 'permission_count', 'created_at']
    list_filter = ['is_system', 'created_at']
    search_fields = ['name', 'code']
    filter_horizontal = ['permissions']
    ordering = ['name']

    def permission_count(self, obj):
        return obj.permissions.count()
    permission_count.short_description = '权限数量'
