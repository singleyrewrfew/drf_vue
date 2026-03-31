from django.contrib import admin
from .models import Image, Album, UploadChunk


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'is_public', 'image_count', 'created_at']
    list_filter = ['is_public', 'created_at']
    search_fields = ['name', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    
    def image_count(self, obj):
        return obj.image_count
    image_count.short_description = '图片数量'


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['filename', 'user', 'album', 'file_size', 'format', 'width', 'height', 'is_public', 'access_count', 'created_at']
    list_filter = ['format', 'is_public', 'storage_backend', 'created_at']
    search_fields = ['filename', 'title', 'user__username', 'album__name']
    readonly_fields = ['file_hash', 'file_size', 'width', 'height', 'format', 'access_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('user', 'album', 'file', 'filename', 'file_hash')
        }),
        ('文件信息', {
            'fields': ('file_size', 'width', 'height', 'format', 'storage_backend', 'storage_path')
        }),
        ('描述信息', {
            'fields': ('title', 'description', 'tags')
        }),
        ('访问控制', {
            'fields': ('is_public', 'access_count')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(UploadChunk)
class UploadChunkAdmin(admin.ModelAdmin):
    list_display = ['upload_id', 'chunk_number', 'total_chunks', 'filename', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['upload_id', 'filename', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
