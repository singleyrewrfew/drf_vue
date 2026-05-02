import json
import time
import logging
from django.http import StreamingHttpResponse, HttpResponseForbidden

logger = logging.getLogger(__name__)


def event_stream(media_id):
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


def authenticate_request(request):
    from rest_framework_simplejwt.tokens import AccessToken
    from django.contrib.auth import get_user_model

    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    if auth_header.startswith('Bearer '):
        token = auth_header[7:]
    else:
        token = request.GET.get('token')

    if not token:
        return None

    try:
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        User = get_user_model()
        return User.objects.get(id=user_id)
    except Exception:
        return None


def thumbnail_status_stream(request, media_id):
    user = authenticate_request(request)
    if not user:
        return HttpResponseForbidden('认证失败')

    from apps.media.models import Media
    try:
        media = Media.objects.get(id=media_id)
        if not user.is_admin and media.uploader != user:
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
