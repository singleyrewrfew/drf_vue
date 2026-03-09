from rest_framework.response import Response


def success_response(data=None, message='操作成功', status=200):
    return Response({
        'code': 0,
        'message': message,
        'data': data
    }, status=status)


def error_response(message='操作失败', code=1, status=400):
    return Response({
        'code': code,
        'message': message,
        'data': None
    }, status=status)
