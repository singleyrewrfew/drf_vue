from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# 注册自定义用户模型到 Django 管理后台
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    自定义用户管理后台配置
    
    功能：
    - 自定义列表显示字段
    - 自定义过滤器
    - 自定义搜索字段
    - 自定义只读字段
    - 自定义字段分组
    """
    # 列表页显示的字段
    list_display = ['username', 'email', 'role', 'is_active', 'created_at']
    # 列表页的过滤器
    list_filter = ['role', 'is_active', 'created_at']
    # 列表页的搜索字段
    search_fields = ['username', 'email']
    # 只读字段（不可编辑）
    readonly_fields = ['id', 'created_at', 'updated_at']
    # 字段分组：将相关字段分组显示
    fieldsets = UserAdmin.fieldsets + (
        ('扩展信息', {'fields': ('id', 'avatar', 'role', 'created_at', 'updated_at')}),
    )
