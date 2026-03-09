from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'is_active', 'created_at']
    list_filter = ['role', 'is_active', 'created_at']
    search_fields = ['username', 'email']
    readonly_fields = ['id', 'created_at', 'updated_at']

    fieldsets = UserAdmin.fieldsets + (
        ('扩展信息', {'fields': ('id', 'avatar', 'role', 'created_at', 'updated_at')}),
    )
