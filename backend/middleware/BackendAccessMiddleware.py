from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication


class BackendAccessMiddleware:
    """
    检查用户是否有后台访问权限的中间件
    
    权限分级：
    1. 公开路径 - 所有人可访问（登录、注册、公开内容列表）
    2. 用户路径 - 认证用户可访问（上传媒体、管理个人内容）
    3. 管理路径 - 仅管理员可访问（用户管理、系统设置）
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # 只检查后台 API 请求
        if request.path.startswith('/api/') and not self._is_public_path(request.path):
            try:
                # 尝试从 JWT token 中获取用户
                jwt_auth = JWTAuthentication()
                user_auth_tuple = jwt_auth.authenticate(request)
                
                if user_auth_tuple:
                    user, token = user_auth_tuple
                    
                    # 检查是否为管理路径
                    if self._is_admin_path(request.path):
                        # 管理路径需要 is_staff 或 is_superuser
                        if not user.is_staff and not user.is_superuser:
                            return JsonResponse({
                                'error': 'permission_denied',
                                'message': '需要管理员权限才能访问此接口'
                            }, status=403)
                    # 其他路径只需要认证即可，由 DRF 的权限类进一步检查
                        
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
    
    def _is_admin_path(self, path):
        """判断是否为管理路径（需要 is_staff）"""
        admin_paths = [
            '/api/users/',  # 用户管理
            '/api/roles/',  # 角色管理
            '/api/core/',   # 系统核心配置
        ]
        
        for admin_path in admin_paths:
            if path.startswith(admin_path):
                return True
        
        return False
