from rest_framework import serializers
from django.conf import settings
from django.core.exceptions import ValidationError
import hashlib
import logging
import os
import shutil

from .models import Media

logger = logging.getLogger(__name__)


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
        
        # 检查磁盘空间
        try:
            media_root = settings.MEDIA_ROOT
            if os.path.exists(media_root):
                stat = shutil.disk_usage(media_root)
                free_space = stat.free
                
                # 预留 100MB 安全空间
                if free_space < (value.size + 100 * 1024 * 1024):
                    logger.error(f"Insufficient disk space: free={free_space}, need={value.size}")
                    raise serializers.ValidationError('服务器存储空间不足，无法上传文件')
        except Exception as e:
            logger.warning(f"Failed to check disk space: {e}")
            # 如果检查失败，继续上传但不保证成功

        return value

    def create(self, validated_data):
        """
        创建媒体记录并验证文件完整性
        
        参数:
            validated_data: 已验证的数据字典
        
        返回:
            Media: 创建的媒体对象
        
        异常:
            serializers.ValidationError: 当文件完整性校验失败时
        """
        import os
        from django.db import transaction
        
        file = validated_data['file']
        uploader = self.context['request'].user
        temp_file_path = None
        
        try:
            # 预先计算文件哈希值
            file.seek(0)
            expected_hash = hashlib.md5(file.read()).hexdigest()
            file.seek(0)
            
            # 保存临时文件路径（用于失败时清理）
            if hasattr(file, 'temporary_file_path'):
                temp_file_path = file.temporary_file_path()
            
            with transaction.atomic():
                # 使用 get_or_create_by_file 方法（会自动处理去重）
                media, created = Media.objects.get_or_create_by_file(file, uploader)
                
                if not created:
                    # 如果是重复文件，更新文件名
                    media.filename = file.name
                    media.save(update_fields=['filename'])
                
                # 验证文件完整性（仅针对新上传的文件）
                if created and media.file:
                    media.file.seek(0)
                    actual_hash = hashlib.md5(media.file.read()).hexdigest()
                    
                    if actual_hash != expected_hash:
                        # 文件损坏，删除数据库记录（事务会自动回滚）
                        logger.error(f"File integrity check failed: expected={expected_hash}, actual={actual_hash}")
                        raise serializers.ValidationError('文件上传过程中损坏，请重新上传')
                
                # 如果是视频，异步生成缩略图
                if media.is_video:
                    media.generate_thumbnails_async()
                
                logger.info(f"Media uploaded successfully: {media.id}, filename={media.filename}")
                return media
                
        except serializers.ValidationError:
            # 验证错误，重新抛出让事务回滚
            raise
        except Exception as e:
            # 其他异常，记录日志并转换为友好的错误消息
            logger.error(f"Failed to upload media: {type(e).__name__}: {e}", exc_info=True)
            
            # 尝试清理临时文件
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.remove(temp_file_path)
                    logger.info(f"Cleaned up temp file: {temp_file_path}")
                except Exception as cleanup_error:
                    logger.error(f"Failed to cleanup temp file: {cleanup_error}")
            
            raise serializers.ValidationError('文件上传失败，请稍后重试')
