"""
权限测试

测试用户权限类的功能

作用：验证自定义权限类的正确性，确保权限控制逻辑符合预期
使用：运行 pytest tests/test_permissions/ 执行所有权限测试

测试覆盖的权限类：
    1. IsAdminUser - 管理员权限检查
    2. IsEditorUser - 编辑者权限检查
    3. IsOwnerOrAdmin - 所有者或管理员权限检查

测试场景：
    - 管理员访问各种资源
    - 普通用户访问受限资源
    - 匿名用户访问受保护资源
    - 对象所有者访问自己的资源
    - 非所有者尝试访问他人资源
"""
import pytest
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView

from apps.users.models import User
from apps.users.permissions import IsAdminUser, IsEditorUser, IsOwnerOrAdmin


@pytest.mark.unit
class TestIsAdminUserPermission:
    """
    IsAdminUser 权限类测试
    
    验证管理员权限检查逻辑，确保只有管理员用户可以访问受保护的资源。
    
    测试用例：
        - 管理员用户（is_staff=True, is_superuser=True）应该通过权限检查
        - 普通用户（is_staff=False, is_superuser=False）应该被拒绝
        - 匿名用户（AnonymousUser）应该被拒绝
    
    权限规则：
        - 满足 is_staff 或 is_superuser 任一条件即为管理员
        - 匿名用户永远没有管理员权限
    """
    
    def test_admin_has_permission(self):
        """
        测试管理员用户具有访问权限
        
        验证当用户是管理员（is_staff=True 且 is_superuser=True）时，
        IsAdminUser 权限检查应该返回 True。
        
        测试步骤：
            1. 创建 IsAdminUser 权限实例
            2. 创建管理员用户对象
            3. 模拟 HTTP GET 请求并设置用户
            4. 调用 has_permission 方法验证权限
        
        预期结果：
            - has_permission 返回 True
        """
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
        """
        测试普通用户没有访问权限
        
        验证当用户是普通用户（is_staff=False, is_superuser=False）时，
        IsAdminUser 权限检查应该返回 False。
        
        测试步骤：
            1. 创建 IsAdminUser 权限实例
            2. 创建普通用户对象
            3. 模拟 HTTP GET 请求并设置用户
            4. 调用 has_permission 方法验证权限
        
        预期结果：
            - has_permission 返回 False
        """
        permission = IsAdminUser()
        
        # 创建普通用户
        user = User(username='user', is_staff=False, is_superuser=False)
        
        factory = APIRequestFactory()
        request = factory.get('/api/test')
        request.user = user
        
        view = APIView()
        
        assert permission.has_permission(request, view) is False
    
    def test_anonymous_user_no_permission(self):
        """
        测试匿名用户没有访问权限
        
        验证当用户未登录（AnonymousUser）时，
        IsAdminUser 权限检查应该返回 False。
        
        测试步骤：
            1. 创建 IsAdminUser 权限实例
            2. 创建匿名用户对象
            3. 模拟 HTTP GET 请求并设置匿名用户
            4. 调用 has_permission 方法验证权限
        
        预期结果：
            - has_permission 返回 False
        
        安全意义：
            - 确保未认证用户无法访问需要管理员权限的接口
        """
        permission = IsAdminUser()
        
        from django.contrib.auth.models import AnonymousUser
        
        factory = APIRequestFactory()
        request = factory.get('/api/test')
        request.user = AnonymousUser()
        
        view = APIView()
        
        assert permission.has_permission(request, view) is False


@pytest.mark.unit
class TestIsEditorUserPermission:
    """
    IsEditorUser 权限类测试
    
    验证编辑者权限检查逻辑，确保只有编辑者角色可以访问特定资源。
    
    测试用例：
        - 编辑者用户（role='editor'）应该通过权限检查
        - 普通用户应该被拒绝
    
    权限规则：
        - 用户的角色代码为 'editor' 或 'admin' 时具有编辑权限
        - 需要通过 Role 模型关联来设置用户角色
    """
    
    def test_editor_has_permission(self, db):
        """
        测试编辑者用户具有访问权限
        
        验证当用户拥有编辑者角色时，IsEditorUser 权限检查应该返回 True。
        此测试需要数据库访问以创建 Role 记录。
        
        测试步骤：
            1. 创建或获取编辑者角色（Role.objects.get_or_create）
            2. 创建用户并分配编辑者角色
            3. 模拟 HTTP GET 请求并设置用户
            4. 调用 has_permission 方法验证权限
        
        预期结果：
            - has_permission 返回 True
        
        注意：
            - 此测试需要 db fixture 以访问数据库
            - 使用 get_or_create 避免重复创建角色
        """
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
        """
        测试普通用户没有编辑权限
        
        验证当用户没有编辑者角色时，IsEditorUser 权限检查应该返回 False。
        
        测试步骤：
            1. 创建 IsEditorUser 权限实例
            2. 创建普通用户对象（无特殊角色）
            3. 模拟 HTTP GET 请求并设置用户
            4. 调用 has_permission 方法验证权限
        
        预期结果：
            - has_permission 返回 False
        """
        permission = IsEditorUser()
        
        user = User(username='user', is_staff=False)
        
        factory = APIRequestFactory()
        request = factory.get('/api/test')
        request.user = user
        
        view = APIView()
        
        assert permission.has_permission(request, view) is False


@pytest.mark.unit
class TestIsOwnerOrAdminPermission:
    """
    IsOwnerOrAdmin 权限类测试
    
    验证对象级权限检查逻辑，确保只有对象所有者或管理员可以操作对象。
    
    测试用例：
        - 管理员可以访问任何对象（无论所有者是谁）
        - 对象所有者可以访问自己的对象
        - 其他用户不能访问他人的对象
        - 支持多种所有者属性名（author, user, uploader）
    
    权限规则：
        - 管理员（is_staff 或 is_superuser）可以访问所有对象
        - 对象的所有者（通过 author/user/uploader 属性判断）可以访问
        - 其他用户无权访问
    
    适用场景：
        - 文章内容编辑/删除（author 属性）
        - 个人资料修改（user 属性）
        - 媒体文件管理（uploader 属性）
    """
    
    def test_admin_can_access_any_object(self):
        """
        测试管理员可以访问任何对象
        
        验证即使用户不是对象的所有者，只要是管理员就可以访问该对象。
        这是管理员特权的核心体现。
        
        测试步骤：
            1. 创建 IsOwnerOrAdmin 权限实例
            2. 创建管理员用户对象
            3. 创建模拟对象（MockObject），设置其他用户为作者
            4. 模拟 HTTP GET 请求并设置管理员用户
            5. 调用 has_object_permission 方法验证权限
        
        预期结果：
            - has_object_permission 返回 True（管理员可以访问他人对象）
        
        安全考虑：
            - 管理员需要能够管理所有内容，包括审核、删除违规内容等
        """
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
        """
        测试对象所有者可以访问自己的对象
        
        验证当用户是对象的所有者时，可以访问该对象。
        这是对象级权限的基本功能。
        
        测试步骤：
            1. 创建 IsOwnerOrAdmin 权限实例
            2. 创建作者用户对象
            3. 创建模拟对象，设置该作者为所有者
            4. 模拟 HTTP GET 请求并设置作者用户
            5. 调用 has_object_permission 方法验证权限
        
        预期结果：
            - has_object_permission 返回 True（所有者可以访问自己的对象）
        
        应用场景：
            - 用户编辑自己发布的文章
            - 用户修改自己的个人资料
            - 用户删除自己上传的文件
        """
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
        """
        测试其他用户不能访问他人的对象
        
        验证当用户既不是管理员也不是对象所有者时，无法访问该对象。
        这是数据隔离和隐私保护的关键。
        
        测试步骤：
            1. 创建 IsOwnerOrAdmin 权限实例
            2. 创建作者用户和其他用户
            3. 创建模拟对象，设置作者为所有者
            4. 模拟 HTTP GET 请求并设置其他用户
            5. 调用 has_object_permission 方法验证权限
        
        预期结果：
            - has_object_permission 返回 False（其他用户无权访问）
        
        安全意义：
            - 防止用户查看、修改或删除他人的数据
            - 保护用户隐私和数据安全
        """
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
        """
        测试检查具有 user 属性的对象
        
        验证 IsOwnerOrAdmin 权限类能够识别 user 属性作为所有者标识。
        适用于 UserProfile、UserSettings 等以 user 为外键的模型。
        
        测试步骤：
            1. 创建 IsOwnerOrAdmin 权限实例
            2. 创建用户对象
            3. 创建模拟对象，设置 user 属性为该用户
            4. 模拟 HTTP GET 请求并设置相同用户
            5. 调用 has_object_permission 方法验证权限
        
        预期结果：
            - has_object_permission 返回 True（user 属性匹配）
        
        适用模型：
            - UserProfile（用户资料）
            - UserSettings（用户设置）
            - UserPreference（用户偏好）
        """
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
        """
        测试检查具有 uploader 属性的对象
        
        验证 IsOwnerOrAdmin 权限类能够识别 uploader 属性作为所有者标识。
        适用于 Media、File 等以上传者为所有者的模型。
        
        测试步骤：
            1. 创建 IsOwnerOrAdmin 权限实例
            2. 创建上传者用户对象
            3. 创建模拟对象，设置 uploader 属性为该用户
            4. 模拟 HTTP GET 请求并设置相同用户
            5. 调用 has_object_permission 方法验证权限
        
        预期结果：
            - has_object_permission 返回 True（uploader 属性匹配）
        
        适用模型：
            - Media（媒体文件）
            - Document（文档）
            - Attachment（附件）
        """
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
