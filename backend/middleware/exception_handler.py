"""
统一异常处理中间件

捕获并标准化处理所有 API 异常，返回统一的 JSON 格式响应
"""
import logging
from django.http import JsonResponse
from rest_framework.exceptions import (
    APIException, PermissionDenied, NotFound, ValidationError, AuthenticationFailed
)
from django.core.exceptions import (
    PermissionDenied as DjangoPermissionDenied,
    ObjectDoesNotExist, ValidationError as DjangoValidationError
)
from django.db import DatabaseError, IntegrityError

logger = logging.getLogger(__name__)


class ExceptionHandlerMiddleware:
    """
    全局异常处理中间件
    
    功能：
    1. 捕获所有未处理的异常
    2. 转换为统一的 JSON 响应格式
    3. 记录详细的错误日志
    4. 根据环境返回不同详细程度的错误信息
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as exc:
            return self.handle_exception(request, exc)
    
    def handle_exception(self, request, exc):
        """
        统一处理各类异常
        
        Args:
            request: HTTP 请求对象
            exc: 异常实例
            
        Returns:
            JsonResponse: 标准化的错误响应
        """
        # DRF 标准异常
        if isinstance(exc, (PermissionDenied, DjangoPermissionDenied)):
            logger.warning(f"Permission denied: {request.path}, user={getattr(request.user, 'username', 'anonymous')}")
            return JsonResponse(
                {'error': '权限不足', 'code': 'permission_denied'},
                status=403
            )
        
        if isinstance(exc, NotFound):
            logger.info(f"Resource not found: {request.path}")
            return JsonResponse(
                {'error': '资源不存在', 'code': 'not_found'},
                status=404
            )
        
        if isinstance(exc, AuthenticationFailed):
            logger.warning(f"Authentication failed: {request.path}")
            return JsonResponse(
                {'error': '认证失败', 'code': 'authentication_failed'},
                status=401
            )
        
        if isinstance(exc, ValidationError):
            logger.info(f"Validation error: {exc.detail}")
            errors = exc.detail if hasattr(exc, 'detail') else str(exc)
            return JsonResponse(
                {'error': '验证失败', 'errors': errors, 'code': 'validation_error'},
                status=400
            )
        
        if isinstance(exc, APIException):
            logger.error(f"API exception: {type(exc).__name__}: {exc}")
            return JsonResponse(
                {'error': str(exc.detail) if hasattr(exc, 'detail') else str(exc)},
                status=exc.status_code
            )
        
        # Django 核心异常
        if isinstance(exc, ObjectDoesNotExist):
            logger.info(f"Object does not exist: {exc}")
            return JsonResponse(
                {'error': '资源不存在', 'code': 'not_found'},
                status=404
            )
        
        if isinstance(exc, DjangoValidationError):
            logger.info(f"Django validation error: {exc.messages}")
            return JsonResponse(
                {'error': '验证失败', 'errors': exc.messages, 'code': 'validation_error'},
                status=400
            )
        
        if isinstance(exc, (DatabaseError, IntegrityError)):
            logger.error(f"Database error: {type(exc).__name__}: {exc}", exc_info=True)
            return JsonResponse(
                {'error': '数据库操作失败', 'code': 'database_error'},
                status=500
            )
        
        # 其他未预期的异常
        logger.critical(f"Unhandled exception: {type(exc).__name__}: {exc}", exc_info=True)
        
        # 开发环境显示详细信息，生产环境隐藏细节
        from django.conf import settings
        if settings.DEBUG:
            import traceback
            return JsonResponse(
                {
                    'error': f'服务器内部错误：{type(exc).__name__}',
                    'message': str(exc),
                    'traceback': traceback.format_exc()
                },
                status=500
            )
        else:
            return JsonResponse(
                {'error': '服务器内部错误，请稍后重试', 'code': 'internal_server_error'},
                status=500
            )
