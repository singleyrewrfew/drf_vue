import json
import logging
import time

from django.http import StreamingHttpResponse, HttpResponseForbidden
from utils.cache_utils import get_redis_client

logger = logging.getLogger(__name__)

THUMBNAIL_CHANNEL_PREFIX = 'thumbnail:'
HEARTBEAT_INTERVAL = 30
SSE_TIMEOUT = 600
DB_FALLBACK_INTERVAL = 10


def _get_current_status(media_id):
    """
    获取媒体文件当前缩略图状态

    SSE 连接建立时先查一次数据库，确保不错过订阅前的状态变更。

    Args:
        media_id: 媒体文件 ID

    Returns:
        dict: 包含状态信息的事件数据，媒体不存在时返回 None
    """
    from apps.media.models import Media

    try:
        media = Media.objects.only(
            'id', 'thumbnail_status', 'thumbnails', 'thumbnails_count'
        ).get(id=media_id)
        event_data = {
            'media_id': str(media.id),
            'thumbnail_status': media.thumbnail_status,
        }
        if media.thumbnail_status == 'completed':
            event_data['thumbnails_url'] = media.thumbnails.url if media.thumbnails else None
            event_data['thumbnails_count'] = media.thumbnails_count
        return event_data
    except Media.DoesNotExist:
        return None


def event_stream(media_id):
    """
    基于 Redis Pub/Sub 的 SSE 事件流（带 DB 轮询兜底）

    工作流程：
    1. 先订阅 Redis 频道
    2. Drain subscribe 确认消息，确保 SUBSCRIBE 命令已真正发送到 Redis
    3. 查数据库获取当前状态
    4. 如果已是终态（completed/failed），直接推送并关闭
    5. 否则推送当前状态，进入监听循环
    6. 优先通过 Redis Pub/Sub 接收事件（毫秒级）
    7. 每 10 秒兜底查一次数据库（防止 Redis 消息丢失）
    8. 每 30 秒发送心跳防止代理服务器断开连接
    9. 超时 600 秒自动关闭

    Args:
        media_id: 媒体文件 ID

    Yields:
        str: SSE 格式的事件数据字符串
    """
    channel = f'{THUMBNAIL_CHANNEL_PREFIX}{media_id}'
    pubsub = None

    try:
        client = get_redis_client()
        pubsub = client.pubsub()
        pubsub.subscribe(channel)

        deadline = time.time() + 5
        while time.time() < deadline:
            msg = pubsub.get_message(timeout=1)
            if msg and msg['type'] == 'subscribe':
                logger.debug(f"[SSE] 已订阅频道: {channel}")
                break

        current = _get_current_status(media_id)
        if current is None:
            yield f"data: {json.dumps({'error': 'Media not found'})}\n\n"
            return

        if current['thumbnail_status'] in ('completed', 'failed'):
            yield f"data: {json.dumps(current)}\n\n"
            return

        yield f"data: {json.dumps(current)}\n\n"

        last_heartbeat = time.time()
        last_db_check = time.time()
        start_time = time.time()
        last_status = current['thumbnail_status']

        while True:
            if time.time() - start_time > SSE_TIMEOUT:
                logger.debug(f"[SSE] 连接超时: media_id={media_id}")
                yield f"data: {json.dumps({'error': 'Connection timeout'})}\n\n"
                break

            try:
                message = pubsub.get_message(timeout=0.1)
            except Exception:
                message = None

            if message and message['type'] == 'message':
                data = message['data']
                if isinstance(data, bytes):
                    data = data.decode('utf-8')

                yield f"data: {data}\n\n"

                try:
                    parsed = json.loads(data)
                    if parsed.get('thumbnail_status') in ('completed', 'failed'):
                        break
                    last_status = parsed.get('thumbnail_status', last_status)
                except (json.JSONDecodeError, KeyError):
                    pass

            current_time = time.time()

            if current_time - last_db_check >= DB_FALLBACK_INTERVAL:
                last_db_check = current_time
                fallback = _get_current_status(media_id)
                if fallback and fallback['thumbnail_status'] != last_status:
                    last_status = fallback['thumbnail_status']
                    yield f"data: {json.dumps(fallback)}\n\n"
                    if fallback['thumbnail_status'] in ('completed', 'failed'):
                        break

            if current_time - last_heartbeat >= HEARTBEAT_INTERVAL:
                yield ": heartbeat\n\n"
                last_heartbeat = current_time

    except GeneratorExit:
        pass
    except Exception as e:
        logger.error(f"[SSE] 事件流异常: media_id={media_id}, error={e}")
    finally:
        if pubsub:
            try:
                pubsub.unsubscribe(channel)
                pubsub.close()
                logger.debug(f"[SSE] 已取消订阅频道: {channel}")
            except Exception:
                pass
        logger.debug(f"[SSE] 流连接已关闭: media_id={media_id}")


def authenticate_request(request):
    """
    从HTTP请求中提取并验证JWT令牌，返回认证用户对象。

    支持两种令牌传递方式：
    1. Authorization请求头：Bearer <token>
    2. URL查询参数：?token=<token>

    Args:
        request: Django HTTP请求对象，包含认证信息

    Returns:
        User对象: 认证成功时返回对应的用户对象
        None: 认证失败、令牌无效或令牌缺失时返回None
    """
    from rest_framework_simplejwt.tokens import AccessToken
    from django.contrib.auth import get_user_model

    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    
    if auth_header.startswith('Bearer '):
        token = auth_header[7:]
    else:
        token = request.GET.get('token')

    if not token:
        logger.warning("[SSE] 未提供认证令牌")
        return None

    try:
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        User = get_user_model()
        user = User.objects.select_related('role').prefetch_related('role__permissions').get(id=user_id)
        logger.debug(f"[SSE] 认证成功: user_id={user_id}")
        return user
    except Exception as e:
        logger.warning(f"[SSE] 令牌验证失败")
        return None


def thumbnail_status_stream(request, media_id):
    """
    SSE视图函数，用于建立媒体缩略图状态的实时推送连接。
    """
    from apps.media.models import Media

    user = authenticate_request(request)
    if not user:
        logger.warning(f"[SSE] 认证失败: media_id={media_id}")
        return HttpResponseForbidden('认证失败')

    try:
        media = Media.objects.select_related('uploader').get(id=media_id)
        
        is_admin = user.is_admin or user.is_superuser
        is_owner = media.uploader_id == user.id
        
        logger.debug(f"[SSE] 权限检查: media_id={media_id}, is_admin={is_admin}, is_owner={is_owner}")
        
        if not is_admin and not is_owner:
            logger.warning(f"[SSE] 权限拒绝: user_id={user.id} 无权访问 media_id={media_id}")
            return HttpResponseForbidden('无权访问此资源')
            
    except Media.DoesNotExist:
        logger.warning(f"[SSE] 媒体不存在: media_id={media_id}")
        return HttpResponseForbidden('媒体文件不存在')

    response = StreamingHttpResponse(
        event_stream(media_id),
        content_type='text/event-stream',
    )
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response
