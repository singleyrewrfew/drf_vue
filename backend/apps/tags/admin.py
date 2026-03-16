from django.contrib import admin
from .models import Tag

# 注册标签模型到 Django 管理后台
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    标签管理后台配置
    
    功能：
    - 自定义列表显示字段
    - 自定义搜索字段
    - 自动填充 slug 字段
    """
    # 列表页显示的字段
    list_display = ['name', 'slug', 'created_at']
    # 列表页的搜索字段
    search_fields = ['name', 'slug']
    # 自动填充：根据 name 字段自动填充 slug
    prepopulated_fields = {'slug': ('name',)}
