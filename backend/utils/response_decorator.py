import functools
from utils.response import StandardResponse


def auto_response(func):
    """
    自动包装响应装饰器
    
    如果函数返回的不是 Response 对象，则自动使用 StandardResponse 包装
    这样可以简化 ViewSet 的代码，无需手动调用 StandardResponse
    
    使用示例：
    @auto_response
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return serializer.data  # 自动包装为 StandardResponse(serializer.data)
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        
        # 如果已经是 Response 对象，直接返回
        from rest_framework.response import Response
        if isinstance(result, Response):
            return result
        
        # 否则自动包装
        return StandardResponse(result)
    
    return wrapper
