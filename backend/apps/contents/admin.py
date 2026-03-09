from django.contrib import admin

from .models import Content


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'view_count', 'is_top', 'created_at']
    list_filter = ['status', 'category', 'is_top', 'created_at']
    search_fields = ['title', 'summary', 'content']
    raw_id_fields = ['author', 'category']
    filter_horizontal = ['tags']
    prepopulated_fields = {'slug': ('title',)}
