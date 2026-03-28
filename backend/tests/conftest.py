"""
Pytest Configuration

测试配置和 fixtures
"""
import os
import pytest

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
