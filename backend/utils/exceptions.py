from rest_framework.views import exception_handler
from utils.response import api_error
from utils.error_codes import ErrorTypes
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
        return api_error(
            message='服务器内部错误',
            error_type=ErrorTypes.INTERNAL_ERROR,
            status=500
        )

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
    
    # 提取错误消息（兼容 dict 和 list 格式）
    msg = "未知错误"
    if isinstance(response.data, dict):
        for key, value in response.data.items():
            msg = value[0] if isinstance(value, list) else str(value)
            break
    elif isinstance(response.data, list):
        msg = str(response.data[0]) if response.data else "未知错误"
    
    # ⚠️ 重要：使用统一的错误响应格式
    # 根据状态码映射对应的错误类型
    error_type_map = {
        400: ErrorTypes.BAD_REQUEST,
        401: ErrorTypes.UNAUTHORIZED,
        403: ErrorTypes.FORBIDDEN,
        404: ErrorTypes.NOT_FOUND,
        405: ErrorTypes.BAD_REQUEST,
        500: ErrorTypes.INTERNAL_ERROR,
    }
    error_type = error_type_map.get(status_code, ErrorTypes.INTERNAL_ERROR)
    
    return api_error(
        message=msg,
        error_type=error_type,
        status=status_code
    )
