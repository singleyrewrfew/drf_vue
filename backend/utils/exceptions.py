from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from utils.response import api_error
from utils.error_codes import ErrorTypes
import logging

logger = logging.getLogger('django.request')


# ==========================================
# 统一业务异常体系
# ==========================================

class AppException(APIException):
    """
    应用基础异常类
    
    所有业务异常都应该继承自此类，确保统一的错误处理流程
    """
    default_detail = '服务器错误'
    default_code = 'error'
    
    def __init__(self, detail=None, code=None, error_type=None):
        """
        Args:
            detail: 错误详情（字符串或字典）
            code: 错误代码（字符串）
            error_type: 错误类型（使用 ErrorTypes 常量）
        """
        super().__init__(detail=detail, code=code)
        self.error_type = error_type or ErrorTypes.INTERNAL_ERROR


class BusinessException(AppException):
    """
    业务逻辑异常基类
    
    用于表示业务规则违反，如权限不足、数据验证失败等
    """
    pass


class PermissionException(BusinessException):
    """
    权限异常
    
    当用户没有执行某操作的权限时抛出
    HTTP 403 Forbidden
    """
    status_code = 403
    default_detail = '无权限执行此操作'
    default_code = 'permission_denied'
    
    def __init__(self, detail=None):
        super().__init__(
            detail=detail or self.default_detail,
            error_type=ErrorTypes.FORBIDDEN
        )


class ValidationException(BusinessException):
    """
    数据验证异常
    
    当输入数据不符合要求时抛出
    HTTP 400 Bad Request
    """
    status_code = 400
    default_detail = '数据验证失败'
    default_code = 'validation_error'
    
    def __init__(self, detail=None, field_errors=None):
        """
        Args:
            detail: 通用错误消息
            field_errors: 字段级别的错误字典 {field: [errors]}
        """
        if field_errors:
            # 如果有字段级错误，使用字典格式
            super().__init__(detail=field_errors, error_type=ErrorTypes.VALIDATION_ERROR)
        else:
            super().__init__(
                detail=detail or self.default_detail,
                error_type=ErrorTypes.VALIDATION_ERROR
            )


class ResourceNotFoundException(BusinessException):
    """
    资源不存在异常
    
    当请求的资源不存在时抛出
    HTTP 404 Not Found
    """
    status_code = 404
    default_detail = '资源不存在'
    default_code = 'not_found'
    
    def __init__(self, detail=None, resource_type=None):
        if resource_type:
            detail = detail or f'{resource_type}不存在'
        super().__init__(
            detail=detail or self.default_detail,
            error_type=ErrorTypes.NOT_FOUND
        )


class ConflictException(BusinessException):
    """
    冲突异常
    
    当操作与当前状态冲突时抛出（如重复提交、状态不符）
    HTTP 409 Conflict
    """
    status_code = 409
    default_detail = '操作冲突'
    default_code = 'conflict'
    
    def __init__(self, detail=None):
        super().__init__(
            detail=detail or self.default_detail,
            error_type=ErrorTypes.CONFLICT
        )


class RateLimitException(BusinessException):
    """
    频率限制异常
    
    当用户操作频率超限时抛出
    HTTP 429 Too Many Requests
    """
    status_code = 429
    default_detail = '操作过于频繁，请稍后再试'
    default_code = 'rate_limit_exceeded'
    
    def __init__(self, detail=None, retry_after=None):
        super().__init__(
            detail=detail or self.default_detail,
            error_type=ErrorTypes.RATE_LIMIT_EXCEEDED
        )
        if retry_after:
            self.retry_after = retry_after


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
        409: ErrorTypes.CONFLICT,
        423: ErrorTypes.CONFLICT,
        429: ErrorTypes.RATE_LIMIT_EXCEEDED,
        500: ErrorTypes.INTERNAL_ERROR,
    }
    
    # 优先使用业务异常的 error_type
    if hasattr(exc, 'error_type'):
        error_type = exc.error_type
    else:
        error_type = error_type_map.get(status_code, ErrorTypes.INTERNAL_ERROR)
    
    return api_error(
        message=msg,
        error_type=error_type,
        status=status_code
    )
