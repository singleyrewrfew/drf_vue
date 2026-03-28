"""
Test Utilities

测试工具类和Mock对象
"""
from unittest.mock import Mock
from django.contrib.auth import get_user_model

User = get_user_model()


class MockUser:
    """
    Mock用户类
    
    用于测试的用户模拟对象
    """
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', 1)
        self.username = kwargs.get('username', 'testuser')
        self.email = kwargs.get('email', 'test@example.com')
        self.is_superuser = kwargs.get('is_superuser', False)
        self.is_staff = kwargs.get('is_staff', False)
        self.is_active = kwargs.get('is_active', True)
        self._permissions = kwargs.get('permissions', [])
        self._role_code = kwargs.get('role_code', 'user')
    
    def __eq__(self, other):
        """支持对象比较（基于 ID）"""
        if not isinstance(other, MockUser):
            return False
        return self.id == other.id
    
    def has_permission(self, permission_code):
        """检查权限"""
        if self.is_superuser:
            return True
        return permission_code in self._permissions
    
    @property
    def is_admin(self):
        """是否为管理员"""
        return self.is_superuser or self._role_code == 'admin' or self.is_staff
    
    @property
    def is_editor(self):
        """是否为编辑"""
        return self.is_superuser or self._role_code in ['admin', 'editor']


class MockContent:
    """
    Mock内容类
    
    用于测试的内容模拟对象
    """
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', 1)
        self.title = kwargs.get('title', 'Test Content')
        self.content = kwargs.get('content', 'Test content body')
        self.status = kwargs.get('status', 'draft')
        self.view_count = kwargs.get('view_count', 0)
        self.author = kwargs.get('author', MockUser())
        self.created_at = kwargs.get('created_at')
        self.updated_at = kwargs.get('updated_at')
        self.published_at = kwargs.get('published_at')
    
    def save(self, *args, **kwargs):
        """保存方法"""
        pass
    
    def increment_view_count(self):
        """增加浏览量"""
        self.view_count += 1


class MockCategory:
    """
    Mock分类类
    """
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', 1)
        self.name = kwargs.get('name', 'Test Category')
        self.slug = kwargs.get('slug', 'test-category')
        self.description = kwargs.get('description', 'Test description')
        self.sort_order = kwargs.get('sort_order', 0)
    
    def save(self):
        """保存方法"""
        pass


class MockTag:
    """
    Mock标签类
    """
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', 1)
        self.name = kwargs.get('name', 'Test Tag')
        self.slug = kwargs.get('slug', 'test-tag')
    
    def save(self):
        """保存方法"""
        pass


def create_test_user(**kwargs):
    """
    创建测试用户
    
    Args:
        **kwargs: 用户属性
    
    Returns:
        User: 用户实例
    """
    defaults = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123',
        'is_active': True
    }
    defaults.update(kwargs)
    
    user = User.objects.create_user(**defaults)
    return user


def create_test_content(author, **kwargs):
    """
    创建测试内容
    
    Args:
        author: 作者
        **kwargs: 内容属性
    
    Returns:
        Content: 内容实例
    """
    from apps.contents.models import Content
    from utils.slug_utils import generate_unique_slug
    
    defaults = {
        'title': 'Test Content',
        'content': 'Test content body',
        'summary': 'Test summary',
        'status': 'draft',
        'author': author
    }
    defaults.update(kwargs)
    
    # 自动生成唯一 slug
    if 'slug' not in defaults:
        defaults['slug'] = generate_unique_slug(Content, defaults.get('title', 'test-content'))
    
    content = Content.objects.create(**defaults)
    return content


def create_test_category(**kwargs):
    """
    创建测试分类
    
    Args:
        **kwargs: 分类属性
    
    Returns:
        Category: 分类实例
    """
    from apps.categories.models import Category
    
    defaults = {
        'name': 'Test Category',
        'description': 'Test description',
        'sort_order': 0
    }
    defaults.update(kwargs)
    
    category = Category.objects.create(**defaults)
    return category


def create_test_tag(**kwargs):
    """
    创建测试标签
    
    Args:
        **kwargs: 标签属性
    
    Returns:
        Tag: 标签实例
    """
    from apps.tags.models import Tag
    
    defaults = {
        'name': 'Test Tag'
    }
    defaults.update(kwargs)
    
    tag = Tag.objects.create(**defaults)
    return tag


def assert_response_status(response, expected_status):
    """
    断言响应状态码
    
    Args:
        response: 响应对象
        expected_status: 预期状态码
    
    Raises:
        AssertionError: 状态码不匹配
    """
    assert response.status_code == expected_status, \
        f'Expected status {expected_status}, got {response.status_code}. Response: {response.data}'


def assert_response_data(response, key, expected_value):
    """
    断言响应数据
    
    Args:
        response: 响应对象
        key: 数据键
        expected_value: 预期值
    
    Raises:
        AssertionError: 值不匹配
    """
    assert key in response.data, f'Key "{key}" not found in response data'
    assert response.data[key] == expected_value, \
        f'Expected {key}={expected_value}, got {response.data[key]}'
