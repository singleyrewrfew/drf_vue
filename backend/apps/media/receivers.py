import logging

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Media
from apps.core.events import media_uploaded, media_processed

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Media)
def on_media_created(sender, instance, created, **kwargs):
    """
    媒体文件创建后的信号处理
    
    仅处理新创建的视频文件，触发缩略图生成任务。
    使用 transaction.on_commit 确保事务提交后再执行任务。
    """
    if not created:
        return

    # 触发媒体上传事件（解耦）
    try:
        media_uploaded.send(
            sender=Media,
            media=instance,
            uploader=instance.uploader
        )
    except Exception as e:
        logger.error(f'Failed to trigger media_uploaded event: {e}', exc_info=True)

    if not instance.is_video:
        return

    if instance.reference:
        logger.info(f"[Signal] Media {instance.id} is a reference, skipping thumbnail generation")
        return

    def trigger_thumbnail_task():
        from .tasks import generate_video_thumbnails

        logger.info(f"[Signal] Transaction committed, triggering thumbnail task for media {instance.id}")
        generate_video_thumbnails.delay(str(instance.id))

    transaction.on_commit(trigger_thumbnail_task)

    logger.info(f"[Signal] Video uploaded: {instance.id}, thumbnail task scheduled after transaction commit")


@receiver(media_processed)
def on_thumbnail_generated(sender, media_id, success, processing_type=None, error=None, **kwargs):
    """
    媒体处理完成的信号处理（统一处理所有媒体类型）
    
    可用于后续扩展，如通知用户、更新缓存等。
    """
    if success:
        logger.info(f'[Signal] Media processed successfully: media_id={media_id}, type={processing_type}')
    else:
        logger.warning(f'[Signal] Media processing failed: media_id={media_id}, error={error}')
