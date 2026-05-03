"""
API 错误代码常量定义

设计原则：
1. 所有错误类型使用常量定义，避免硬编码字符串
2. 错误类型与 HTTP 状态码对应
3. 前端可以通过常量名理解错误含义

使用示例：
    from utils.error_codes import ErrorTypes
    
    return api_error(
        message='权限不足',
        error_type=ErrorTypes.FORBIDDEN,
        status=status.HTTP_403_FORBIDDEN
    )
"""


class ErrorTypes:
    """
    API 错误类型常量
    
    分类说明：
    - 4xx: 客户端错误（请求有问题）
    - 5xx: 服务器错误（服务端有问题）
    
    命名规范：
    - 使用大写蛇形命名法（UPPER_SNAKE_CASE）
    - 名称要语义清晰，见名知意
    """
    
    # ========== 客户端错误 (4xx) ==========
    
    # 400 - 请求错误
    BAD_REQUEST = 'bad_request'                    # 通用请求错误
    VALIDATION_ERROR = 'validation_error'          # 参数验证失败
    INVALID_INPUT = 'invalid_input'                # 输入数据无效
    
    # 401 - 未授权
    UNAUTHORIZED = 'unauthorized'                  # 通用未授权
    TOKEN_EXPIRED = 'token_expired'                # Token 过期
    TOKEN_INVALID = 'token_invalid'                # Token 无效
    MISSING_TOKEN = 'missing_token'                # 缺少 Token
    
    # 403 - 禁止访问
    FORBIDDEN = 'forbidden'                        # 通用禁止访问
    NO_BACKEND_ACCESS = 'no_backend_access'        # 无后台访问权限
    INSUFFICIENT_PERMISSIONS = 'insufficient_permissions'  # 权限不足
    ACCOUNT_DISABLED = 'account_disabled'          # 账户被禁用
    
    # 404 - 资源不存在
    NOT_FOUND = 'not_found'                        # 通用资源不存在
    USER_NOT_FOUND = 'user_not_found'              # 用户不存在
    CONTENT_NOT_FOUND = 'content_not_found'        # 内容不存在
    
    # 409 - 冲突
    CONFLICT = 'conflict'                          # 通用冲突
    DUPLICATE_ENTRY = 'duplicate_entry'            # 重复记录
    
    # 413 - 请求过大
    PAYLOAD_TOO_LARGE = 'payload_too_large'        # 文件过大
    
    # 415 - 不支持的媒体类型
    UNSUPPORTED_MEDIA_TYPE = 'unsupported_media_type'  # 文件格式不支持
    
    # 429 - 请求过多
    TOO_MANY_REQUESTS = 'too_many_requests'        # 请求频率过高
    RATE_LIMIT_EXCEEDED = 'rate_limit_exceeded'    # 速率限制超限
    
    # ========== 服务器错误 (5xx) ==========
    
    # 500 - 内部错误
    INTERNAL_ERROR = 'internal_error'              # 通用服务器错误
    DATABASE_ERROR = 'database_error'              # 数据库错误
    FILE_PROCESSING_ERROR = 'file_processing_error'  # 文件处理错误
    
    # 502 - 网关错误
    BAD_GATEWAY = 'bad_gateway'                    # 上游服务错误
    
    # 503 - 服务不可用
    SERVICE_UNAVAILABLE = 'service_unavailable'    # 服务维护中
    
    # 504 - 网关超时
    GATEWAY_TIMEOUT = 'gateway_timeout'            # 上游服务超时


# 错误类型到 HTTP 状态码的映射（便于快速查找和验证）
ERROR_STATUS_MAP = {
    # 400 系列
    ErrorTypes.BAD_REQUEST: 400,
    ErrorTypes.VALIDATION_ERROR: 400,
    ErrorTypes.INVALID_INPUT: 400,
    
    # 401 系列
    ErrorTypes.UNAUTHORIZED: 401,
    ErrorTypes.TOKEN_EXPIRED: 401,
    ErrorTypes.TOKEN_INVALID: 401,
    ErrorTypes.MISSING_TOKEN: 401,
    
    # 403 系列
    ErrorTypes.FORBIDDEN: 403,
    ErrorTypes.NO_BACKEND_ACCESS: 403,
    ErrorTypes.INSUFFICIENT_PERMISSIONS: 403,
    ErrorTypes.ACCOUNT_DISABLED: 403,
    
    # 404 系列
    ErrorTypes.NOT_FOUND: 404,
    ErrorTypes.USER_NOT_FOUND: 404,
    ErrorTypes.CONTENT_NOT_FOUND: 404,
    
    # 其他 4xx
    ErrorTypes.CONFLICT: 409,
    ErrorTypes.DUPLICATE_ENTRY: 409,
    ErrorTypes.PAYLOAD_TOO_LARGE: 413,
    ErrorTypes.UNSUPPORTED_MEDIA_TYPE: 415,
    ErrorTypes.TOO_MANY_REQUESTS: 429,
    ErrorTypes.RATE_LIMIT_EXCEEDED: 429,
    
    # 500 系列
    ErrorTypes.INTERNAL_ERROR: 500,
    ErrorTypes.DATABASE_ERROR: 500,
    ErrorTypes.FILE_PROCESSING_ERROR: 500,
    ErrorTypes.BAD_GATEWAY: 502,
    ErrorTypes.SERVICE_UNAVAILABLE: 503,
    ErrorTypes.GATEWAY_TIMEOUT: 504,
}
