from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger('picBed')


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        error_data = {
            'success': False,
            'error': {
                'code': response.status_code,
                'message': get_error_message(response.data),
                'details': response.data
            }
        }
        response.data = error_data
    
    else:
        logger.error(f'Unhandled exception: {exc}', exc_info=True)
        response = Response(
            {
                'success': False,
                'error': {
                    'code': 500,
                    'message': '服务器内部错误',
                    'details': str(exc)
                }
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return response


def get_error_message(data):
    if isinstance(data, dict):
        if 'detail' in data:
            return str(data['detail'])
        elif 'message' in data:
            return str(data['message'])
        else:
            messages = []
            for key, value in data.items():
                if isinstance(value, list):
                    messages.append(f'{key}: {", ".join(str(v) for v in value)}')
                else:
                    messages.append(f'{key}: {value}')
            return '; '.join(messages)
    elif isinstance(data, list):
        return '; '.join(str(item) for item in data)
    else:
        return str(data)
