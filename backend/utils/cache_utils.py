"""
缓存工具函数

提供常用的缓存操作功能。
"""

from django.core.cache import cache
from django.conf import settings


def get_cache_key(prefix: str, *args) -> str:
    """
    生成缓存键

    Args:
        prefix: 缓存键前缀
        *args: 缓存键组成部分

    Returns:
        str: 完整的缓存键
    """
    parts = [settings.CACHE_KEY_PREFIX, prefix] + [str(arg) for arg in args]
    return ':'.join(parts)


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
            result = cache.get(cache_key)
            if result is not None:
                return result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, timeout or settings.REDIS_CACHE_TIMEOUT)
            return result
        return wrapper
    return decorator


def invalidate_cache(key_prefix: str, *args):
    """
    使缓存失效

    Args:
        key_prefix: 缓存键前缀
        *args: 缓存键组成部分
    """
    cache_key = get_cache_key(key_prefix, *args)
    cache.delete(cache_key)


def invalidate_pattern(pattern: str):
    """
    使匹配模式的所有缓存失效

    使用 Redis SCAN 命令安全地查找并删除匹配的键。

    Args:
        pattern: 缓存键模式（不含前缀，如 'categories:list'）
    """
    try:
        client = cache.client.get_client(write=True)
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


def get_or_set(key: str, func, timeout: int = None):
    """
    获取缓存，如果不存在则设置

    Args:
        key: 缓存键
        func: 获取数据的函数
        timeout: 缓存超时时间（秒）

    Returns:
        缓存的数据
    """
    return cache.get_or_set(key, func, timeout or settings.REDIS_CACHE_TIMEOUT)
