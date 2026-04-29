import hashlib
import logging
import os
import platform
import shutil
import subprocess
import threading
import uuid

from django.db import models, transaction
from django.conf import settings
from apps.core.models import User
from apps.base.models import BaseModel

logger = logging.getLogger(__name__)


def get_ffmpeg_executable(name):
    ffmpeg_path = shutil.which(name)
    if ffmpeg_path:
        return ffmpeg_path
    
    from django.conf import settings
    
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
    
    return shutil.which(name) or name


def get_ffprobe_path():
    path = get_ffmpeg_executable('ffprobe')
    logger.debug(f"[FFmpeg] FFPROBE path resolved: {path}")
    return path


def get_ffmpeg_path():
    path = get_ffmpeg_executable('ffmpeg')
    logger.debug(f"[FFmpeg] FFMPEG path resolved: {path}")
    return path


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
    
    参数:
        instance: Media 实例
        filename: 原始文件名
    
    返回:
        str: 上传路径
    """
    ext = filename.split('.')[-1].lower() if '.' in filename else ''
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
    
    ffprobe_path = get_ffprobe_path()
    ffmpeg_path = get_ffmpeg_path()
    
    logger.info(f"[Thumbnail] Using FFPROBE: {ffprobe_path}")
    logger.info(f"[Thumbnail] Using FFMPEG: {ffmpeg_path}")
    
    try:
        result = subprocess.run(
            [ffprobe_path, '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', video_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode != 0:
            logger.error(f"FFPROBE failed: {result.stderr}")
            return None, 0
        duration = float(result.stdout.strip())
    except Exception as e:
        logger.error(f"Error getting video duration: {e}")
        return None, 0
    
    num_thumbnails = max(1, int(duration / interval))
    
    cols = min(num_thumbnails, 10)
    rows = (num_thumbnails + cols - 1) // cols
    
    filter_complex = f"fps=1/{interval},scale=160:90,tile={cols}x{rows}"
    
    try:
        result = subprocess.run(
            [ffmpeg_path, '-y', '-i', video_path, '-vf', filter_complex, '-frames:v', '1', thumbnails_image],
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode != 0:
            logger.error(f"FFMPEG failed with code {result.returncode}: {result.stderr}")
            return None, 0
    except subprocess.TimeoutExpired:
        logger.error(f"FFMPEG timeout for video: {video_path}")
        return None, 0
    except Exception as e:
        logger.error(f"Error generating thumbnails: {e}")
        return None, 0
    
    if not os.path.exists(thumbnails_image):
        logger.error(f"Thumbnails file not created: {thumbnails_image}")
        return None, 0
    
    return thumbnails_image, num_thumbnails


class MediaManager(models.Manager):
    @transaction.atomic
    def get_or_create_by_file(self, file, uploader):
        """
        获取或创建媒体文件（线程安全版本）
        
        使用数据库事务和 select_for_update 确保并发场景下的数据一致性。
        只有在文件成功保存后才插入数据库记录。
        
        参数:
            file: 上传的文件对象
            uploader: 上传者用户对象
        
        返回:
            tuple: (Media 实例，是否新创建)
        
        异常:
            Exception: 如果文件保存失败，会抛出异常并回滚事务
        """
        # 计算文件哈希值
        file.seek(0)
        file_hash = hashlib.md5(file.read()).hexdigest()
        file.seek(0)
        file_size = file.size

        # 使用数据库锁检查当前用户是否已上传过相同文件
        existing_for_uploader = self.select_for_update().filter(
            file_hash=file_hash,
            file_size=file_size,
            uploader=uploader
        ).first()

        if existing_for_uploader:
            # 如果当前用户已上传过相同文件，直接返回现有记录
            logger.debug(f"File already uploaded by user: {existing_for_uploader.id}")
            return existing_for_uploader, False

        # 使用数据库锁检查是否有其他用户上传过相同文件（全局去重）
        existing_global = self.select_for_update().filter(
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
            # 增加原始文件的引用计数
            existing_global.increment_reference_count()
            logger.debug(f"Created reference record: {media.id} -> {existing_global.id}")
            return media, False  # 返回引用记录

        # 如果是新文件，创建新记录
        # 注意：Django 的 FileField 会在 model.save() 时自动保存文件
        # 如果文件保存失败，save() 会抛出异常，事务会自动回滚
        media = self.model(
            file=file,
            filename=file.name,
            file_type=file.content_type,
            file_size=file_size,
            file_hash=file_hash,
            uploader=uploader
        )
        
        # 保存文件（如果失败会抛出异常，事务回滚）
        media.save()
        logger.info(f"Created new media record: {media.id}, file saved successfully")
        return media, True


class Media(BaseModel):
    """
    媒体文件模型
    
    继承 BaseModel，提供：
    - UUID 主键
    - created_at 自动时间戳
    """
    # 注意：id, created_at 由 BaseModel 提供
    file = models.FileField(upload_to=upload_to, verbose_name='文件', blank=True, null=True)
    filename = models.CharField(max_length=200, verbose_name='文件名')
    file_type = models.CharField(max_length=50, verbose_name='文件类型')
    file_size = models.PositiveIntegerField(verbose_name='文件大小 (字节)')
    file_hash = models.CharField(max_length=32, blank=True, verbose_name='文件 MD5')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='media_files', verbose_name='上传者')
    # 注意：created_at 由 BaseModel 提供
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
        """增加引用计数"""
        self.reference_count += 1
        self.save(update_fields=['reference_count'])

    def decrement_reference_count(self):
        """减少引用计数"""
        if self.reference_count > 0:
            self.reference_count -= 1
            self.save(update_fields=['reference_count'])

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
        """生成视频缩略图（同步方法，在线程中调用）"""
        print(f"[Thumbnail] generate_thumbnails called for media {self.id}")
        
        if not self.is_video:
            print(f"[Thumbnail] Media {self.id} is not a video, skipping")
            return False
        
        actual_file = self.actual_file
        if not actual_file:
            print(f"[Thumbnail] Media {self.id} has no actual file, skipping")
            return False
        
        # 注意：状态已在 generate_thumbnails_async() 的任务函数中设置为 'processing'
        # 这里只需要处理 completed/failed 状态
        
        video_path = actual_file.path
        print(f"[Thumbnail] Video path: {video_path}")
        output_dir = os.path.join(settings.MEDIA_ROOT, 'thumbnails', str(self.uploader.id), str(self.id))
        print(f"[Thumbnail] Output directory: {output_dir}")
        
        try:
            thumbnails_image, num_thumbnails = generate_video_thumbnails(video_path, output_dir)
            print(f"[Thumbnail] Generated: image={thumbnails_image}, count={num_thumbnails}")
            
            if thumbnails_image and num_thumbnails > 0:
                relative_image_path = os.path.relpath(thumbnails_image, settings.MEDIA_ROOT)
                print(f"[Thumbnail] Relative path: {relative_image_path}")
                
                self.thumbnails.name = relative_image_path
                self.thumbnails_count = num_thumbnails
                self.thumbnail_status = 'completed'
                
                # SQLite 并发保存重试机制
                import time
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        self.save(update_fields=['thumbnails', 'thumbnails_count', 'thumbnail_status'])
                        print(f"[Thumbnail] Successfully saved thumbnails for media {self.id}")
                        return True
                    except Exception as save_error:
                        if 'database is locked' in str(save_error).lower() and attempt < max_retries - 1:
                            wait_time = 1.0 * (attempt + 1)
                            logger.warning(f"[Thumbnail] Database locked during save, retrying in {wait_time}s... (attempt {attempt + 1}/{max_retries})")
                            time.sleep(wait_time)
                            continue
                        raise
            else:
                print(f"[Thumbnail] No thumbnails generated for media {self.id}")
                self.thumbnail_status = 'failed'
                self.save(update_fields=['thumbnail_status'])
                return False
        except Exception as e:
            print(f"[Thumbnail] Error generating thumbnails for media {self.id}: {e}")
            import traceback
            traceback.print_exc()
            self.thumbnail_status = 'failed'
            self.save(update_fields=['thumbnail_status'])
            return False

    def generate_thumbnails_async(self):
        """
        异步生成视频缩略图
        
        使用任务管理器处理视频缩略图生成，提供完整的错误处理和状态更新机制。
        """
        if not self.is_video:
            return
        
        from utils.task_manager import task_manager, TaskInfo
        
        media_id = self.id
        logger.info(f"[Thumbnail] Submitting async thumbnail generation task for media {media_id}")
        
        def _generate():
            import django
            from django.db import connection, transaction
            import time
            
            if not django.apps.apps.ready:
                django.setup()
            
            try:
                from apps.media.models import Media
                logger.debug(f"[Thumbnail] Fetching media {media_id} from database")
                
                with transaction.atomic():
                    try:
                        media = Media.objects.select_for_update().get(id=media_id)
                    except Media.DoesNotExist:
                        logger.warning(f"[Thumbnail] Media {media_id} not found, skipping")
                        return
                    
                    current_status = media.thumbnail_status
                    logger.debug(f"[Thumbnail] Media found, current status: {current_status}")
                    
                    if current_status == 'completed':
                        logger.info(f"[Thumbnail] Media {media_id} already completed, skipping")
                        return
                    
                    media.thumbnail_status = 'processing'
                    media.save(update_fields=['thumbnail_status'])
                    logger.info(f"[Thumbnail] Media {media_id} status changed to 'processing'")
                
                with transaction.atomic():
                    media = Media.objects.get(id=media_id)
                    result = media.generate_thumbnails()
                    logger.debug(f"[Thumbnail] Generation result: {result}, new status: {media.thumbnail_status}")
                    
            except Media.DoesNotExist:
                logger.error(f"[Thumbnail] Media {media_id} not found")
            except Exception as e:
                logger.error(f"[Thumbnail] Async thumbnail generation error: {e}")
                import traceback
                traceback.print_exc()
                
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
            callback=lambda task_info: logger.info(
                f"[Thumbnail] Task {task_info.task_id} completed with status: {task_info.status.value}"
            )
        )
