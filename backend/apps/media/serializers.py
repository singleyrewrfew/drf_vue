from rest_framework import serializers
from django.conf import settings
from django.core.exceptions import ValidationError

from .models import Media


class MediaSerializer(serializers.ModelSerializer):
    url = serializers.ReadOnlyField()
    is_image = serializers.ReadOnlyField()
    is_video = serializers.ReadOnlyField()
    thumbnails_url = serializers.SerializerMethodField()
    thumbnail_status_display = serializers.CharField(source='get_thumbnail_status_display', read_only=True)
    uploader_name = serializers.CharField(source='uploader.username', read_only=True)
    has_reference = serializers.SerializerMethodField()

    class Meta:
        model = Media
        fields = ['id', 'file', 'url', 'filename', 'file_type', 'file_size', 'is_image', 'is_video', 'thumbnails_url', 'thumbnails_count', 'thumbnail_status', 'thumbnail_status_display', 'uploader', 'uploader_name', 'created_at', 'has_reference']
        read_only_fields = ['id', 'filename', 'file_type', 'file_size', 'file_hash', 'uploader', 'created_at']

    def get_thumbnails_url(self, obj):
        if obj.thumbnails:
            return obj.thumbnails.url
        return None

    def get_has_reference(self, obj):
        return obj.reference is not None


class MediaUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['file']

    def validate_file(self, value):
        # 验证文件大小（视频除外）
        max_size = getattr(settings, 'FILE_UPLOAD_MAX_MEMORY_SIZE', 10 * 1024 * 1024)  # 默认 10MB
        is_video = value.content_type.startswith('video/')
        
        if not is_video and value.size > max_size:
            max_size_mb = max_size / (1024 * 1024)
            raise serializers.ValidationError(f'文件大小不能超过 {max_size_mb:.0f}MB（视频文件不限大小）')

        # 验证文件类型
        allowed_types = getattr(settings, 'ALLOWED_FILE_TYPES', [])
        if allowed_types and value.content_type not in allowed_types:
            raise serializers.ValidationError(
                f'不支持的文件类型：{value.content_type}。'
                f'支持的类型：图片（jpg, png, gif, webp, svg）、视频（mp4, webm, ogg）、文档（pdf, doc, docx）'
            )

        # 验证文件扩展名
        import os
        ext = os.path.splitext(value.name)[1].lower()
        allowed_extensions = [
            '.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg',  # 图片
            '.mp4', '.webm', '.ogg', '.mov',  # 视频
            '.pdf', '.doc', '.docx',  # 文档
        ]
        if ext not in allowed_extensions:
            raise serializers.ValidationError(
                f'不支持的文件扩展名：{ext}。'
                f'支持的扩展名：{", ".join(allowed_extensions)}'
            )

        return value

    def create(self, validated_data):
        file = validated_data['file']
        uploader = self.context['request'].user
        media, created = Media.objects.get_or_create_by_file(file, uploader)
        if not created:
            media.filename = file.name
            media.save()
        
        if media.is_video:
            media.generate_thumbnails_async()
        
        return media
