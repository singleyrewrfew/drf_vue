"""
媒体缩略图状态 SSE 流

提供 Server-Sent Events 接口，实时推送视频缩略图生成状态。
"""
import json
import time
import logging
from django.http import StreamingHttpResponse, HttpResponseForbidden

logger = logging.getLogger(__name__)


def event_stream(media_id):
    """
    SSE 事件流生成器
    
    Args:
        media_id: 媒体文件 ID
        
    Yields:
        str: SSE 格式的事件数据
    """
    from apps.media.models import Media
    
    logger.info(f"[SSE] Starting event stream for media {media_id}")
    
    try:
        while True:
            try:
                # 查询数据库获取最新状态
                media = Media.objects.only('id', 'thumbnail_status').get(id=media_id)
                
                # 构造 SSE 事件
                event_data = {
                    'media_id': str(media.id),
                    'thumbnail_status': media.thumbnail_status,
                    'timestamp': time.time()
                }
                
                # SSE 格式：data: {...}\n\n
                yield f"data: {json.dumps(event_data)}\n\n"
                
                # 如果任务完成或失败，停止推送
                if media.thumbnail_status in ('completed', 'failed'):
                    logger.info(f"[SSE] Task finished for media {media_id}, closing stream")
                    break
                
                # 每 1 秒检查一次状态（提高实时性）
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
        logger.info(f"[SSE] Client disconnected for media {media_id}")
    finally:
        logger.info(f"[SSE] Event stream closed for media {media_id}")


def thumbnail_status_stream(request, media_id):
    """
    SSE 接口：实时推送缩略图生成状态
    
    Usage:
        const eventSource = new EventSource(`/api/media/${mediaId}/thumbnail_status/?token=xxx`);
        eventSource.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log('Status:', data.thumbnail_status);
        };
    """
    # 支持通过 URL 参数传递 token（EventSource 不支持自定义 headers）
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
    
    # 验证用户是否有权限访问该媒体文件
    from apps.media.models import Media
    try:
        media = Media.objects.get(id=media_id)
        # 非管理员只能查看自己的文件
        if not request.user.is_admin and media.uploader != request.user:
            return HttpResponseForbidden('无权访问此资源')
    except Media.DoesNotExist:
        return HttpResponseForbidden('媒体文件不存在')
    
    response = StreamingHttpResponse(
        event_stream(media_id),
        content_type='text/event-stream'
    )
    
    # SSE 必需的响应头
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'  # Nginx 禁用缓冲
    # 注意：'Connection: keep-alive' 不能在 WSGI 中设置，应在 Nginx 配置
    
    return response
