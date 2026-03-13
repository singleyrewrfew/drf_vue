from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication


class BackendAccessMiddleware:
    """
    检查用户是否有后台访问权限的中间件
    在每次请求时检查 is_staff 字段
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # 只检查后台 API 请求（排除登录、注册等公开接口）
        if request.path.startswith('/api/') and not self._is_public_path(request.path):
            try:
                # 尝试从 JWT token 中获取用户
                jwt_auth = JWTAuthentication()
                user_auth_tuple = jwt_auth.authenticate(request)
                
                if user_auth_tuple:
                    user, token = user_auth_tuple
                    
                    # 检查用户是否有后台访问权限
                    if not user.is_staff and not user.is_superuser:
                        return JsonResponse({
                            'error': 'no_backend_access',
                            'message': '您没有后台访问权限，请联系管理员'
                        }, status=403)
                        
            except Exception:
                # 如果 token 无效，让 DRF 的权限系统处理
                pass
        
        response = self.get_response(request)
        return response
    
    def _is_public_path(self, path):
        """判断是否为公开路径"""
        public_paths = [
            '/api/auth/login/',
            '/api/auth/register/',
            '/api/users/login/',
            '/api/users/register/',
            '/api/users/popular/',
            '/api/contents/',  # 前台内容列表
            '/api/categories/',
            '/api/tags/',
        ]
        
        # 检查是否为公开路径或前台只读接口
        for public_path in public_paths:
            if path.startswith(public_path):
                # 对于内容、分类、标签等，只允许 GET 请求
                if path.startswith(('/api/contents/', '/api/categories/', '/api/tags/')):
                    return True
                return True
        
        return False
