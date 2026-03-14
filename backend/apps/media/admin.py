from django.contrib import admin

from .models import Media


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ['filename', 'file_type', 'file_size', 'uploader', 'created_at']
    list_filter = ['file_type', 'created_at']
    search_fields = ['filename']
    raw_id_fields = ['uploader']
