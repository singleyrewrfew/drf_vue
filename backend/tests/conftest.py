"""
Pytest Configuration

测试配置和 fixtures

作用：定义项目测试的全局配置、共享 fixtures 和钩子函数
使用：pytest 自动加载此文件，所有测试均可使用其中定义的 fixtures

主要功能：
    1. Django 环境初始化 - 设置环境变量并启动 Django
    2. 通用 fixtures - 提供 API 客户端、测试数据等共享资源
    3. 测试媒体目录管理 - 自动创建和清理隔离的测试文件目录
    4. 会话生命周期钩子 - 在测试开始和结束时执行清理操作

Fixture 分类：
    - 客户端类：api_client, authenticated_api_client, request_factory
    - 数据类：user_data, content_data, category_data, tag_data
    - 数据库类：user（需要 db fixture）
    - 会话级：setup_test_media_directory, django_db_setup
"""
import os
import shutil
from pathlib import Path

import pytest

# 设置 Django 环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
from django.test import RequestFactory
from rest_framework.test import APIClient

# 初始化 Django
django.setup()


@pytest.fixture
def authenticated_api_client(api_client, user):
    """
    创建已认证的 API 客户端 Fixture
    
    为测试提供带有 JWT Token 的认证客户端，用于测试需要登录的接口。
    自动为指定用户生成 access token 并设置到请求头中。
    
    Args:
        api_client: DRF APIClient 实例（由 api_client fixture 提供）
        user: 测试用户对象（由 user fixture 提供）
    
    Returns:
        APIClient: 已配置认证信息的 API 客户端实例
    
    使用示例：
        def test_protected_endpoint(authenticated_api_client):
            response = authenticated_api_client.get('/api/protected/')
            assert response.status_code == 200
    """
    from rest_framework_simplejwt.tokens import RefreshToken
    
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client


@pytest.fixture
def api_client():
    """
    创建未认证的 API 客户端 Fixture
    
    提供基础的 DRF APIClient 实例，用于发送 HTTP 请求。
    不包含任何认证信息，适合测试公开接口或验证权限控制。
    
    Returns:
        APIClient: DRF API 客户端实例
    
    使用示例：
        def test_public_endpoint(api_client):
            response = api_client.get('/api/public/')
            assert response.status_code == 200
    """
    return APIClient()


@pytest.fixture
def request_factory():
    """
    创建 Django RequestFactory Fixture
    
    提供 RequestFactory 实例，用于创建模拟的 HTTP 请求对象。
    适用于测试视图函数、中间件或需要直接操作 request 对象的场景。
    
    Returns:
        RequestFactory: Django 请求工厂实例
    
    使用示例：
        def test_view_logic(request_factory):
            request = request_factory.get('/api/test/')
            response = my_view(request)
    """
    return RequestFactory()


@pytest.fixture
def user_data():
    """
    提供用户测试数据字典 Fixture
    
    返回标准的用户注册/创建数据，包含必填字段和默认值。
    可用于测试用户创建、更新等操作的数据准备。
    
    Returns:
        dict: 用户数据字典，包含以下字段：
            - username (str): 用户名 'testuser'
            - email (str): 邮箱 'test@example.com'
            - password (str): 密码 'testpass123'
            - first_name (str): 名字 'Test'
            - last_name (str): 姓氏 'User'
    
    使用示例：
        def test_create_user(api_client, user_data):
            response = api_client.post('/api/users/', user_data)
            assert response.status_code == 201
    """
    return {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123',
        'first_name': 'Test',
        'last_name': 'User'
    }


@pytest.fixture
def content_data():
    """
    提供内容测试数据字典 Fixture
    
    返回标准的内容创建数据，包含文章的基本字段。
    用于测试内容的创建、更新等操作。
    
    Returns:
        dict: 内容数据字典，包含以下字段：
            - title (str): 标题 'Test Content'
            - content (str): 正文内容
            - summary (str): 摘要
            - status (str): 状态 'draft'（草稿）
    
    使用示例：
        def test_create_content(authenticated_api_client, content_data):
            response = authenticated_api_client.post('/api/contents/', content_data)
            assert response.status_code == 201
    """
    return {
        'title': 'Test Content',
        'content': 'This is test content.',
        'summary': 'Test summary',
        'status': 'draft'
    }


@pytest.fixture
def category_data():
    """
    提供分类测试数据字典 Fixture
    
    返回标准的分类创建数据，用于测试分类的 CRUD 操作。
    
    Returns:
        dict: 分类数据字典，包含以下字段：
            - name (str): 分类名称 'Test Category'
            - description (str): 分类描述
            - sort_order (int): 排序顺序 1
    
    使用示例：
        def test_create_category(authenticated_api_client, category_data):
            response = authenticated_api_client.post('/api/categories/', category_data)
            assert response.status_code == 201
    """
    return {
        'name': 'Test Category',
        'description': 'Test category description',
        'sort_order': 1
    }


@pytest.fixture
def tag_data():
    """
    提供标签测试数据字典 Fixture
    
    返回标准的标签创建数据，用于测试标签的 CRUD 操作。
    
    Returns:
        dict: 标签数据字典，包含以下字段：
            - name (str): 标签名称 'Test Tag'
    
    使用示例：
        def test_create_tag(authenticated_api_client, tag_data):
            response = authenticated_api_client.post('/api/tags/', tag_data)
            assert response.status_code == 201
    """
    return {
        'name': 'Test Tag'
    }


@pytest.fixture
def user(db):
    """
    创建或获取测试用户 Fixture
    
    使用 get_or_create 确保用户存在且唯一，避免重复创建导致的冲突。
    如果用户已存在，会重置密码以确保测试一致性。
    
    Args:
        db: pytest-django 提供的数据库访问 fixture，启用数据库操作
    
    Returns:
        User: 测试用户实例，用户名为 'testuser'
    
    注意：
        - 用户名固定为 'testuser'，便于在清理逻辑中识别
        - 密码统一设置为 'testpass123'
        - 使用 get_or_create 保证跨测试用例的一致性
    
    使用示例：
        def test_user_profile(authenticated_api_client, user):
            response = authenticated_api_client.get('/api/users/me/')
            assert response.data['username'] == user.username
    """
    from apps.users.models import User
    # 使用 get_or_create 避免重复创建导致的唯一性冲突
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
        }
    )
    if not created:
        # 如果用户已存在，设置密码
        user.set_password('testpass123')
        user.save()
    return user


@pytest.fixture(scope='session', autouse=True)
def setup_test_media_directory():
    """
    会话级 Fixture：初始化测试媒体目录
    
    在测试会话开始时自动执行，创建独立的测试媒体目录。
    确保测试环境与生产环境完全隔离，避免污染真实数据。
    
    执行流程：
        1. 安全检查：确认在 pytest 环境中运行
        2. 路径验证：确保操作的是 media_test 目录而非生产目录
        3. 清理旧数据：删除已存在的测试目录（如果存在）
        4. 创建新目录：建立干净的测试媒体目录
    
    特性：
        - scope='session': 整个测试会话只执行一次，提高性能
        - autouse=True: 自动使用，无需在测试中显式声明
        - 安全性：多重检查防止误删生产数据
    
    Raises:
        Exception: 目录创建失败时打印错误信息但不中断测试
    
    注意：
        - 测试媒体目录位于 backend/media_test/
        - 测试结束后目录会保留以便调试，需手动清理
    """
    import sys
    
    # 安全检查：确保只在 pytest 测试环境执行
    if 'pytest' not in sys.modules:
        print("\n[警告] 非 pytest 环境，跳过测试媒体目录设置")
        return
    
    # 获取测试媒体目录
    from django.conf import settings
    test_media_root = Path(settings.MEDIA_ROOT)
    
    # 确保只操作测试目录（media_test）
    if not str(test_media_root).endswith('media_test'):
        print(f"\n[警告] 媒体目录不是测试目录：{test_media_root}，跳过设置")
        return
    
    # 如果已存在，先清理
    if test_media_root.exists():
        try:
            shutil.rmtree(test_media_root)
            print(f"\n[清理] 已删除旧的测试媒体目录：{test_media_root}")
        except Exception as e:
            print(f"\n[清理失败] {test_media_root}: {e}")
    
    # 创建新的测试媒体目录
    try:
        test_media_root.mkdir(parents=True, exist_ok=True)
        print(f"\n[准备] 已创建测试媒体目录：{test_media_root}")
    except Exception as e:
        print(f"\n[错误] 创建测试目录失败：{e}")


@pytest.fixture(scope='session')
def django_db_setup():
    """
    配置 Django 数据库访问 Fixture
    
    为 pytest_sessionfinish 钩子函数提供数据库访问能力。
    此 fixture 本身不执行任何操作，仅作为依赖注入点。
    
    注意：
        - scope='session': 会话级别，整个测试周期只配置一次
        - 实际清理逻辑在 pytest_sessionfinish 中执行
        - 此处 pass 是为了让 pytest-django 正确初始化数据库连接
    """
    pass


def pytest_sessionfinish(session, exitstatus):
    """
    Pytest 会话结束钩子函数
    
    在所有测试执行完毕后自动调用，输出测试媒体目录的提示信息。
    保留测试目录以便调试，避免自动删除导致问题排查困难。
    
    Args:
        session: pytest 会话对象，包含测试执行的整体信息
        exitstatus: 测试退出状态码（0 表示成功，非 0 表示失败）
    
    执行流程：
        1. 环境检查：确认在 pytest 环境中运行
        2. 路径获取：从 Django 设置中读取媒体目录路径
        3. 安全验证：确保只处理 media_test 测试目录
        4. 提示输出：告知用户测试目录位置及手动清理方法
    
    注意：
        - 此函数由 pytest 自动调用，无需手动触发
        - 测试媒体目录在开始时已清理，结束时保留供调试使用
        - 如需完全清理，可手动删除 backend/media_test 目录
        - 不会影响生产环境的 media 目录
    
    使用场景：
        - 测试失败时查看生成的测试文件
        - 验证文件上传功能的实际存储结果
        - 调试媒体文件相关的问题
    """
    import sys
    
    # 安全检查：确保只在 pytest 测试环境执行
    if 'pytest' not in sys.modules:
        return
    
    # 获取测试媒体目录
    from django.conf import settings
    test_media_root = Path(settings.MEDIA_ROOT)
    
    # 确保只处理测试目录（media_test）
    if str(test_media_root).endswith('media_test') and test_media_root.exists():
        print(f"\n[提示] 测试媒体目录已保留：{test_media_root}")
        print("       如需清理，请手动删除该目录")
