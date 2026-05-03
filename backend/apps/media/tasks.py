"""
媒体处理 Celery 任务

提供视频缩略图生成等异步任务。
"""

import json
import logging
import traceback

from celery import shared_task
from utils.cache_utils import get_redis_client

logger = logging.getLogger(__name__)

THUMBNAIL_CHANNEL_PREFIX = 'thumbnail:'


def _publish_thumbnail_event(media_id, event_data):
    """
    通过 Redis Pub/Sub 发布缩略图状态变更事件

    SSE 视图订阅该频道，实现实时推送（替代轮询）。

    Args:
        media_id: 媒体文件 ID
        event_data: 事件数据字典
    """
    try:
        client = get_redis_client()
        channel = f'{THUMBNAIL_CHANNEL_PREFIX}{media_id}'
        client.publish(channel, json.dumps(event_data))
        logger.debug(f"[Celery] 发布缩略图事件: channel={channel}, status={event_data.get('thumbnail_status')}")
    except Exception as e:
        logger.warning(f"[Celery] 发布缩略图事件失败（不影响任务执行）: {e}")


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    time_limit=10 * 60,  # Hard timeout: 10 minutes
    # Note: soft_time_limit not supported on Windows (no SIGUSR1 signal)
)
def generate_video_thumbnails(self, media_id: str):
    """
    异步生成视频缩略图
    
    Args:
        media_id: 媒体文件 ID
        self: Celery 任务实例（bind=True 时自动传入）
    """
    from apps.media.models import Media
    
    logger.info(f"[Celery] 开始生成视频缩略图: media_id={media_id}")
    
    try:
        media = Media.objects.get(id=media_id)
    except Media.DoesNotExist:
        logger.error(f"[Celery] 媒体文件不存在: media_id={media_id}")
        return {'status': 'error', 'message': 'Media not found'}
    
    if not media.is_video:
        logger.warning(f"[Celery] 非视频文件，跳过缩略图生成: media_id={media_id}")
        return {'status': 'skipped', 'message': 'Not a video file'}
    
    try:
        Media.objects.filter(id=media_id).update(thumbnail_status='processing')
        logger.info(f"[Celery] 状态更新为 processing: media_id={media_id}")
        _publish_thumbnail_event(media_id, {
            'media_id': str(media_id),
            'thumbnail_status': 'processing',
        })
        
        success = _do_generate_thumbnails(media)
        
        if success:
            Media.objects.filter(id=media_id).update(
                thumbnail_status='completed',
                thumbnails=media.thumbnails,
                thumbnails_count=media.thumbnails_count
            )
            logger.info(f"[Celery] 视频缩略图生成成功: media_id={media_id}")

            from apps.media.models import Media as MediaModel
            refreshed = MediaModel.objects.only('thumbnails', 'thumbnails_count').get(id=media_id)
            _publish_thumbnail_event(media_id, {
                'media_id': str(media_id),
                'thumbnail_status': 'completed',
                'thumbnails_url': refreshed.thumbnails.url if refreshed.thumbnails else None,
                'thumbnails_count': refreshed.thumbnails_count,
            })
            
            from apps.media.signals import video_thumbnail_generated
            video_thumbnail_generated.send(
                sender=None,
                media_id=str(media_id),
                success=True
            )
            
            return {'status': 'success', 'media_id': str(media_id)}
        else:
            Media.objects.filter(id=media_id).update(thumbnail_status='failed')
            logger.error(f"[Celery] 视频缩略图生成失败: media_id={media_id}")

            _publish_thumbnail_event(media_id, {
                'media_id': str(media_id),
                'thumbnail_status': 'failed',
            })
            
            from apps.media.signals import video_thumbnail_generated
            video_thumbnail_generated.send(
                sender=None,
                media_id=str(media_id),
                success=False
            )
            
            return {'status': 'failed', 'message': 'Thumbnail generation returned False'}
            
    except Exception as e:
        logger.error(f"[Celery] 视频缩略图生成异常: media_id={media_id}, error={str(e)}")
        logger.error(traceback.format_exc())
        
        try:
            Media.objects.filter(id=media_id).update(thumbnail_status='failed')
        except Exception:
            pass

        _publish_thumbnail_event(media_id, {
            'media_id': str(media_id),
            'thumbnail_status': 'failed',
        })

        if self.request.retries < self.max_retries:
            logger.info(f"[Celery] 将重试任务: media_id={media_id}, retry={self.request.retries + 1}")
            raise self.retry(exc=e)
        
        return {'status': 'failed', 'message': str(e)}


def _do_generate_thumbnails(media):
    """
    实际执行缩略图生成的内部函数
    
    Args:
        media: Media 模型实例
        
    Returns:
        bool: 成功返回 True，失败返回 False
    """
    import os
    import time
    from django.conf import settings
    from utils.video_utils import generate_video_thumbnails as gen_thumbs
    
    actual_file = media.actual_file
    if not actual_file:
        logger.warning(f"[Celery] Media {media.id} has no actual file")
        return False
    
    video_path = actual_file.path
    logger.info(f"[Celery] 视频路径: {video_path}")
    
    if not os.path.exists(video_path):
        logger.error(f"[Celery] 视频文件不存在: {video_path}")
        return False
    
    output_dir = os.path.join(
        settings.MEDIA_ROOT, 
        'thumbnails', 
        str(media.uploader.id), 
        str(media.id)
    )
    logger.info(f"[Celery] 输出目录: {output_dir}")
    
    try:
        thumbnails_image, num_thumbnails = gen_thumbs(video_path, output_dir)
        logger.info(f"[Celery] FFmpeg 执行完成: thumbnails_image={thumbnails_image}, num_thumbnails={num_thumbnails}")
    except Exception as e:
        logger.error(f"[Celery] FFmpeg 执行异常: {e}")
        logger.error(traceback.format_exc())
        return False
    
    if thumbnails_image and num_thumbnails > 0:
        relative_image_path = os.path.relpath(thumbnails_image, settings.MEDIA_ROOT)
        media.thumbnails.name = relative_image_path
        media.thumbnails_count = num_thumbnails
        logger.info(f"[Celery] 缩略图生成成功: {relative_image_path}, count={num_thumbnails}")
        return True
    else:
        logger.warning(f"[Celery] 未生成缩略图")
        return False


@shared_task(
    time_limit=5 * 60,  # Hard timeout: 5 minutes
    # Note: soft_time_limit not supported on Windows (no SIGUSR1 signal)
)
def cleanup_old_thumbnails(days: int = 30):
    """
    清理旧的临时缩略图文件
    
    Args:
        days: 清理多少天前的文件
    """
    import os
    from datetime import timedelta
    from django.utils import timezone
    from django.conf import settings
    
    logger.info(f"[Celery] 开始清理 {days} 天前的临时文件")
    
    temp_dir = getattr(settings, 'UPLOAD_TEMP_DIR', None)
    if not temp_dir or not os.path.exists(temp_dir):
        return {'status': 'skipped', 'message': 'Temp directory not found'}
    
    cutoff_time = timezone.now() - timedelta(days=days)
    cleaned_count = 0
    
    for filename in os.listdir(temp_dir):
        filepath = os.path.join(temp_dir, filename)
        if os.path.isfile(filepath):
            file_mtime = timezone.datetime.fromtimestamp(
                os.path.getmtime(filepath),
                tz=timezone.get_current_timezone()
            )
            if file_mtime < cutoff_time:
                try:
                    os.remove(filepath)
                    cleaned_count += 1
                except Exception as e:
                    logger.warning(f"[Celery] 无法删除文件 {filepath}: {e}")
    
    logger.info(f"[Celery] 清理完成，共删除 {cleaned_count} 个文件")
    return {'status': 'success', 'cleaned_count': cleaned_count}
