"""
缓存失效机制测试（简化版）

验证 CacheInvalidationMixin 的核心功能。
"""
import pytest
import uuid
from django.contrib.auth import get_user_model

from apps.contents.models import Content
from apps.categories.models import Category
from utils.cache_utils import cache_set, cache_get, get_cache_key

User = get_user_model()


@pytest.mark.django_db
class TestCacheInvalidationCore:
    """测试缓存失效核心功能"""

    @pytest.fixture
    def admin_client(self):
        """创建管理员客户端"""
        from rest_framework.test import APIClient
        user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if not user.is_superuser:
            user.is_superuser = True
            user.save()
        
        client = APIClient()
        client.force_authenticate(user=user)
        return client

    @pytest.fixture
    def unique_category(self):
        """创建唯一分类"""
        unique_slug = f'test-{uuid.uuid4().hex[:8]}'
        return Category.objects.create(name='Test', slug=unique_slug)

    def test_cache_cleared_on_content_create(self, admin_client, unique_category):
        """测试创建内容时清除缓存"""
        # 设置缓存（使用正确的缓存键前缀）
        cache_key = get_cache_key('contents:list')
        cache_set(cache_key, {'test': 'data'}, timeout=300)
        assert cache_get(cache_key) is not None
        
        # 创建内容（需要content字段）
        response = admin_client.post('/api/contents/', {
            'title': 'Test Content',
            'category': str(unique_category.id),
            'content': '<p>Test content body</p>',
            'status': 'draft'
        }, format='json')
        
        assert response.status_code == 201
        
        # 缓存应该被清除
        assert cache_get(cache_key) is None

    def test_additional_patterns_cleared(self, admin_client, unique_category):
        """测试额外缓存模式也被清除"""
        # 设置多个缓存（使用正确的缓存键前缀）
        contents_key = get_cache_key('contents:list')
        stats_key = get_cache_key('stats:daily')
        authors_key = get_cache_key('popular_authors:list')
        
        cache_set(contents_key, {'main': 'cache'}, timeout=300)
        cache_set(stats_key, {'stats': 'data'}, timeout=300)
        cache_set(authors_key, {'authors': 'list'}, timeout=300)
        
        # 创建内容（需要content字段）
        response = admin_client.post('/api/contents/', {
            'title': 'Test Content 2',
            'category': str(unique_category.id),
            'content': '<p>Test content body 2</p>',
            'status': 'draft'
        }, format='json')
        
        assert response.status_code == 201
        
        # 所有缓存都应该被清除
        assert cache_get(contents_key) is None
        assert cache_get(stats_key) is None
        assert cache_get(authors_key) is None

    def test_cache_cleared_on_content_update(self, admin_client, unique_category):
        """测试更新内容时清除缓存"""
        # 创建内容
        user = User.objects.create_user(username='author', password='pass123')
        content = Content.objects.create(
            title='Original',
            slug=f'original-{uuid.uuid4().hex[:8]}',
            author=user,
            category=unique_category,
            status='draft'
        )
        
        # 设置缓存（使用正确的缓存键前缀）
        cache_key = get_cache_key('contents:list')
        cache_set(cache_key, {'test': 'data'}, timeout=300)
        assert cache_get(cache_key) is not None
        
        # 更新内容
        response = admin_client.patch(f'/api/contents/{content.id}/', {
            'title': 'Updated Title'
        }, format='json')
        
        assert response.status_code == 200
        
        # 缓存应该被清除
        assert cache_get(cache_key) is None

    def test_cache_cleared_on_content_delete(self, admin_client, unique_category):
        """测试删除内容时清除缓存"""
        # 创建内容
        user = User.objects.create_user(username='author2', password='pass123')
        content = Content.objects.create(
            title='To Delete',
            slug=f'to-delete-{uuid.uuid4().hex[:8]}',
            author=user,
            category=unique_category,
            status='draft'
        )
        
        # 设置缓存（使用正确的缓存键前缀）
        cache_key = get_cache_key('contents:list')
        cache_set(cache_key, {'test': 'data'}, timeout=300)
        assert cache_get(cache_key) is not None
        
        # 删除内容
        response = admin_client.delete(f'/api/contents/{content.id}/')
        
        assert response.status_code == 204
        
        # 缓存应该被清除
        assert cache_get(cache_key) is None

    def test_mixin_configuration(self):
        """测试Mixin配置正确性"""
        from apps.contents.views import ContentViewSet
        
        viewset = ContentViewSet()
        
        # 验证配置
        assert viewset.cache_key_prefix == 'contents:list'
        assert 'stats' in viewset.additional_cache_patterns
        assert 'popular_authors' in viewset.additional_cache_patterns

    def test_category_viewset_config(self):
        """测试分类ViewSet配置"""
        from apps.categories.views import CategoryViewSet
        
        viewset = CategoryViewSet()
        
        assert viewset.cache_key_prefix == 'categories:list'
        assert viewset.additional_cache_patterns == []

    def test_tag_viewset_config(self):
        """测试标签ViewSet配置"""
        from apps.tags.views import TagViewSet
        
        viewset = TagViewSet()
        
        assert viewset.cache_key_prefix == 'tags:list'
        assert viewset.additional_cache_patterns == []
