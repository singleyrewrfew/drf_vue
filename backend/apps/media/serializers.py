import hashlib
import logging
import os
import shutil

from django.conf import settings
from rest_framework import serializers

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
            
            # SQLite 并发写入重试机制
            import time
            max_retries = 5
            for attempt in range(max_retries):
                try:
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
                                logger.error(f"File integrity check failed: expected={expected_hash}, actual={actual_hash}")
                                raise serializers.ValidationError('文件上传过程中损坏，请重新上传')
                        
                        logger.info(f"Media uploaded successfully: {media.id}, filename={media.filename}")
                        return media
                        
                except Exception as db_error:
                    if 'database is locked' in str(db_error).lower() and attempt < max_retries - 1:
                        wait_time = 1.0 * (attempt + 1)  # 递增延迟：1s, 2s, 3s, 4s
                        logger.warning(f"Database locked, retrying in {wait_time}s... (attempt {attempt + 1}/{max_retries})")
                        time.sleep(wait_time)
                        continue
                    raise
                
        except serializers.ValidationError:
            # 验证错误，重新抛出让事务回滚
            raise
        except Exception as e:
            # 其他异常，记录日志并转换为友好的错误消息
            logger.error(f"Failed to upload media: {type(e).__name__}: {e}", exc_info=True)
            logger.error(f"File info: name={file.name if file else 'None'}, size={file.size if file else 'None'}, type={file.content_type if hasattr(file, 'content_type') else 'Unknown'}")
            
            # 尝试清理临时文件（Windows 下可能因文件占用失败）
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    # Windows 下文件可能被占用，延迟删除
                    import time
                    for attempt in range(3):
                        try:
                            os.remove(temp_file_path)
                            logger.info(f"Cleaned up temp file: {temp_file_path}")
                            break
                        except PermissionError:
                            if attempt < 2:
                                time.sleep(0.5)
                            else:
                                logger.warning(f"Temp file locked, will be cleaned later: {temp_file_path}")
                        except Exception as cleanup_error:
                            logger.error(f"Failed to cleanup temp file: {cleanup_error}")
                            break
                except Exception:
                    pass
            
            raise serializers.ValidationError(f'文件上传失败: {str(e)}')
