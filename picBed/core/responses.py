from rest_framework.response import Response
from rest_framework import status


class APIResponse:
    @staticmethod
    def success(data=None, message='操作成功', status_code=status.HTTP_200_OK):
        return Response(
            {
                'success': True,
                'message': message,
                'data': data
            },
            status=status_code
        )
    
    @staticmethod
    def error(message='操作失败', error_code=None, status_code=status.HTTP_400_BAD_REQUEST, details=None):
        response_data = {
            'success': False,
            'error': {
                'message': message,
                'code': error_code or status_code,
            }
        }
        if details:
            response_data['error']['details'] = details
        
        return Response(response_data, status=status_code)
    
    @staticmethod
    def paginated(data, page, page_size, total_count, message='查询成功'):
        return Response(
            {
                'success': True,
                'message': message,
                'data': {
                    'items': data,
                    'pagination': {
                        'page': page,
                        'page_size': page_size,
                        'total_count': total_count,
                        'total_pages': (total_count + page_size - 1) // page_size
                    }
                }
            }
        )
