import json
import logging

from django.conf import settings

logger = logging.getLogger('django')


class ResponseLogMiddleware:
    """API 响应日志中间件
    
    仅在 DEBUG 模式下记录 JSON 响应，用于开发调试。
    生产环境自动禁用，避免性能损耗和信息泄露。
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # 空列表表示监控所有 JSON 响应
        self.monitored_paths = []

    def __call__(self, request):
        response = self.get_response(request)

        # 仅在生产环境禁用日志输出
        if not settings.DEBUG:
            return response

        try:
            content_type = response.get("Content-Type", "")
            if "application/json" not in content_type:
                return response

            # 如果设置了监控路径，则只打印匹配的路径
            if self.monitored_paths and not any(
                request.path.startswith(path) for path in self.monitored_paths
            ):
                return response

            # 读取并解析响应内容
            response_data = response.content.decode("utf-8")
            
            logger.info(
                "API Response [%s] %s | Status: %d | Body: %s",
                request.method,
                request.path,
                response.status_code,
                response_data
            )

        except Exception as e:
            logger.error("ResponseLogMiddleware error: %s", str(e))

        return response
