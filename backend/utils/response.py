from rest_framework.response import Response
from utils.error_codes import ErrorTypes, ERROR_STATUS_MAP


class StandardResponse(Response):
    """
    统一 API 响应格式
    
    设计原则：
    1. 所有数据统一放在 data 字段中
    2. 成功和错误都使用统一的包装格式
    3. 分页时：保留 DRF 的分页格式在 data 中
    
    响应格式示例：
    
    成功（单个对象）:
    {
        "code": 0,
        "message": "操作成功",
        "data": {
            "id": "uuid",
            "title": "文章标题",
            "content": "..."
        }
    }
    
    成功（列表，分页）:
    {
        "code": 0,
        "message": "操作成功",
        "data": {
            "count": 100,
            "next": "/api/contents/?page=2",
            "previous": null,
            "results": [...]
        }
    }
    
    错误:
    {
        "code": 400,
        "message": "错误信息",
        "error": "错误类型",
        "data": null
    }
    """
    
    def __init__(self, data=None, message='操作成功', code=0, status=200, error_type=None):
        # 所有数据统一包装在 data 字段中
        response_data = {
            'code': code,
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


def api_error(message, error_type=ErrorTypes.BAD_REQUEST, code=None, status=None, data=None):
    """
    统一的错误响应
    
    ⚠️ 重要：error_type 应使用 ErrorTypes 常量，避免硬编码字符串
    
    Args:
        message: 错误信息
        error_type: 错误类型（使用 ErrorTypes 常量）
        code: 业务错误代码（可选，默认使用 status）
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
        code=code if code is not None else status,
        status=status,
        error_type=error_type
    )
