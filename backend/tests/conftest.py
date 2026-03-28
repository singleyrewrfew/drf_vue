"""
Pytest Configuration

测试配置和fixtures
"""
import pytest
from django.conf import settings
from django.test import RequestFactory
from rest_framework.test import APIClient


@pytest.fixture(scope='session')
def django_db_setup():
    """
    数据库设置
    """
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }


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
