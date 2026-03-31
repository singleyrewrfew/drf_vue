from django.urls import path
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
import time


def health_check(request):
    start_time = time.time()
    
    health_status = {
        'status': 'healthy',
        'timestamp': time.time(),
        'services': {}
    }
    
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
        health_status['services']['database'] = 'healthy'
    except Exception as e:
        health_status['services']['database'] = f'unhealthy: {str(e)}'
        health_status['status'] = 'unhealthy'
    
    try:
        cache.set('health_check', 'ok', 1)
        if cache.get('health_check') == 'ok':
            health_status['services']['redis'] = 'healthy'
        else:
            health_status['services']['redis'] = 'unhealthy: cache test failed'
            health_status['status'] = 'unhealthy'
    except Exception as e:
        health_status['services']['redis'] = f'unhealthy: {str(e)}'
        health_status['status'] = 'unhealthy'
    
    health_status['response_time_ms'] = int((time.time() - start_time) * 1000)
    
    status_code = 200 if health_status['status'] == 'healthy' else 503
    return JsonResponse(health_status, status=status_code)


def readiness_check(request):
    return JsonResponse({'status': 'ready'})


def liveness_check(request):
    return JsonResponse({'status': 'alive'})


urlpatterns = [
    path('', health_check, name='health-check'),
    path('ready/', readiness_check, name='readiness-check'),
    path('live/', liveness_check, name='liveness-check'),
]
