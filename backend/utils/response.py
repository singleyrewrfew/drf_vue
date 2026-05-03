from rest_framework.response import Response
from utils.error_codes import ErrorTypes, ERROR_STATUS_MAP


class StandardResponse(Response):
    """
    统一 API 响应格式
    
    设计原则：
    1. 所有数据统一放在 data 字段中
    2. 使用 HTTP 状态码表示请求结果（符合 RESTful 规范）
    3. 分页时：保留 DRF 的分页格式在 data 中
    
    响应格式示例：
    
    成功（单个对象）:
    {
        "message": "操作成功",
        "data": {
            "id": "uuid",
            "title": "文章标题",
            "content": "..."
        }
    }
    HTTP Status: 200
    
    成功（列表，分页）:
    {
        "message": "操作成功",
        "data": {
            "count": 100,
            "next": "/api/contents/?page=2",
            "previous": null,
            "results": [...]
        }
    }
    HTTP Status: 200
    
    错误:
    {
        "message": "错误信息",
        "error": "错误类型",
        "data": null
    }
    HTTP Status: 400/401/403/404/500 等
    """
    
    def __init__(self, data=None, message='操作成功', status=200, error_type=None):
        # 所有数据统一包装在 data 字段中
        response_data = {
            'message': message,
            'data': data,
        }
        
        # 如果是错误响应，添加 error 字段
        if error_type:
            response_data['error'] = error_type
        
        super().__init__(response_data, status=status)


def api_response(data=None, message='操作成功', status=200):
    """
    简化版响应函数
    
    Args:
        data: 返回的数据（放在 data 字段中）
        message: 成功消息
        status: HTTP 状态码
    
    Returns:
        Response: 响应对象
    """
    return StandardResponse(data=data, message=message, status=status)


def api_error(message, error_type=ErrorTypes.BAD_REQUEST, status=None, data=None):
    """
    统一的错误响应
    
    ⚠️ 重要：error_type 应使用 ErrorTypes 常量，避免硬编码字符串
    
    Args:
        message: 错误信息
        error_type: 错误类型（使用 ErrorTypes 常量）
        status: HTTP 状态码（可选，根据 error_type 自动推断）
        data: 额外的错误数据（可选）
    
    Returns:
        Response: 错误响应对象
    
    Example:
        >>> api_error('用户名已存在', ErrorTypes.DUPLICATE_ENTRY)
        >>> api_error('权限不足', ErrorTypes.FORBIDDEN, status=403)
    """
    # 如果没有指定 status，根据 error_type 自动推断
    if status is None:
        status = ERROR_STATUS_MAP.get(error_type, 400)
    
    return StandardResponse(
        data=data,
        message=message,
        status=status,
        error_type=error_type
    )


# ========== 快捷错误响应函数 ==========
# 这些函数封装了常用的错误类型，简化调用代码

def bad_request(message, data=None):
    """400 - 请求错误"""
    return api_error(message, ErrorTypes.BAD_REQUEST, data=data)


def validation_error(message, data=None):
    """400 - 参数验证失败"""
    return api_error(message, ErrorTypes.VALIDATION_ERROR, data=data)


def unauthorized(message='未授权访问', data=None):
    """401 - 未授权"""
    return api_error(message, ErrorTypes.UNAUTHORIZED, data=data)


def token_expired(message='Token 已过期', data=None):
    """401 - Token 过期"""
    return api_error(message, ErrorTypes.TOKEN_EXPIRED, data=data)


def token_invalid(message='Token 无效', data=None):
    """401 - Token 无效"""
    return api_error(message, ErrorTypes.TOKEN_INVALID, data=data)


def forbidden(message='禁止访问', data=None):
    """403 - 禁止访问"""
    return api_error(message, ErrorTypes.FORBIDDEN, data=data)


def insufficient_permissions(message='权限不足', data=None):
    """403 - 权限不足"""
    return api_error(message, ErrorTypes.INSUFFICIENT_PERMISSIONS, data=data)


def account_disabled(message='账户已被禁用', data=None):
    """403 - 账户被禁用"""
    return api_error(message, ErrorTypes.ACCOUNT_DISABLED, data=data)


def not_found(message='资源不存在', data=None):
    """404 - 资源不存在"""
    return api_error(message, ErrorTypes.NOT_FOUND, data=data)


def conflict(message='资源冲突', data=None):
    """409 - 冲突"""
    return api_error(message, ErrorTypes.CONFLICT, data=data)


def duplicate_entry(message='重复记录', data=None):
    """409 - 重复记录"""
    return api_error(message, ErrorTypes.DUPLICATE_ENTRY, data=data)


def payload_too_large(message='文件过大', data=None):
    """413 - 文件过大"""
    return api_error(message, ErrorTypes.PAYLOAD_TOO_LARGE, data=data)


def unsupported_media_type(message='不支持的文件格式', data=None):
    """415 - 不支持的媒体类型"""
    return api_error(message, ErrorTypes.UNSUPPORTED_MEDIA_TYPE, data=data)


def rate_limit_exceeded(message='请求过于频繁', data=None):
    """429 - 速率限制超限"""
    return api_error(message, ErrorTypes.RATE_LIMIT_EXCEEDED, data=data)


def internal_error(message='服务器内部错误', data=None):
    """500 - 内部错误"""
    return api_error(message, ErrorTypes.INTERNAL_ERROR, data=data)


def file_processing_error(message='文件处理失败', data=None):
    """500 - 文件处理错误"""
    return api_error(message, ErrorTypes.FILE_PROCESSING_ERROR, data=data)
