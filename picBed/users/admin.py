from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'storage_used', 'storage_quota', 'is_active', 'created_at']
    list_filter = ['is_active', 'is_staff', 'created_at']
    search_fields = ['username', 'email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('username', 'email', 'password')
        }),
        ('个人信息', {
            'fields': ('avatar', 'bio')
        }),
        ('存储信息', {
            'fields': ('storage_quota', 'storage_used')
        }),
        ('权限信息', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at', 'last_login')
        }),
    )
