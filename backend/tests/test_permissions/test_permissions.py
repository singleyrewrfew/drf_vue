"""
权限测试

测试用户权限类的功能
"""
import pytest
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView

from apps.users.models import User
from apps.users.permissions import IsAdminUser, IsEditorUser, IsOwnerOrAdmin


@pytest.mark.unit
class TestIsAdminUserPermission:
    """管理员权限测试类"""
    
    def test_admin_has_permission(self):
        """测试管理员有权限"""
        permission = IsAdminUser()
        
        # 创建管理员用户
        admin = User(username='admin', is_staff=True, is_superuser=True)
        
        # 模拟请求
        factory = APIRequestFactory()
        request = factory.get('/api/test')
        request.user = admin
        
        view = APIView()
        
        # is_admin 是计算属性，基于 is_superuser 或角色
        assert permission.has_permission(request, view) is True
    
    def test_normal_user_no_permission(self):
        """测试普通用户无权限"""
        permission = IsAdminUser()
        
        # 创建普通用户
        user = User(username='user', is_staff=False, is_superuser=False)
        
        factory = APIRequestFactory()
        request = factory.get('/api/test')
        request.user = user
        
        view = APIView()
        
        assert permission.has_permission(request, view) is False
    
    def test_anonymous_user_no_permission(self):
        """测试匿名用户无权限"""
        permission = IsAdminUser()
        
        from django.contrib.auth.models import AnonymousUser
        
        factory = APIRequestFactory()
        request = factory.get('/api/test')
        request.user = AnonymousUser()
        
        view = APIView()
        
        assert permission.has_permission(request, view) is False


@pytest.mark.unit
class TestIsEditorUserPermission:
    """编辑者权限测试类"""
    
    def test_editor_has_permission(self, db):
        """测试编辑者有权限"""
        permission = IsEditorUser()
        
        # 创建编辑者用户（需要设置 role）
        from apps.roles.models import Role
        editor_role, _ = Role.objects.get_or_create(code='editor', defaults={'name': '编辑者'})
        editor = User(username='editor', is_staff=True, role=editor_role)
        
        factory = APIRequestFactory()
        request = factory.get('/api/test')
        request.user = editor
        
        view = APIView()
        
        # is_editor 是计算属性，基于角色代码
        assert permission.has_permission(request, view) is True
    
    def test_normal_user_no_permission(self):
        """测试普通用户无权限"""
        permission = IsEditorUser()
        
        user = User(username='user', is_staff=False)
        
        factory = APIRequestFactory()
        request = factory.get('/api/test')
        request.user = user
        
        view = APIView()
        
        assert permission.has_permission(request, view) is False


@pytest.mark.unit
class TestIsOwnerOrAdminPermission:
    """所有者或管理员权限测试类"""
    
    def test_admin_can_access_any_object(self):
        """测试管理员可以访问任何对象"""
        permission = IsOwnerOrAdmin()
        
        # 创建管理员
        admin = User(username='admin', is_staff=True, is_superuser=True)
        
        # 创建测试对象（模拟有 author 属性的对象）
        class MockObject:
            def __init__(self, author):
                self.author = author
        
        other_user = User(username='other', is_staff=False)
        obj = MockObject(author=other_user)
        
        factory = APIRequestFactory()
        request = factory.get('/api/test')
        request.user = admin
        
        view = APIView()
        
        assert permission.has_object_permission(request, view, obj) is True
    
    def test_owner_can_access_own_object(self):
        """测试所有者可以访问自己的对象"""
        permission = IsOwnerOrAdmin()
        
        # 创建作者
        author = User(username='author', is_staff=False)
        
        class MockObject:
            def __init__(self, author):
                self.author = author
        
        obj = MockObject(author=author)
        
        factory = APIRequestFactory()
        request = factory.get('/api/test')
        request.user = author
        
        view = APIView()
        
        assert permission.has_object_permission(request, view, obj) is True
    
    def test_other_user_cannot_access(self):
        """测试其他用户不能访问"""
        permission = IsOwnerOrAdmin()
        
        # 创建作者和其他用户
        author = User(username='author', is_staff=False)
        other_user = User(username='other', is_staff=False)
        
        class MockObject:
            def __init__(self, author):
                self.author = author
        
        obj = MockObject(author=author)
        
        factory = APIRequestFactory()
        request = factory.get('/api/test')
        request.user = other_user
        
        view = APIView()
        
        assert permission.has_object_permission(request, view, obj) is False
    
    def test_check_user_object(self):
        """测试检查 user 属性的对象"""
        permission = IsOwnerOrAdmin()
        
        # 创建用户对象（有 user 属性）
        user = User(username='user', is_staff=False)
        
        class MockObject:
            def __init__(self, user):
                self.user = user
        
        obj = MockObject(user=user)
        
        factory = APIRequestFactory()
        request = factory.get('/api/test')
        request.user = user
        
        view = APIView()
        
        assert permission.has_object_permission(request, view, obj) is True
    
    def test_check_uploader_object(self):
        """测试检查 uploader 属性的对象"""
        permission = IsOwnerOrAdmin()
        
        # 创建上传者对象
        uploader = User(username='uploader', is_staff=False)
        
        class MockObject:
            def __init__(self, uploader):
                self.uploader = uploader
        
        obj = MockObject(uploader=uploader)
        
        factory = APIRequestFactory()
        request = factory.get('/api/test')
        request.user = uploader
        
        view = APIView()
        
        assert permission.has_object_permission(request, view, obj) is True
