"""
数据库连接池监控工具

提供数据库连接状态的监控和诊断功能。
"""
import logging
from django.db import connection
from utils.cache_utils import cache_get, cache_set

logger = logging.getLogger(__name__)


def get_connection_info():
    """
    获取当前数据库连接信息
    
    Returns:
        dict: 连接信息字典
    """
    info = {
        'connected': False,
        'in_atomic_block': False,
        'connection_config': {},
    }
    
    try:
        # 检查连接状态
        if connection.connection:
            info['connected'] = True
            
            # 获取连接配置
            settings_dict = connection.settings_dict
            info['connection_config'] = {
                'engine': settings_dict.get('ENGINE'),
                'host': settings_dict.get('HOST'),
                'port': settings_dict.get('PORT'),
                'name': settings_dict.get('NAME'),
                'conn_max_age': settings_dict.get('CONN_MAX_AGE', 0),
                'conn_health_checks': settings_dict.get('CONN_HEALTH_CHECKS', False),
            }
            
            # 检查是否在事务中
            info['in_atomic_block'] = connection.in_atomic_block
            
            # 对于 MySQL，获取更多信息
            if 'mysql' in settings_dict.get('ENGINE', '').lower():
                try:
                    with connection.cursor() as cursor:
                        # 获取线程 ID
                        cursor.execute('SELECT CONNECTION_ID()')
                        info['thread_id'] = cursor.fetchone()[0]
                        
                        # 获取当前连接状态
                        cursor.execute('SHOW STATUS LIKE "Threads_connected"')
                        result = cursor.fetchone()
                        if result:
                            info['total_connections'] = int(result[1])
                        
                        # 获取 wait_timeout
                        cursor.execute('SHOW VARIABLES LIKE "wait_timeout"')
                        result = cursor.fetchone()
                        if result:
                            info['wait_timeout'] = int(result[1])
                            
                except Exception as e:
                    logger.warning(f"获取 MySQL 连接信息失败: {e}")
        
        return info
        
    except Exception as e:
        logger.error(f"获取连接信息失败: {e}")
        info['error'] = str(e)
        return info


def check_connection_health():
    """
    检查数据库连接健康状态
    
    Returns:
        dict: 健康检查结果
    """
    result = {
        'healthy': False,
        'response_time_ms': 0,
        'details': {},
    }
    
    import time
    start_time = time.time()
    
    try:
        # 执行简单查询测试连接
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
            cursor.fetchone()
        
        elapsed_ms = (time.time() - start_time) * 1000
        result['healthy'] = True
        result['response_time_ms'] = round(elapsed_ms, 2)
        result['details']['message'] = '连接正常'
        
        # 获取连接信息
        conn_info = get_connection_info()
        result['details']['connection_info'] = conn_info
        
    except Exception as e:
        elapsed_ms = (time.time() - start_time) * 1000
        result['healthy'] = False
        result['response_time_ms'] = round(elapsed_ms, 2)
        result['details']['error'] = str(e)
        logger.error(f"数据库健康检查失败: {e}")
    
    return result


def monitor_connection_pool():
    """
    监控连接池状态（需要缓存支持）
    
    记录连接使用情况，用于分析和优化。
    
    Returns:
        dict: 连接池统计信息
    """
    stats = {
        'total_requests': 0,
        'reused_connections': 0,
        'new_connections': 0,
        'health_check_failures': 0,
    }
    
    try:
        # 从缓存获取统计数据
        stats_key = 'db_connection_stats'
        cached_stats = cache_get(stats_key)
        
        if cached_stats:
            stats.update(cached_stats)
        
        # 获取当前连接状态
        conn_info = get_connection_info()
        stats['current_connection'] = conn_info
        
        # 计算复用率
        if stats['total_requests'] > 0:
            stats['reuse_rate'] = round(
                stats['reused_connections'] / stats['total_requests'] * 100, 
                2
            )
        else:
            stats['reuse_rate'] = 0
        
        return stats
        
    except Exception as e:
        logger.error(f"监控连接池失败: {e}")
        stats['error'] = str(e)
        return stats


def record_connection_usage(reused: bool, health_check_failed: bool = False):
    """
    记录连接使用情况
    
    Args:
        reused: 是否复用了连接
        health_check_failed: 健康检查是否失败
    """
    try:
        stats_key = 'db_connection_stats'
        
        # 获取现有统计
        stats = cache_get(stats_key, {
            'total_requests': 0,
            'reused_connections': 0,
            'new_connections': 0,
            'health_check_failures': 0,
        })
        
        # 更新统计
        stats['total_requests'] += 1
        if reused:
            stats['reused_connections'] += 1
        else:
            stats['new_connections'] += 1
        
        if health_check_failed:
            stats['health_check_failures'] += 1
        
        # 保存回缓存（1小时过期）
        cache_set(stats_key, stats, timeout=3600)
        
    except Exception as e:
        logger.warning(f"记录连接使用失败: {e}")


def reset_connection_stats():
    """重置连接池统计"""
    try:
        from utils.cache_utils import cache_delete
        cache_delete('db_connection_stats')
        logger.info("连接池统计已重置")
    except Exception as e:
        logger.error(f"重置统计失败: {e}")


def get_connection_recommendations():
    """
    获取连接池配置建议
    
    Returns:
        list: 建议列表
    """
    recommendations = []
    
    try:
        conn_info = get_connection_info()
        config = conn_info.get('connection_config', {})
        
        conn_max_age = config.get('conn_max_age', 0)
        health_checks = config.get('conn_health_checks', False)
        
        # 检查 CONN_MAX_AGE
        if conn_max_age == 0:
            recommendations.append({
                'level': 'warning',
                'message': 'CONN_MAX_AGE 为 0，未启用连接持久化',
                'suggestion': '生产环境建议设置为 300-600 秒以提升性能'
            })
        elif conn_max_age > 600:
            recommendations.append({
                'level': 'warning',
                'message': f'CONN_MAX_AGE 设置为 {conn_max_age} 秒，可能过长',
                'suggestion': '建议降低到 300-600 秒以避免连接泄漏'
            })
        
        # 检查健康检查
        if not health_checks and conn_max_age > 0:
            recommendations.append({
                'level': 'info',
                'message': '启用了连接持久化但未开启健康检查',
                'suggestion': '建议设置 DB_CONN_HEALTH_CHECKS=True 以提高稳定性'
            })
        
        # 检查 wait_timeout
        wait_timeout = conn_info.get('wait_timeout')
        if wait_timeout and conn_max_age > 0:
            if wait_timeout <= conn_max_age:
                recommendations.append({
                    'level': 'error',
                    'message': f'MySQL wait_timeout ({wait_timeout}s) <= CONN_MAX_AGE ({conn_max_age}s)',
                    'suggestion': '增加 MySQL wait_timeout 或降低 CONN_MAX_AGE'
                })
        
        if not recommendations:
            recommendations.append({
                'level': 'success',
                'message': '连接池配置良好',
                'suggestion': '无需调整'
            })
        
        return recommendations
        
    except Exception as e:
        logger.error(f"获取建议失败: {e}")
        return [{
            'level': 'error',
            'message': f'无法获取建议: {str(e)}',
            'suggestion': '检查数据库连接'
        }]
