from rest_framework.views import exception_handler
from rest_framework.response import Response
import logging

logger = logging.getLogger('django.request')


def custom_exception_handler(exc, context):
    """
    自定义 DRF 全局异常捕获（真正可用的生产级）
    能捕获：
    1. DRF 异常（认证、权限、校验、APIException）
    2. 代码错误（服务器 500）
    """
    # 先调用 DRF 原有异常处理
    response = exception_handler(exc, context)

    # 获取请求信息
    request = context.get("request")
    view = context.get("view")
    url = request.path if request else "未知URL"
    method = request.method if request else "未知方法"

    # ==========================================
    # 关键：如果 response 为 None → 代表代码报错
    # ==========================================
    if response is None:
        logger.error(f"""
        ==============================================
        【服务器错误 500】
        URL: {url}
        方法: {method}
        视图: {view.__class__.__name__ if view else '未知视图'}
        错误: {str(exc)}
        ==============================================
        """)
        return Response({"detail": "服务器内部错误"}, status=500)

    # DRF 正常异常
    status_code = response.status_code
    logger.error(f"""
    ==============================================
    【接口异常】
    URL: {url}
    方法: {method}
    状态码: {status_code}
    视图: {view.__class__.__name__ if view else '未知视图'}
    内容: {response.data}
    ==============================================
    """)
    msg = "未知错误"
    for key, value in response.data.items():
        msg = value[0] if isinstance(value, list) else str(value)
        break
    # 异常请求直接拦截返回错误
    return Response({"detail": msg}, status=status_code)
