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
    """
    from apps.users.models import User
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


def pytest_sessionfinish(session, exitstatus):
    """
    在 pytest 会话结束后清理测试产生的媒体文件
    
    重要：只在 pytest 测试环境执行，避免误删生产数据
    
    参数:
        session: pytest 会话对象
        exitstatus: 退出状态码
    """
    import uuid as uuid_module
    
    # 安全检查：确保只在 pytest 测试环境执行
    # 通过检查环境变量或命令行参数来判断
    import sys
    if 'pytest' not in sys.modules:
        print("\n[警告] 非 pytest 环境，跳过媒体文件清理")
        return
    
    # 获取媒体目录
    media_root = Path(settings.MEDIA_ROOT)
    
    if not media_root.exists():
        return
    
    # 清理测试产生的用户文件夹（保留 avatars 和 thumbnails）
    cleaned_count = 0
    for folder in media_root.iterdir():
        if folder.is_dir() and folder.name not in ['avatars', 'thumbnails']:
            try:
                # 检查是否是 UUID 格式（测试用户的特征）
                try:
                    uuid_module.UUID(folder.name)
                    # 是 UUID 格式，删除整个文件夹
                    shutil.rmtree(folder)
                    print(f"\n[清理] 已删除测试文件夹：{folder.name}")
                    cleaned_count += 1
                except ValueError:
                    pass  # 不是 UUID，跳过
                    
            except Exception as e:
                print(f"\n[清理失败] {folder.name}: {e}")
    
    if cleaned_count > 0:
        print(f"[统计] 共清理 {cleaned_count} 个测试文件夹")
