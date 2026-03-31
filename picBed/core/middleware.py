import logging
import time
import uuid
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('picBed')


class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.request_id = str(uuid.uuid4())
        request.start_time = time.time()
        
        log_data = {
            'method': request.method,
            'path': request.path,
            'query_params': dict(request.GET),
            'user_id': getattr(request.user, 'id', None) if hasattr(request, 'user') else None,
            'ip': self.get_client_ip(request),
        }
        
        logger.info(
            f'Request started: {request.method} {request.path}',
            extra={
                'request_id': request.request_id,
                'user_id': log_data['user_id'],
                'extra_data': log_data
            }
        )
    
    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            duration_ms = int(duration * 1000)
            
            log_data = {
                'method': request.method,
                'path': request.path,
                'status_code': response.status_code,
                'duration_ms': duration_ms,
                'user_id': getattr(request.user, 'id', None) if hasattr(request, 'user') else None,
            }
            
            logger.info(
                f'Request completed: {request.method} {request.path} - {response.status_code} ({duration_ms}ms)',
                extra={
                    'request_id': getattr(request, 'request_id', None),
                    'user_id': log_data['user_id'],
                    'extra_data': log_data
                }
            )
        
        if hasattr(request, 'request_id'):
            response['X-Request-ID'] = request.request_id
        
        return response
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
