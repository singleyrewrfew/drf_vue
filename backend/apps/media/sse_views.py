import json
import time
import logging
from django.http import StreamingHttpResponse, HttpResponseForbidden

logger = logging.getLogger(__name__)


def event_stream(media_id):
    """
    生成SSE（Server-Sent Events）事件流，用于实时推送媒体缩略图处理状态。

    该函数会持续轮询数据库检查媒体文件的缩略图状态，当状态发生变化时向客户端推送更新。
    当状态变为'completed'或'failed'时，或者发生错误时，流将自动关闭。

    Args:
        media_id: 媒体文件的唯一标识符（UUID或整数）

    Yields:
        str: SSE格式的事件数据字符串，包含以下信息：
            - media_id: 媒体文件ID
            - thumbnail_status: 缩略图处理状态（processing/completed/failed等）
            - thumbnails_url: 缩略图URL（仅在状态为completed时提供）
            - thumbnails_count: 缩略图数量（仅在状态为completed时提供）
            - error: 错误信息（仅在发生错误时提供）
            - heartbeat: 心跳信号（每30秒发送一次，保持连接活跃）

    Note:
        - 每5秒轮询一次数据库，平衡实时性和数据库负载
        - 每30秒发送心跳防止代理服务器断开连接
        - 使用GeneratorExit优雅处理客户端断开连接
        - 所有异常都会被捕获并记录到日志中
    """
    from apps.media.models import Media

    last_status = None
    last_heartbeat = time.time()

    try:
        while True:
            try:
                media = Media.objects.only(
                    'id', 'thumbnail_status', 'thumbnails', 'thumbnails_count'
                ).get(id=media_id)
                current_status = media.thumbnail_status

                current_time = time.time()
                
                # 每30秒发送心跳，防止代理服务器断开空闲连接
                if current_time - last_heartbeat >= 30:
                    yield ": heartbeat\n\n"
                    last_heartbeat = current_time
                    logger.debug(f"[SSE] 发送心跳: media_id={media_id}")

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

                time.sleep(5)

            except Media.DoesNotExist:
                logger.error(f"[SSE] 媒体文件 {media_id} 不存在")
                yield f"data: {json.dumps({'error': 'Media not found'})}\n\n"
                break
            except Exception as e:
                logger.error(f"[SSE] 事件流推送错误: {e}")
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
                break

    except GeneratorExit:
        pass
    finally:
        logger.info(f"[SSE] 媒体 {media_id} 的流连接已关闭")


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
        logger.info(f"[SSE] 认证成功: user_id={user_id}, username={user.username}")
        return user
    except Exception as e:
        logger.warning(f"[SSE] 令牌验证失败: {e}")
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
        
        logger.info(
            f"[SSE] 权限检查: media_id={media_id}, "
            f"user={user.username}, uploader={media.uploader.username if media.uploader else 'None'}, "
            f"is_admin={is_admin}, is_owner={is_owner}"
        )
        
        if not is_admin and not is_owner:
            logger.warning(f"[SSE] 权限拒绝: user={user.username} 无权访问 media_id={media_id}")
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
