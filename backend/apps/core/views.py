import time
import logging

from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

from utils.cache_utils import get_redis_client

logger = logging.getLogger(__name__)


def _check_database():
    start = time.time()
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
        return {
            'status': 'healthy',
            'response_time_ms': round((time.time() - start) * 1000, 2),
        }
    except Exception as e:
        logger.error(f"健康检查 - 数据库异常: {e}")
        return {
            'status': 'unhealthy',
            'error': str(e),
            'response_time_ms': round((time.time() - start) * 1000, 2),
        }


def _check_redis():
    start = time.time()
    try:
        client = get_redis_client()
        client.ping()
        info = client.info('memory')
        return {
            'status': 'healthy',
            'used_memory_human': info.get('used_memory_human', 'unknown'),
            'response_time_ms': round((time.time() - start) * 1000, 2),
        }
    except Exception as e:
        logger.error(f"健康检查 - Redis 异常: {e}")
        return {
            'status': 'unhealthy',
            'error': str(e),
            'response_time_ms': round((time.time() - start) * 1000, 2),
        }


def _check_celery():
    start = time.time()
    try:
        from celery import current_app
        inspect = current_app.control.inspect(timeout=3)
        active = inspect.active()
        if active is None:
            return {
                'status': 'unhealthy',
                'error': '无可用 Worker',
                'response_time_ms': round((time.time() - start) * 1000, 2),
            }
        worker_count = len(active)
        return {
            'status': 'healthy',
            'workers': worker_count,
            'response_time_ms': round((time.time() - start) * 1000, 2),
        }
    except Exception as e:
        logger.error(f"健康检查 - Celery 异常: {e}")
        return {
            'status': 'unhealthy',
            'error': str(e),
            'response_time_ms': round((time.time() - start) * 1000, 2),
        }


@csrf_exempt
@require_GET
def health_check(request):
    """
    就绪检查：验证所有依赖服务是否可用

    GET /api/health/ → 
        - 200: 全部健康 (status: 'healthy')
        - 503: 部分或全部不健康 (status: 'degraded' 或 'unhealthy')
    
    状态说明:
        - healthy: 所有服务正常
        - degraded: 非关键服务异常（Redis/Celery），但核心功能可用
        - unhealthy: 关键服务异常（Database），系统不可用
    """
    start = time.time()

    # 检查各服务状态
    services = {
        'database': _check_database(),
        'redis': _check_redis(),
        'celery': _check_celery(),
    }

    # 确定整体状态
    db_healthy = services['database']['status'] == 'healthy'
    redis_healthy = services['redis']['status'] == 'healthy'
    celery_healthy = services['celery']['status'] == 'healthy'
    
    if db_healthy:
        # 数据库正常，检查其他服务
        if redis_healthy and celery_healthy:
            overall = 'healthy'
        else:
            # 部分非关键服务异常
            overall = 'degraded'
    else:
        # 数据库异常，系统不可用
        overall = 'unhealthy'

    result = {
        'status': overall,
        'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime()),
        'services': services,
        'response_time_ms': round((time.time() - start) * 1000, 2),
    }

    # 根据状态返回不同的 HTTP 状态码
    status_code = 200 if overall == 'healthy' else 503
    return JsonResponse(result, status=status_code)


@csrf_exempt
@require_GET
def liveness_check(request):
    """
    存活检查：进程是否在运行

    GET /api/health/live/ → 200
    """
    return JsonResponse({'status': 'alive'})
