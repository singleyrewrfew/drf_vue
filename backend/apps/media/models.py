import hashlib
import logging
import os
import platform
import shutil
import subprocess
import threading
import time
import uuid

from django.db import models, transaction
from django.conf import settings
from apps.core.models import User
from apps.base.models import BaseModel

logger = logging.getLogger(__name__)


def get_ffmpeg_executable(name):
    """
    查找 FFmpeg/FFprobe 可执行文件路径

    搜索顺序：系统 PATH → Django 配置 → 常见安装目录
    """
    ffmpeg_path = shutil.which(name)
    if ffmpeg_path:
        return ffmpeg_path

    common_paths = [getattr(settings, 'FFMPEG_PATH', None)]
    common_paths.extend(getattr(settings, 'FFMPEG_ADDITIONAL_PATHS', []))

    if platform.system() == 'Windows':
        common_paths.extend([
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'ffmpeg', 'bin'),
            os.path.join(os.environ.get('PROGRAMFILES', ''), 'ffmpeg', 'bin'),
        ])
        exe_name = f'{name}.exe'
    else:
        common_paths.extend([
            '/usr/bin',
            '/usr/local/bin',
            '/opt/ffmpeg/bin',
        ])
        exe_name = name

    for path in common_paths:
        if path:
            exe_path = os.path.join(path, exe_name)
            if os.path.exists(exe_path):
                return exe_path

    return name


FFMPEG = get_ffmpeg_executable('ffmpeg')
FFPROBE = get_ffmpeg_executable('ffprobe')

logger.info(f"[FFmpeg] Module loaded - FFMPEG: {FFMPEG}, FFPROBE: {FFPROBE}")

THUMBNAIL_STATUS_CHOICES = [
    ('pending', '等待中'),
    ('processing', '处理中'),
    ('completed', '已完成'),
    ('failed', '失败'),
]


def upload_to(instance, filename):
    """
    生成文件上传路径

    按用户 ID 和文件类型分类存储，结构为：
    {用户 ID}/{UUID}.{扩展名}
    """
    ext = filename.split('.')[-1].lower() if '.' in filename else ''
    return f'{instance.uploader.id}/{uuid.uuid4().hex}.{ext}'


def thumbnails_upload_to(instance, filename):
    return f'thumbnails/{instance.uploader.id}/{filename}'


def generate_video_thumbnails(video_path, output_dir, interval=5):
    """
    生成视频缩略图（Artplayer 格式）

    使用 FFmpeg 将视频按间隔截帧并拼合为一张雪碧图。
    返回 (缩略图图片路径, 截帧数量)，失败返回 (None, 0)。
    """
    os.makedirs(output_dir, exist_ok=True)

    thumbnails_image = os.path.join(output_dir, 'thumbnails.jpg')

    try:
        result = subprocess.run(
            [FFPROBE, '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', video_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode != 0:
            logger.error(f"[Thumbnail] FFPROBE failed: {result.stderr}")
            return None, 0
        duration = float(result.stdout.strip())
    except Exception as e:
        logger.error(f"[Thumbnail] Error getting video duration: {e}")
        return None, 0

    num_thumbnails = max(1, int(duration / interval))
    cols = min(num_thumbnails, 10)
    rows = (num_thumbnails + cols - 1) // cols
    filter_complex = f"fps=1/{interval},scale=160:90,tile={cols}x{rows}"

    try:
        result = subprocess.run(
            [FFMPEG, '-y', '-i', video_path, '-vf', filter_complex,
             '-frames:v', '1', thumbnails_image],
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode != 0:
            logger.error(f"[Thumbnail] FFMPEG failed (code {result.returncode}): {result.stderr}")
            return None, 0
    except subprocess.TimeoutExpired:
        logger.error(f"[Thumbnail] FFMPEG timeout for video: {video_path}")
        return None, 0
    except Exception as e:
        logger.error(f"[Thumbnail] Error generating thumbnails: {e}")
        return None, 0

    if not os.path.exists(thumbnails_image):
        logger.error(f"[Thumbnail] Output file not created: {thumbnails_image}")
        return None, 0

    return thumbnails_image, num_thumbnails


class MediaManager(models.Manager):
    @transaction.atomic
    def get_or_create_by_file(self, file, uploader):
        """
        获取或创建媒体文件（线程安全版本）

        使用数据库事务和 select_for_update 确保并发场景下的数据一致性。
        支持同用户去重和跨用户文件引用（全局去重）。
        """
        file.seek(0)
        file_hash = hashlib.md5(file.read()).hexdigest()
        file.seek(0)
        file_size = file.size

        existing_for_uploader = self.select_for_update().filter(
            file_hash=file_hash,
            file_size=file_size,
            uploader=uploader
        ).first()

        if existing_for_uploader:
            return existing_for_uploader, False

        existing_global = self.select_for_update().filter(
            file_hash=file_hash,
            file_size=file_size
        ).first()

        if existing_global:
            media = self.model(
                filename=file.name,
                file_type=file.content_type,
                file_size=file_size,
                file_hash=file_hash,
                uploader=uploader,
                reference=existing_global
            )
            media.save()
            existing_global.increment_reference_count()
            return media, False

        media = self.model(
            file=file,
            filename=file.name,
            file_type=file.content_type,
            file_size=file_size,
            file_hash=file_hash,
            uploader=uploader
        )
        media.save()
        logger.info(f"Created new media record: {media.id}")
        return media, True


class Media(BaseModel):
    """
    媒体文件模型

    继承 BaseModel，提供 UUID 主键和 created_at 自动时间戳。
    支持文件去重（同用户/跨用户引用）和视频缩略图自动生成。
    """
    file = models.FileField(upload_to=upload_to, verbose_name='文件', blank=True, null=True)
    filename = models.CharField(max_length=200, verbose_name='文件名')
    file_type = models.CharField(max_length=50, verbose_name='文件类型')
    file_size = models.PositiveIntegerField(verbose_name='文件大小 (字节)')
    file_hash = models.CharField(max_length=32, blank=True, verbose_name='文件 MD5')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='media_files', verbose_name='上传者')
    reference = models.ForeignKey('self', on_delete=models.CASCADE, related_name='references', null=True, blank=True, verbose_name='引用文件')
    reference_count = models.PositiveIntegerField(default=0, verbose_name='引用计数', editable=False)
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

    def increment_reference_count(self):
        self.reference_count += 1
        self.save(update_fields=['reference_count'])

    def decrement_reference_count(self):
        if self.reference_count > 0:
            self.reference_count -= 1
            self.save(update_fields=['reference_count'])

    @property
    def url(self):
        if self.reference:
            return self.reference.file.url if self.reference.file else None
        return self.file.url if self.file else None

    @property
    def actual_file(self):
        """获取实际文件（引用文件或自身文件）"""
        if self.reference:
            return self.reference.file
        return self.file

    @property
    def is_image(self):
        return self.file_type in ['image/jpeg', 'image/png', 'image/gif', 'image/webp']

    @property
    def is_video(self):
        return self.file_type.startswith('video/')

    def generate_thumbnails(self):
        """
        同步生成视频缩略图

        包含数据库锁重试机制（应对 SQLite 并发写入）。
        成功返回 True，失败返回 False。
        """
        if not self.is_video:
            return False

        actual_file = self.actual_file
        if not actual_file:
            logger.warning(f"[Thumbnail] Media {self.id} has no actual file, skipping")
            return False

        video_path = actual_file.path
        output_dir = os.path.join(settings.MEDIA_ROOT, 'thumbnails', str(self.uploader.id), str(self.id))

        try:
            thumbnails_image, num_thumbnails = generate_video_thumbnails(video_path, output_dir)

            if thumbnails_image and num_thumbnails > 0:
                relative_image_path = os.path.relpath(thumbnails_image, settings.MEDIA_ROOT)
                self.thumbnails.name = relative_image_path
                self.thumbnails_count = num_thumbnails
                self.thumbnail_status = 'completed'

                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        self.save(update_fields=['thumbnails', 'thumbnails_count', 'thumbnail_status'])
                        logger.info(f"[Thumbnail] Saved thumbnails for media {self.id}")
                        return True
                    except Exception as save_error:
                        if 'database is locked' in str(save_error).lower() and attempt < max_retries - 1:
                            wait_time = 1.0 * (attempt + 1)
                            logger.warning(f"[Thumbnail] DB locked, retry {attempt + 1}/{max_retries} in {wait_time}s")
                            time.sleep(wait_time)
                            continue
                        raise
            else:
                logger.warning(f"[Thumbnail] No thumbnails generated for media {self.id}")
                self.thumbnail_status = 'failed'
                self.save(update_fields=['thumbnail_status'])
                return False
        except Exception as e:
            logger.error(f"[Thumbnail] Error for media {self.id}: {e}", exc_info=True)
            self.thumbnail_status = 'failed'
            self.save(update_fields=['thumbnail_status'])
            return False

    def generate_thumbnails_async(self):
        """
        异步生成视频缩略图

        通过任务管理器在线程池中执行，包含完整的错误处理和状态回退机制。
        延迟导入 Django 和 Media 模型以适应子线程环境。
        """
        if not self.is_video:
            return

        from utils.task_manager import task_manager

        media_id = self.id
        logger.info(f"[Thumbnail] Submitting async task for media {media_id}")

        def _generate():
            import django
            from django.db import connection, transaction

            if not django.apps.apps.ready:
                django.setup()

            try:
                from apps.media.models import Media

                with transaction.atomic():
                    try:
                        media = Media.objects.select_for_update().get(id=media_id)
                    except Media.DoesNotExist:
                        logger.warning(f"[Thumbnail] Media {media_id} not found, skipping")
                        return

                    if media.thumbnail_status == 'completed':
                        logger.info(f"[Thumbnail] Media {media_id} already completed, skipping")
                        return

                    media.thumbnail_status = 'processing'
                    media.save(update_fields=['thumbnail_status'])

                with transaction.atomic():
                    media = Media.objects.get(id=media_id)
                    media.generate_thumbnails()

            except Media.DoesNotExist:
                logger.error(f"[Thumbnail] Media {media_id} not found")
            except Exception as e:
                logger.error(f"[Thumbnail] Async error for media {media_id}: {e}", exc_info=True)

                try:
                    from apps.media.models import Media
                    media = Media.objects.get(id=media_id)
                    media.thumbnail_status = 'failed'
                    media.save(update_fields=['thumbnail_status'])
                except Exception:
                    pass
            finally:
                connection.close()

        task_manager.submit(
            func=_generate,
            task_name=f"generate_thumbnails_{media_id}",
            max_retries=2,
        )
