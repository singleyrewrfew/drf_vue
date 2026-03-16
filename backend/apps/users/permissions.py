from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    管理员权限类
    
    允许条件：
    - 用户已认证
    - 用户是管理员（is_admin 属性为 True）
    """
    def has_permission(self, request, view):
        # 检查用户是否已认证且是管理员
        return request.user and request.user.is_authenticated and request.user.is_admin

class IsEditorUser(permissions.BasePermission):
    """
    编辑者权限类
    
    允许条件：
    - 用户已认证
    - 用户是编辑者（is_editor 属性为 True）
    """
    def has_permission(self, request, view):
        # 检查用户是否已认证且是编辑者
        return request.user and request.user.is_authenticated and request.user.is_editor

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    所有者或管理员权限类
    
    允许条件：
    - 用户是管理员（is_admin 为 True）
    - 用户是对象的所有者（author、user 或 uploader）
    
    使用场景：
    - 文章：检查是否是作者
    - 用户：检查是否是用户自己
    - 媒体：检查是否是上传者
    """
    def has_object_permission(self, request, view, obj):
        # 管理员拥有所有权限
        if request.user.is_admin:
            return True
        # 检查对象是否有 author 属性（文章）
        if hasattr(obj, 'author') and obj.author == request.user:
            return True
        # 检查对象是否有 user 属性（用户）
        if hasattr(obj, 'user') and obj.user == request.user:
            return True
        # 检查对象是否有 uploader 属性（媒体）
        if hasattr(obj, 'uploader') and obj.uploader == request.user:
            return True
        # 其他情况拒绝访问
        return False
