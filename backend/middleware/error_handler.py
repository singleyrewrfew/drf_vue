"""
统一错误处理中间件

捕获并统一处理所有未处理的异常，返回标准化的错误响应
"""

from rest_framework.exceptions import (
    ValidationError, 
    PermissionDenied, 
    AuthenticationFailed,
    NotFound
)
from django.http import Http404
import logging
from utils.response import api_error

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware:
    """
    错误处理中间件
    
    自动捕获 ViewSet 中未处理的异常，并转换为统一的错误响应格式
    减少业务代码中的 try-except 样板代码
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            return self._handle_exception(request, e)
    
    def _handle_exception(self, request, exc):
        """
        统一处理各类异常
        
        Args:
            request: HTTP 请求对象
            exc: 异常对象
            
        Returns:
            Response: 统一的错误响应
        """
        # DRF 标准异常
        if isinstance(exc, ValidationError):
            return api_error(
                message=str(exc.detail) if hasattr(exc, 'detail') else str(exc),
                error_type='validation_error',
                status=400
            )
        
        if isinstance(exc, PermissionDenied):
            return api_error(
                message='没有权限执行此操作',
                error_type='permission_denied',
                status=403
            )
        
        if isinstance(exc, AuthenticationFailed):
            return api_error(
                message='认证失败，请检查登录状态',
                error_type='authentication_failed',
                status=401
            )
        
        if isinstance(exc, NotFound) or isinstance(exc, Http404):
            return api_error(
                message='请求的资源不存在',
                error_type='not_found',
                status=404
            )
        
        # 业务逻辑异常（ValueError）
        if isinstance(exc, ValueError):
            return api_error(
                message=str(exc),
                error_type='bad_request',
                status=400
            )
        
        # 其他未预料的异常 - 记录日志并返回通用错误
        logger.error(f'Unhandled exception: {str(exc)}', exc_info=True)
        return api_error(
            message='服务器内部错误，请稍后重试',
            error_type='internal_server_error',
            status=500
        )
