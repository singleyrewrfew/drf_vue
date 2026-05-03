"""
日志敏感信息脱敏工具

提供统一的敏感数据脱敏函数，防止密码、Token、密钥等敏感信息泄露到日志中。

使用示例：
    from utils.log_utils import mask_sensitive_data
    
    # 脱敏字典中的敏感字段
    data = {'username': 'admin', 'password': 'secret123'}
    safe_data = mask_sensitive_data(data)
    logger.info(f'用户登录: {safe_data}')  # 输出: {'username': 'admin', 'password': '***'}
    
    # 脱敏 Token
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
    safe_token = mask_token(token)
    logger.info(f'Token: {safe_token}')  # 输出: 'eyJh...*** (length: 35)'
"""
import logging
import re
from typing import Any, Dict, Union


# 需要脱敏的字段名模式（不区分大小写）
SENSITIVE_FIELD_PATTERNS = [
    r'^password$',           # password
    r'^passwd$',             # passwd
    r'^pwd$',                # pwd
    r'^token$',              # token
    r'^access_token$',       # access_token
    r'^refresh_token$',      # refresh_token
    r'^secret$',             # secret
    r'^secret_key$',         # secret_key
    r'^api_key$',            # api_key
    r'^apikey$',             # apikey
    r'^authorization$',      # authorization
    r'^auth$',               # auth
    r'^credential$',         # credential
    r'^credentials$',        # credentials
]

# 编译正则表达式（提高性能）
SENSITIVE_PATTERNS = [re.compile(pattern, re.IGNORECASE) for pattern in SENSITIVE_FIELD_PATTERNS]


def _is_sensitive_field(field_name: str) -> bool:
    """
    检查字段名是否属于敏感字段
    
    Args:
        field_name: 字段名称
        
    Returns:
        bool: 是否为敏感字段
    """
    return any(pattern.match(field_name) for pattern in SENSITIVE_PATTERNS)


def mask_password(password: str, show_length: bool = True) -> str:
    """
    脱敏密码
    
    Args:
        password: 原始密码
        show_length: 是否显示密码长度
        
    Returns:
        str: 脱敏后的密码字符串
        
    Example:
        >>> mask_password('secret123')
        '*** (length: 8)'
        >>> mask_password('secret123', show_length=False)
        '***'
    """
    if not password:
        return '***'
    if show_length:
        return f'*** (length: {len(password)})'
    return '***'


def mask_token(token: str, show_prefix_length: int = 4) -> str:
    """
    脱敏 Token（JWT、API Key 等）
    
    Args:
        token: 原始 Token
        show_prefix_length: 显示的前缀长度（用于识别 Token 类型）
        
    Returns:
        str: 脱敏后的 Token 字符串
        
    Example:
        >>> mask_token('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...')
        'eyJh...*** (length: 35)'
    """
    if not token:
        return '***'
    
    if len(token) <= show_prefix_length:
        return '***'
    
    prefix = token[:show_prefix_length]
    return f'{prefix}...*** (length: {len(token)})'


def mask_dict(data: Dict[str, Any], show_length: bool = True) -> Dict[str, Any]:
    """
    脱敏字典中的敏感字段
    
    Args:
        data: 原始字典
        show_length: 是否显示敏感字段的长度
        
    Returns:
        dict: 脱敏后的字典（深拷贝，不影响原字典）
        
    Example:
        >>> mask_dict({'username': 'admin', 'password': 'secret123'})
        {'username': 'admin', 'password': '*** (length: 8)'}
    """
    if not isinstance(data, dict):
        return data
    
    masked = {}
    for key, value in data.items():
        if _is_sensitive_field(key):
            # 如果是敏感字段，直接脱敏值
            if isinstance(value, str):
                # 判断是否为 Token 类型（通常较长且包含特殊字符）
                if len(value) > 20 and ('.' in value or '_' in value or '-' in value):
                    masked[key] = mask_token(value)
                else:
                    masked[key] = mask_password(value, show_length)
            elif isinstance(value, dict):
                # 如果值是字典，递归脱敏内部字段
                masked[key] = mask_dict(value, show_length)
            else:
                masked[key] = '***'
        elif isinstance(value, dict):
            # 非敏感字段但值是字典，递归处理
            masked[key] = mask_dict(value, show_length)
        elif isinstance(value, list):
            # 处理列表中的字典
            masked[key] = [
                mask_dict(item, show_length) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            masked[key] = value
    
    return masked


def mask_sensitive_data(data: Any, show_length: bool = True) -> Any:
    """
    通用敏感数据脱敏函数
    
    支持多种数据类型：
    - dict: 脱敏敏感字段
    - str: 如果看起来像 Token 或密码，进行脱敏
    - 其他类型: 原样返回
    
    Args:
        data: 任意类型的数据
        show_length: 是否显示长度信息
        
    Returns:
        Any: 脱敏后的数据
        
    Example:
        >>> mask_sensitive_data({'password': 'secret'})
        {'password': '*** (length: 6)'}
        
        >>> mask_sensitive_data('eyJhbGciOiJIUzI1NiJ9...')
        'eyJh...*** (length: 20)'
    """
    if isinstance(data, dict):
        return mask_dict(data, show_length)
    elif isinstance(data, str):
        # 判断字符串是否可能是敏感信息
        # JWT Token 特征：包含两个点号，长度 > 20
        if data.count('.') >= 2 and len(data) > 20:
            return mask_token(data)
        # API Key 特征：以 sk_、pk_、api_ 等开头
        if re.match(r'^(sk_|pk_|api_|key_|secret_)', data, re.IGNORECASE):
            return mask_token(data)
        # 密码特征：较短的字符串，在特定上下文中
        # （这里不做判断，避免误判）
        return data
    elif isinstance(data, (list, tuple)):
        return type(data)(mask_sensitive_data(item, show_length) for item in data)
    else:
        return data


class SafeLogger:
    """
    安全日志记录器包装类
    
    自动脱敏所有日志消息中的敏感数据
    
    Example:
        >>> logger = SafeLogger(logging.getLogger(__name__))
        >>> logger.info('用户数据: %s', {'password': 'secret'})
        # 实际输出: 用户数据: {'password': '*** (length: 6)'}
    """
    
    def __init__(self, logger, show_length: bool = True):
        """
        初始化安全日志记录器
        
        Args:
            logger: 原始 logger 对象
            show_length: 是否显示敏感数据的长度
        """
        self._logger = logger
        self._show_length = show_length
    
    def _mask_args(self, args):
        """脱敏日志参数"""
        if not args:
            return args
        if isinstance(args, tuple):
            return tuple(mask_sensitive_data(arg, self._show_length) for arg in args)
        return mask_sensitive_data(args, self._show_length)
    
    def debug(self, msg, *args, **kwargs):
        self._logger.debug(msg, *self._mask_args(args), **kwargs)
    
    def info(self, msg, *args, **kwargs):
        self._logger.info(msg, *self._mask_args(args), **kwargs)
    
    def warning(self, msg, *args, **kwargs):
        self._logger.warning(msg, *self._mask_args(args), **kwargs)
    
    def error(self, msg, *args, **kwargs):
        self._logger.error(msg, *self._mask_args(args), **kwargs)
    
    def critical(self, msg, *args, **kwargs):
        self._logger.critical(msg, *self._mask_args(args), **kwargs)
    
    def exception(self, msg, *args, **kwargs):
        self._logger.exception(msg, *self._mask_args(args), **kwargs)


def get_safe_logger(name: str = None, show_length: bool = True) -> SafeLogger:
    """
    获取安全日志记录器
    
    Args:
        name: logger 名称
        show_length: 是否显示敏感数据的长度
        
    Returns:
        SafeLogger: 安全日志记录器
        
    Example:
        >>> logger = get_safe_logger(__name__)
        >>> logger.info('用户登录: %s', {'username': 'admin', 'password': 'secret'})
    """
    import logging
    original_logger = logging.getLogger(name)
    return SafeLogger(original_logger, show_length)


class SensitiveDataFilter(logging.Filter):
    """
    日志敏感数据过滤器
    
    在日志输出前自动脱敏敏感字段，作为最后一道防线。
    即使开发者忘记使用 mask_sensitive_data，也能防止敏感信息泄露。
    
    Example:
        # 在 settings.py 中配置
        LOGGING = {
            'filters': {
                'sensitive_data': {
                    '()': 'utils.log_utils.SensitiveDataFilter',
                },
            },
            'handlers': {
                'file': {
                    'filters': ['sensitive_data'],
                    ...
                },
            },
        }
    """
    
    def filter(self, record):
        """
        过滤并脱敏日志记录中的敏感数据
        
        Args:
            record: 日志记录对象
            
        Returns:
            bool: 始终返回 True（不过滤掉日志，只脱敏）
        """
        try:
            # 脱敏 msg 字段
            if isinstance(record.msg, dict):
                record.msg = mask_dict(record.msg)
            elif isinstance(record.msg, str):
                # 尝试检测字符串中是否包含 JSON 格式的敏感数据
                import json
                import re
                
                # 查找可能的 JSON 对象
                json_pattern = r'\{[^{}]*"(?:password|token|secret|key)[^{}]*:[^{}]*\}'
                matches = re.finditer(json_pattern, record.msg, re.IGNORECASE)
                
                for match in matches:
                    try:
                        json_str = match.group(0)
                        json_obj = json.loads(json_str)
                        masked_obj = mask_dict(json_obj)
                        masked_json = json.dumps(masked_obj)
                        record.msg = record.msg.replace(json_str, masked_json)
                    except (json.JSONDecodeError, Exception):
                        pass  # 如果解析失败，保持原样
            
            # 脱敏 args 字段
            if record.args:
                if isinstance(record.args, dict):
                    record.args = mask_dict(record.args)
                elif isinstance(record.args, (tuple, list)):
                    # 保持原始类型（tuple 或 list）
                    masked_args = [
                        mask_dict(arg) if isinstance(arg, dict) else arg
                        for arg in record.args
                    ]
                    record.args = type(record.args)(masked_args)
        except Exception:
            # 如果脱敏过程出错，不影响日志记录
            pass
        
        return True
