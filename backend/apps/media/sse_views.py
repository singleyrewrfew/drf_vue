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

    Note:
        - 每1秒轮询一次数据库
        - 使用GeneratorExit优雅处理客户端断开连接
        - 所有异常都会被捕获并记录到日志中
    """
    from apps.media.models import Media

    last_status = None

    try:
        # 持续轮询媒体文件状态直到处理完成或失败
        while True:
            try:
                # 仅查询必要的字段以优化性能
                media = Media.objects.only(
                    'id', 'thumbnail_status', 'thumbnails', 'thumbnails_count'
                ).get(id=media_id)
                current_status = media.thumbnail_status

                # 仅在状态发生变化时推送事件，避免重复推送
                if current_status != last_status:
                    last_status = current_status
                    # 构建事件数据，根据状态决定是否包含额外信息
                    event_data = {
                        'media_id': str(media.id),
                        'thumbnail_status': current_status,
                    }
                    if current_status == 'completed':
                        event_data['thumbnails_url'] = media.thumbnails.url if media.thumbnails else None
                        event_data['thumbnails_count'] = media.thumbnails_count

                    # 按照SSE协议格式推送数据
                    yield f"data: {json.dumps(event_data)}\n\n"

                    # 终态（完成或失败）时结束流
                    if current_status in ('completed', 'failed'):
                        break

                # 控制轮询间隔，避免对数据库性能造成过大压力
                time.sleep(10)

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

    Note:
        - 使用SimpleJWT的AccessToken进行令牌验证
        - 任何异常都会被视为认证失败并返回None
    """
    from rest_framework_simplejwt.tokens import AccessToken
    from django.contrib.auth import get_user_model

    # 优先从Authorization头获取令牌，其次从URL参数获取
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
    """
    SSE视图函数，用于建立媒体缩略图状态的实时推送连接。

    该函数执行以下操作：
    1. 验证用户身份（通过JWT令牌）
    2. 检查用户对媒体文件的访问权限（管理员或上传者）
    3. 创建SSE响应流开始实时推送状态更新

    Args:
        request: Django HTTP请求对象，必须包含有效的JWT认证信息
        media_id: 媒体文件的唯一标识符（UUID或整数）

    Returns:
        StreamingHttpResponse: 配置好的SSE响应对象，包含：
            - content_type: 'text/event-stream'
            - Cache-Control: 'no-cache'（禁用缓存确保实时性）
            - X-Accel-Buffering: 'no'（禁用Nginx缓冲）
        HttpResponseForbidden: 认证失败或无权访问时返回403响应

    Raises:
        不抛出异常，所有错误都通过HTTP响应码返回

    Note:
        - 只有管理员或文件上传者才能查看缩略图状态
        - 响应头配置确保了SSE流的实时性和稳定性
    """
    # 验证用户身份，未认证用户直接拒绝访问
    user = authenticate_request(request)
    if not user:
        return HttpResponseForbidden('认证失败')

    # 验证媒体文件存在性及用户访问权限
    from apps.media.models import Media
    try:
        media = Media.objects.get(id=media_id)
        # 非管理员只能访问自己上传的文件
        if not user.is_admin and media.uploader != user:
            return HttpResponseForbidden('无权访问此资源')
    except Media.DoesNotExist:
        return HttpResponseForbidden('媒体文件不存在')

    # 创建SSE流式响应，禁用缓存和代理缓冲以确保实时推送
    response = StreamingHttpResponse(
        event_stream(media_id),
        content_type='text/event-stream',
    )
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response
