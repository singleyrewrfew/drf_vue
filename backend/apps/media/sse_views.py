import json
import time
import logging
from django.http import StreamingHttpResponse, HttpResponseForbidden

logger = logging.getLogger(__name__)


def event_stream(media_id):
    """
    SSE 事件流生成器

    每秒轮询数据库检查缩略图状态，状态变更时推送事件。
    到达终态（completed/failed）后自动关闭流。

    延迟导入 Media 模型以避免循环引用。
    """
    from apps.media.models import Media

    last_status = None

    try:
        while True:
            try:
                media = Media.objects.only(
                    'id', 'thumbnail_status', 'thumbnails', 'thumbnails_count'
                ).get(id=media_id)
                current_status = media.thumbnail_status

                if current_status != last_status:
                    last_status = current_status
                    event_data = {
                        'media_id': str(media.id),
                        'thumbnail_status': current_status,
                    }
                    if current_status == 'completed':
                        event_data['thumbnails_url'] = media.thumbnails.url if media.thumbnails else None
                        event_data['thumbnails_count'] = media.thumbnails_count

                    yield f"data: {json.dumps(event_data)}\n\n"

                    if current_status in ('completed', 'failed'):
                        break

                time.sleep(1)

            except Media.DoesNotExist:
                logger.error(f"[SSE] Media {media_id} not found")
                yield f"data: {json.dumps({'error': 'Media not found'})}\n\n"
                break
            except Exception as e:
                logger.error(f"[SSE] Error streaming events: {e}")
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
                break

    except GeneratorExit:
        pass
    finally:
        logger.info(f"[SSE] Stream closed for media {media_id}")


def thumbnail_status_stream(request, media_id):
    """
    缩略图状态 SSE 端点

    通过 URL 参数传递 JWT Token 进行认证（EventSource 不支持自定义 Header）。
    仅管理员或文件上传者可访问。
    """
    token = request.GET.get('token')
    if not token:
        return HttpResponseForbidden('缺少认证 Token')

    from rest_framework_simplejwt.tokens import AccessToken
    try:
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        from django.contrib.auth import get_user_model
        User = get_user_model()
        request.user = User.objects.get(id=user_id)
    except Exception:
        return HttpResponseForbidden('无效的 Token')

    from apps.media.models import Media
    try:
        media = Media.objects.get(id=media_id)
        if not request.user.is_admin and media.uploader != request.user:
            return HttpResponseForbidden('无权访问此资源')
    except Media.DoesNotExist:
        return HttpResponseForbidden('媒体文件不存在')

    response = StreamingHttpResponse(
        event_stream(media_id),
        content_type='text/event-stream',
    )
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response
