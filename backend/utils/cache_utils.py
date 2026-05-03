"""
缓存工具函数

基于 redis-py 的统一缓存操作，不依赖 Django Cache API。

所有缓存读写、Pub/Sub、SCAN 操作均通过 get_redis_client() 获取客户端，
避免 Django Cache API 的自动前缀和版本号导致的键名不一致问题。
"""

import hashlib
import json
import logging
import time

import redis
from django.conf import settings

logger = logging.getLogger(__name__)

_client = None


def get_redis_client():
    """
    获取 Redis 客户端（单例，复用连接池）

    Returns:
        redis.Redis: Redis 客户端实例
    """
    global _client
    if _client is None:
        _client = redis.Redis.from_url(settings.REDIS_URL)
    return _client


def get_cache_key(prefix: str, *args) -> str:
    """
    生成缓存键

    Args:
        prefix: 缓存键前缀
        *args: 缓存键组成部分

    Returns:
        str: 完整的缓存键，格式为 cms:prefix:arg1:arg2:...
    """
    parts = [settings.CACHE_KEY_PREFIX, prefix] + [str(arg) for arg in args]
    return ':'.join(parts)


def cache_get(key: str, default=None):
    """
    获取缓存值

    Args:
        key: 缓存键
        default: 键不存在时的默认值

    Returns:
        缓存的数据，不存在则返回 default
    """
    client = get_redis_client()
    data = client.get(key)
    if data is None:
        return default
    try:
        return json.loads(data)
    except (json.JSONDecodeError, TypeError):
        return default


def cache_set(key: str, value, timeout: int = None):
    """
    设置缓存值

    Args:
        key: 缓存键
        value: 要缓存的数据（必须可 JSON 序列化）
        timeout: 过期时间（秒），默认使用 CACHE_TTL['DEFAULT']
    """
    client = get_redis_client()
    ttl = timeout or settings.CACHE_TTL['DEFAULT']
    client.set(key, json.dumps(value, ensure_ascii=False), ex=ttl)


def cache_delete(key: str):
    """
    删除缓存

    Args:
        key: 缓存键
    """
    client = get_redis_client()
    client.delete(key)


def cache_get_or_set(key: str, func, timeout: int = None):
    """
    获取缓存，如果不存在则调用 func 设置

    Args:
        key: 缓存键
        func: 获取数据的函数
        timeout: 过期时间（秒）

    Returns:
        缓存的数据
    """
    result = cache_get(key)
    if result is not None:
        return result
    result = func()
    cache_set(key, result, timeout)
    return result


def invalidate_cache(key_prefix: str, *args):
    """
    使指定缓存失效

    Args:
        key_prefix: 缓存键前缀
        *args: 缓存键组成部分
    """
    cache_key = get_cache_key(key_prefix, *args)
    cache_delete(cache_key)


def invalidate_pattern(pattern: str) -> int:
    """
    使匹配模式的所有缓存失效

    使用 Redis SCAN 命令安全地查找并删除匹配的键。

    Args:
        pattern: 缓存键模式（不含前缀，如 'categories:list'）
        
    Returns:
        int: 删除的键数量
    """
    try:
        client = get_redis_client()
        full_pattern = f'{settings.CACHE_KEY_PREFIX}:{pattern}*'
        cursor = 0
        deleted_count = 0
        while True:
            cursor, keys = client.scan(cursor, match=full_pattern, count=100)
            if keys:
                deleted_count += client.delete(*keys)
            if cursor == 0:
                break
        return deleted_count
    except Exception as e:
        logger.error(f"Failed to invalidate cache pattern '{pattern}': {e}")
        return 0


def cache_result(key_prefix: str, timeout: int = None):
    """
    缓存函数结果的装饰器

    Args:
        key_prefix: 缓存键前缀
        timeout: 缓存超时时间（秒），默认使用全局配置

    Returns:
        装饰器函数
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            cache_key = get_cache_key(key_prefix, *args[:2] if args else ())
            result = cache_get(cache_key)
            if result is not None:
                return result
            result = func(*args, **kwargs)
            cache_set(cache_key, result, timeout)
            return result
        return wrapper
    return decorator


# ========== 智能缓存功能 ==========

def generate_smart_cache_key(prefix: str, params: dict, max_length: int = 100) -> str:
    """
    智能缓存键生成
    
    - 对长参数进行哈希，避免缓存键过长
    - 排序参数确保一致性
    - 支持自定义最大长度
    
    Args:
        prefix: 缓存键前缀
        params: 查询参数字典
        max_length: 参数字符串最大长度，超过则使用哈希
        
    Returns:
        str: 优化后的缓存键
        
    Example:
        >>> generate_smart_cache_key('contents:list', {'page': 1, 'category': 'python'})
        'cms:contents:list:category=python&page=1'
        
        >>> # 长参数会自动哈希
        >>> generate_smart_cache_key('search', {'q': 'very long search query...' * 10})
        'cms:search:a3f5b8c2'
    """
    # 排序参数确保一致性
    sorted_params = sorted(params.items())
    param_str = '&'.join(f'{k}={v}' for k, v in sorted_params if v)
    
    # 如果参数过长，使用哈希
    if len(param_str) > max_length:
        param_hash = hashlib.md5(param_str.encode()).hexdigest()[:8]
        return get_cache_key(prefix, param_hash)
    
    return get_cache_key(prefix, param_str) if param_str else get_cache_key(prefix)


def get_or_set_cache(key: str, func, timeout: int = None, lock_timeout: int = 10):
    """
    缓存 getter/setter，使用分布式锁避免竞态条件
    
    当多个请求同时请求同一个不存在的缓存时，只有一个请求会执行 func，
    其他请求等待结果，避免“缓存击穿”问题。
    
    Args:
        key: 缓存键
        func: 获取数据的可调用对象（无参数）
        timeout: 缓存过期时间（秒）
        lock_timeout: 锁超时时间（秒），防止死锁
        
    Returns:
        缓存的数据
        
    Example:
        >>> data = get_or_set_cache(
        ...     'my_key',
        ...     lambda: expensive_database_query(),
        ...     timeout=300
        ... )
    """
    client = get_redis_client()
    
    # 尝试获取缓存
    result = cache_get(key)
    if result is not None:
        return result
    
    # 使用 Redis 锁防止竞态条件
    lock_key = f"{key}:lock"
    acquired = client.set(lock_key, time.time(), nx=True, ex=lock_timeout)
    
    if acquired:
        try:
            # 再次检查缓存（双重检查锁定）
            result = cache_get(key)
            if result is not None:
                return result
            
            # 执行函数获取数据
            result = func()
            cache_set(key, result, timeout)
            return result
        finally:
            # 释放锁
            client.delete(lock_key)
    else:
        # 等待其他请求完成
        for _ in range(lock_timeout * 10):  # 最多等待 lock_timeout 秒
            time.sleep(0.1)
            result = cache_get(key)
            if result is not None:
                return result
        
        # 超时后直接执行（降级策略）
        logger.warning(f"Cache lock timeout for key: {key}, executing function directly")
        result = func()
        cache_set(key, result, timeout)
        return result


def calculate_dynamic_ttl(base_ttl: int, hit_count: int = None, last_access: float = None) -> int:
    """
    根据热度动态计算缓存 TTL
    
    - 高频访问的内容使用更长的 TTL
    - 低频访问的内容使用较短的 TTL
    
    Args:
        base_ttl: 基础 TTL（秒）
        hit_count: 访问次数（可选）
        last_access: 最后访问时间戳（可选）
        
    Returns:
        int: 动态计算的 TTL（秒）
        
    Example:
        >>> # 热门内容：TTL 延长 2 倍
        >>> calculate_dynamic_ttl(300, hit_count=1000)
        600
        
        >>> # 冷门内容：TTL 缩短为 0.5 倍
        >>> calculate_dynamic_ttl(300, hit_count=5)
        150
    """
    if hit_count is None:
        return base_ttl
    
    # 根据访问次数调整 TTL
    if hit_count > 1000:
        multiplier = 2.0  # 非常热门
    elif hit_count > 100:
        multiplier = 1.5  # 热门
    elif hit_count > 10:
        multiplier = 1.0  # 正常
    else:
        multiplier = 0.5  # 冷门
    
    return int(base_ttl * multiplier)
