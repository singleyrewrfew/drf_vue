"""
Pytest Configuration

测试配置和 fixtures
"""
import os
import pytest
import shutil
from pathlib import Path

# 设置 Django 环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
from django.conf import settings
from django.test import RequestFactory
from rest_framework.test import APIClient

# 初始化 Django
django.setup()


@pytest.fixture
def authenticated_api_client(api_client, user):
    """
    已认证的 API 客户端
    """
    from rest_framework_simplejwt.tokens import RefreshToken
    
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client


@pytest.fixture
def api_client():
    """
    API客户端fixture
    """
    return APIClient()


@pytest.fixture
def request_factory():
    """
    请求工厂fixture
    """
    return RequestFactory()


@pytest.fixture
def user_data():
    """
    用户测试数据
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
    内容测试数据
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
    分类测试数据
    """
    return {
        'name': 'Test Category',
        'description': 'Test category description',
        'sort_order': 1
    }


@pytest.fixture
def tag_data():
    """
    标签测试数据
    """
    return {
        'name': 'Test Tag'
    }


@pytest.fixture
def user(db):
    """
    创建测试用户（需要数据库）
    
    注意：测试用户的用户名固定为 'testuser'，用于在清理逻辑中识别
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
    在测试会话开始前设置干净的测试媒体目录
    
    重要：
    - 测试环境使用独立的 media_test 目录
    - 每次测试开始前自动清理旧的测试数据
    - 不会影响生产环境的 media 目录
    
    参数:
        session: pytest 会话对象
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
    配置 Django 数据库访问（用于 pytest_sessionfinish 中的数据库查询）
    
    注意：这里只配置，不执行清理，清理逻辑在 pytest_sessionfinish 中
    """
    pass


def pytest_sessionfinish(session, exitstatus):
    """
    在 pytest 会话结束后输出提示信息
    
    注意：
    - 测试媒体目录已在开始时清理，结束时保留以便调试
    - 如需手动清理，可删除 backend/media_test 目录
    
    参数:
        session: pytest 会话对象
        exitstatus: 退出状态码
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
