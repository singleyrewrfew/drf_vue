import hashlib
import os
import subprocess
import threading
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings

User = get_user_model()

FFMPEG_PATH = r'D:\ffmpeg-2025-12-18-git-78c75d546a-essentials_build\bin'
FFMPEG = os.path.join(FFMPEG_PATH, 'ffmpeg.exe')
FFPROBE = os.path.join(FFMPEG_PATH, 'ffprobe.exe')

THUMBNAIL_STATUS_CHOICES = [
    ('pending', '等待中'),
    ('processing', '处理中'),
    ('completed', '已完成'),
    ('failed', '失败'),
]


def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    return f'{instance.uploader.id}/{uuid.uuid4().hex}.{ext}'


def thumbnails_upload_to(instance, filename):
    return f'thumbnails/{instance.uploader.id}/{filename}'


def generate_video_thumbnails(video_path, output_dir, interval=5):
    """
    生成视频缩略图（Artplayer 格式）
    :param video_path: 视频文件路径
    :param output_dir: 输出目录
    :param interval: 截取间隔（秒）
    :return: (thumbnails_image_path, thumbnails_count)
    """
    os.makedirs(output_dir, exist_ok=True)
    
    thumbnails_image = os.path.join(output_dir, 'thumbnails.jpg')
    
    try:
        result = subprocess.run(
            [FFPROBE, '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', video_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        duration = float(result.stdout.strip())
    except Exception as e:
        print(f"Error getting video duration: {e}")
        return None, 0
    
    num_thumbnails = max(1, int(duration / interval))
    
    cols = min(num_thumbnails, 10)
    rows = (num_thumbnails + cols - 1) // cols
    
    filter_complex = f"fps=1/{interval},scale=160:90,tile={cols}x{rows}"
    
    try:
        subprocess.run(
            [FFMPEG, '-y', '-i', video_path, '-vf', filter_complex, '-frames:v', '1', thumbnails_image],
            capture_output=True,
            timeout=300
        )
    except Exception as e:
        print(f"Error generating thumbnails: {e}")
        return None, 0
    
    if not os.path.exists(thumbnails_image):
        return None, 0
    
    return thumbnails_image, num_thumbnails


class MediaManager(models.Manager):
    def get_or_create_by_file(self, file, uploader):
        file.seek(0)
        file_hash = hashlib.md5(file.read()).hexdigest()
        file.seek(0)
        file_size = file.size

        # 首先检查当前用户是否已上传过相同文件
        existing_for_uploader = self.filter(
            file_hash=file_hash,
            file_size=file_size,
            uploader=uploader
        ).first()

        if existing_for_uploader:
            # 如果当前用户已上传过相同文件，直接返回现有记录
            return existing_for_uploader, False

        # 检查是否有其他用户上传过相同文件（全局去重）
        existing_global = self.filter(
            file_hash=file_hash,
            file_size=file_size
        ).first()

        if existing_global:
            # 如果其他用户已上传相同文件，创建引用记录
            media = self.model(
                filename=file.name,
                file_type=file.content_type,
                file_size=file_size,
                file_hash=file_hash,
                uploader=uploader,
                reference=existing_global  # 指向原始文件
            )
            media.save()
            return media, False  # 返回引用记录

        # 如果是新文件，创建新记录
        media = self.model(
            file=file,
            filename=file.name,
            file_type=file.content_type,
            file_size=file_size,
            file_hash=file_hash,
            uploader=uploader
        )
        media.save()
        return media, True


class Media(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to=upload_to, verbose_name='文件', blank=True, null=True)
    filename = models.CharField(max_length=200, verbose_name='文件名')
    file_type = models.CharField(max_length=50, verbose_name='文件类型')
    file_size = models.PositiveIntegerField(verbose_name='文件大小 (字节)')
    file_hash = models.CharField(max_length=32, blank=True, verbose_name='文件 MD5')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='media_files', verbose_name='上传者')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')
    reference = models.ForeignKey('self', on_delete=models.CASCADE, related_name='references', null=True, blank=True, verbose_name='引用文件')
    thumbnails = models.ImageField(upload_to=thumbnails_upload_to, blank=True, null=True, verbose_name='缩略图')
    thumbnails_count = models.PositiveIntegerField(default=0, verbose_name='缩略图数量')
    thumbnail_status = models.CharField(max_length=20, choices=THUMBNAIL_STATUS_CHOICES, default='pending', verbose_name='缩略图状态')

    objects = MediaManager()

    class Meta:
        db_table = 'media'
        verbose_name = '媒体文件'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['file_hash'], name='media_file_hash_idx'),
            models.Index(fields=['uploader', '-created_at'], name='media_uploader_created_idx'),
            models.Index(fields=['file_type'], name='media_file_type_idx'),
        ]

    def __str__(self):
        return self.filename

    @property
    def url(self):
        # 如果有引用，返回引用文件的 URL
        if self.reference:
            return self.reference.file.url if self.reference.file else None
        return self.file.url if self.file else None

    @property
    def actual_file(self):
        """获取实际文件（可能是引用文件）"""
        if self.reference:
            return self.reference.file
        return self.file

    @property
    def is_image(self):
        image_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
        return self.file_type in image_types

    @property
    def is_video(self):
        return self.file_type.startswith('video/')

    def generate_thumbnails(self):
        """生成视频缩略图"""
        if not self.is_video or not self.file:
            return False
        
        self.thumbnail_status = 'processing'
        self.save(update_fields=['thumbnail_status'])
        
        video_path = self.file.path
        output_dir = os.path.join(settings.MEDIA_ROOT, 'thumbnails', str(self.uploader.id), str(self.id))
        
        try:
            thumbnails_image, num_thumbnails = generate_video_thumbnails(video_path, output_dir)
            
            if thumbnails_image and num_thumbnails > 0:
                relative_image_path = os.path.relpath(thumbnails_image, settings.MEDIA_ROOT)
                
                self.thumbnails.name = relative_image_path
                self.thumbnails_count = num_thumbnails
                self.thumbnail_status = 'completed'
                self.save(update_fields=['thumbnails', 'thumbnails_count', 'thumbnail_status'])
                return True
            else:
                self.thumbnail_status = 'failed'
                self.save(update_fields=['thumbnail_status'])
                return False
        except Exception as e:
            print(f"Error generating thumbnails: {e}")
            self.thumbnail_status = 'failed'
            self.save(update_fields=['thumbnail_status'])
            return False

    def generate_thumbnails_async(self):
        """异步生成视频缩略图"""
        if not self.is_video:
            return
        
        def _generate():
            import django
            django.setup()
            from apps.media.models import Media
            try:
                media = Media.objects.get(id=self.id)
                media.generate_thumbnails()
            except Exception as e:
                print(f"Async thumbnail generation error: {e}")
        
        thread = threading.Thread(target=_generate)
        thread.daemon = True
        thread.start()
