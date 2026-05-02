"""
缓存工具函数

基于 redis-py 的统一缓存操作，不依赖 Django Cache API。

所有缓存读写、Pub/Sub、SCAN 操作均通过 get_redis_client() 获取客户端，
避免 Django Cache API 的自动前缀和版本号导致的键名不一致问题。
"""

import json
import logging

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


def invalidate_pattern(pattern: str):
    """
    使匹配模式的所有缓存失效

    使用 Redis SCAN 命令安全地查找并删除匹配的键。

    Args:
        pattern: 缓存键模式（不含前缀，如 'categories:list'）
    """
    try:
        client = get_redis_client()
        full_pattern = f'{settings.CACHE_KEY_PREFIX}:{pattern}*'
        cursor = 0
        while True:
            cursor, keys = client.scan(cursor, match=full_pattern, count=100)
            if keys:
                client.delete(*keys)
            if cursor == 0:
                break
    except Exception:
        pass


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
