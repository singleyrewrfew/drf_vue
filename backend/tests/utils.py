"""
Test Utilities

测试工具类和Mock对象

作用：提供测试所需的 Mock 对象和数据创建辅助函数
使用：在测试文件中导入相应的 Mock 类或 create_ 函数

主要功能：
    1. Mock 对象类 - 模拟 Django 模型对象，避免数据库依赖
    2. 数据创建函数 - 快速创建测试数据，支持自定义参数
    3. 断言辅助函数 - 简化 API 响应的验证逻辑

适用场景：
    - 单元测试：使用 Mock 类隔离外部依赖
    - 集成测试：使用 create_ 函数准备测试数据
    - API 测试：使用 assert_ 函数验证响应结果
"""
from django.contrib.auth import get_user_model

User = get_user_model()


class MockUser:
    """
    Mock 用户类
    
    模拟 Django User 模型对象，用于不依赖数据库的单元测试。
    支持自定义用户属性、权限检查和角色判断。
    
    特性：
        - 支持所有常用用户属性的自定义
        - 实现权限检查方法 has_permission()
        - 提供 is_admin 和 is_editor 属性判断
        - 支持基于 ID 的对象比较
    
    使用示例：
        # 创建普通用户
        user = MockUser(id=1, username='testuser')
        
        # 创建管理员用户
        admin = MockUser(id=2, role_code='admin')
        
        # 检查权限
        if user.has_permission('content_publish'):
            ...
        
        # 判断角色
        if user.is_admin:
            ...
    """
    
    def __init__(self, **kwargs):
        """
        初始化 Mock 用户对象
        
        Args:
            **kwargs: 用户属性字典，支持的字段包括：
                - id (int): 用户 ID，默认为 1
                - username (str): 用户名，默认为 'testuser'
                - email (str): 邮箱，默认为 'test@example.com'
                - is_superuser (bool): 是否为超级用户，默认 False
                - is_staff (bool): 是否为工作人员，默认 False
                - is_active (bool): 是否激活，默认 True
                - permissions (list): 权限列表，默认空列表
                - role_code (str): 角色代码，默认 'user'
        """
        self.id = kwargs.get('id', 1)
        self.username = kwargs.get('username', 'testuser')
        self.email = kwargs.get('email', 'test@example.com')
        self.is_superuser = kwargs.get('is_superuser', False)
        self.is_staff = kwargs.get('is_staff', False)
        self.is_active = kwargs.get('is_active', True)
        self._permissions = kwargs.get('permissions', [])
        self._role_code = kwargs.get('role_code', 'user')
    
    def __eq__(self, other):
        """
        判断两个 MockUser 对象是否相等
        
        基于用户 ID 进行比较，用于测试中的对象匹配和断言。
        
        Args:
            other: 待比较的对象
        
        Returns:
            bool: 如果是 MockUser 且 ID 相同则返回 True，否则 False
        """
        if not isinstance(other, MockUser):
            return False
        return self.id == other.id
    
    def has_permission(self, permission_code):
        """
        检查用户是否具有指定权限
        
        超级用户自动拥有所有权限，普通用户检查权限列表。
        
        Args:
            permission_code (str): 权限代码字符串
        
        Returns:
            bool: 如果用户具有该权限返回 True，否则 False
        
        使用示例：
            user = MockUser(permissions=['content_publish'])
            assert user.has_permission('content_publish') is True
            assert user.has_permission('content_delete') is False
        """
        if self.is_superuser:
            return True
        return permission_code in self._permissions
    
    @property
    def is_admin(self):
        """
        判断用户是否为管理员
        
        满足以下任一条件即为管理员：
            - 是超级用户 (is_superuser)
            - 角色代码为 'admin'
            - 是工作人员 (is_staff)
        
        Returns:
            bool: 如果是管理员返回 True，否则 False
        """
        return self.is_superuser or self._role_code == 'admin' or self.is_staff
    
    @property
    def is_editor(self):
        """
        判断用户是否为编辑
        
        满足以下任一条件即为编辑：
            - 是超级用户 (is_superuser)
            - 角色代码为 'admin' 或 'editor'
        
        Returns:
            bool: 如果是编辑返回 True，否则 False
        """
        return self.is_superuser or self._role_code in ['admin', 'editor']


class MockContent:
    """
    Mock 内容类
    
    模拟 Content 模型对象，用于测试内容相关的业务逻辑。
    支持自定义内容属性、状态管理和浏览量统计。
    
    特性：
        - 支持所有内容字段的自定义
        - 提供 save() 方法占位符（兼容模型接口）
        - 实现 increment_view_count() 方法
        - 默认关联一个 MockUser 作为作者
    
    使用示例：
        # 创建草稿内容
        content = MockContent(title='Test', status='draft')
        
        # 创建已发布内容
        author = MockUser(id=1)
        content = MockContent(author=author, status='published')
        
        # 增加浏览量
        content.increment_view_count()
        assert content.view_count == 1
    """
    
    def __init__(self, **kwargs):
        """
        初始化 Mock 内容对象
        
        Args:
            **kwargs: 内容属性字典，支持的字段包括：
                - id (int): 内容 ID，默认为 1
                - title (str): 标题，默认为 'Test Content'
                - content (str): 正文内容，默认为 'Test content body'
                - status (str): 状态，默认为 'draft'
                - view_count (int): 浏览量，默认为 0
                - author (MockUser): 作者对象，默认为新的 MockUser
                - created_at: 创建时间
                - updated_at: 更新时间
                - published_at: 发布时间
        """
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
        """
        保存方法占位符
        
        模拟 Django 模型的 save() 方法，实际不执行任何操作。
        用于兼容需要调用 save() 的业务逻辑代码。
        
        Args:
            *args: 位置参数（忽略）
            **kwargs: 关键字参数（忽略）
        """
        pass
    
    def increment_view_count(self):
        """
        增加内容浏览量
        
        将 view_count 属性加 1，模拟用户访问内容的行为。
        
        使用示例：
            content = MockContent(view_count=5)
            content.increment_view_count()
            assert content.view_count == 6
        """
        self.view_count += 1


class MockCategory:
    """
    Mock 分类类
    
    模拟 Category 模型对象，用于测试分类相关的功能。
    提供基础的分类属性和 save() 方法占位符。
    
    使用示例：
        category = MockCategory(name='技术', slug='tech')
        assert category.name == '技术'
    """
    
    def __init__(self, **kwargs):
        """
        初始化 Mock 分类对象
        
        Args:
            **kwargs: 分类属性字典，支持的字段包括：
                - id (int): 分类 ID，默认为 1
                - name (str): 分类名称，默认为 'Test Category'
                - slug (str): URL 别名，默认为 'test-category'
                - description (str): 描述，默认为 'Test description'
                - sort_order (int): 排序顺序，默认为 0
        """
        self.id = kwargs.get('id', 1)
        self.name = kwargs.get('name', 'Test Category')
        self.slug = kwargs.get('slug', 'test-category')
        self.description = kwargs.get('description', 'Test description')
        self.sort_order = kwargs.get('sort_order', 0)
    
    def save(self):
        """
        保存方法占位符
        
        模拟 Django 模型的 save() 方法，实际不执行任何操作。
        """
        pass


class MockTag:
    """
    Mock 标签类
    
    模拟 Tag 模型对象，用于测试标签相关的功能。
    提供基础的标签属性和 save() 方法占位符。
    
    使用示例：
        tag = MockTag(name='Python', slug='python')
        assert tag.name == 'Python'
    """
    
    def __init__(self, **kwargs):
        """
        初始化 Mock 标签对象
        
        Args:
            **kwargs: 标签属性字典，支持的字段包括：
                - id (int): 标签 ID，默认为 1
                - name (str): 标签名称，默认为 'Test Tag'
                - slug (str): URL 别名，默认为 'test-tag'
        """
        self.id = kwargs.get('id', 1)
        self.name = kwargs.get('name', 'Test Tag')
        self.slug = kwargs.get('slug', 'test-tag')
    
    def save(self):
        """
        保存方法占位符
        
        模拟 Django 模型的 save() 方法，实际不执行任何操作。
        """
        pass


def create_test_user(**kwargs):
    """
    在数据库中创建测试用户
    
    使用 Django ORM 创建真实用户记录，适用于集成测试和 API 测试。
    自动生成唯一用户名避免冲突，设置默认密码便于测试登录。
    
    Args:
        **kwargs: 用户属性字典，可选字段包括：
            - username (str): 用户名（如不提供则自动生成）
            - username_prefix (str): 用户名前缀，用于生成唯一用户名
            - email (str): 邮箱，默认根据用户名生成
            - password (str): 密码，默认 'testpass123'
            - is_active (bool): 是否激活，默认 True
            - 其他 User 模型支持的字段
    
    Returns:
        User: Django User 模型实例
    
    注意：
        - 此函数会操作数据库，需要在 pytest-django 环境中使用
        - 用户名会自动添加 UUID 后缀保证唯一性
        - 密码统一设置为 'testpass123' 便于测试
    
    使用示例：
        # 创建用户（自动生成用户名）
        user = create_test_user()
        
        # 指定用户名前缀
        user = create_test_user(username_prefix='admin')
        
        # 完全自定义
        user = create_test_user(
            username='custom_user',
            email='custom@example.com',
            is_staff=True
        )
    """
    import uuid
    
    # 如果没有指定用户名，生成唯一的用户名
    if 'username' not in kwargs:
        prefix = kwargs.pop('username_prefix', 'testuser')
        kwargs['username'] = f'{prefix}_{uuid.uuid4().hex[:8]}'
    
    defaults = {
        'email': kwargs.get('username', 'testuser') + '@example.com',
        'password': 'testpass123',
        'is_active': True
    }
    defaults.update(kwargs)
    
    user = User.objects.create_user(**defaults)
    return user


def create_test_content(author, **kwargs):
    """
    在数据库中创建测试内容
    
    使用 Django ORM 创建真实的内容记录，适用于集成测试和 API 测试。
    自动生成唯一 slug 避免冲突，设置默认值便于快速创建。
    
    Args:
        author: 内容作者（User 模型实例）
        **kwargs: 内容属性字典，可选字段包括：
            - title (str): 标题，默认 'Test Content'
            - content (str): 正文内容，默认 'Test content body'
            - summary (str): 摘要，默认 'Test summary'
            - status (str): 状态，默认 'draft'
            - slug (str): URL 别名（如不提供则自动生成）
            - 其他 Content 模型支持的字段
    
    Returns:
        Content: Content 模型实例
    
    注意：
        - 此函数会操作数据库，需要在 pytest-django 环境中使用
        - slug 会自动生成保证唯一性
        - 必须提供 author 参数
    
    使用示例：
        # 创建草稿内容
        user = create_test_user()
        content = create_test_content(user)
        
        # 创建已发布内容
        content = create_test_content(
            user,
            title='My Article',
            status='published'
        )
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
    在数据库中创建测试分类
    
    使用 Django ORM 创建真实的分类记录，适用于集成测试和 API 测试。
    设置默认值便于快速创建分类对象。
    
    Args:
        **kwargs: 分类属性字典，可选字段包括：
            - name (str): 分类名称，默认 'Test Category'
            - description (str): 描述，默认 'Test description'
            - sort_order (int): 排序顺序，默认 0
            - 其他 Category 模型支持的字段
    
    Returns:
        Category: Category 模型实例
    
    注意：
        - 此函数会操作数据库，需要在 pytest-django 环境中使用
    
    使用示例：
        # 创建默认分类
        category = create_test_category()
        
        # 自定义分类
        category = create_test_category(
            name='技术文章',
            slug='tech',
            description='技术相关的文章'
        )
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
    在数据库中创建测试标签
    
    使用 Django ORM 创建真实的标签记录，适用于集成测试和 API 测试。
    设置默认值便于快速创建标签对象。
    
    Args:
        **kwargs: 标签属性字典，可选字段包括：
            - name (str): 标签名称，默认 'Test Tag'
            - slug (str): URL 别名
            - 其他 Tag 模型支持的字段
    
    Returns:
        Tag: Tag 模型实例
    
    注意：
        - 此函数会操作数据库，需要在 pytest-django 环境中使用
    
    使用示例：
        # 创建默认标签
        tag = create_test_tag()
        
        # 自定义标签
        tag = create_test_tag(name='Python', slug='python')
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
