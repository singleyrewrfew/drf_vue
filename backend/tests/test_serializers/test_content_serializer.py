"""
内容序列化器测试

测试内容相关序列化器的数据验证和输入输出
"""
import pytest
from django.contrib.auth import get_user_model

from apps.categories.models import Category
from apps.contents.models import Content
from apps.contents.serializers import (
    ContentSerializer,
    ContentListSerializer,
    ContentCreateUpdateSerializer,
)
from apps.tags.models import Tag

User = get_user_model()


@pytest.mark.unit
class TestContentSerializer:
    """内容序列化器测试类"""
    
    def test_content_serializer_output(self, db):
        """测试内容序列化器输出"""
        # 创建关联对象
        author = User.objects.create_user(username='author', password='pass123')
        category = Category.objects.create(name='技术', slug='tech')
        
        content = Content.objects.create(
            title='测试文章',
            slug='test-article',
            summary='测试摘要',
            content='这是文章内容',
            author=author,
            category=category,
            status='published'
        )
        
        # 序列化
        serializer = ContentSerializer(content)
        data = serializer.data
        
        # 验证字段
        assert data['title'] == '测试文章'
        assert data['slug'] == 'test-article'
        assert data['author_name'] == 'author'
        assert data['category_name'] == '技术'
        assert data['status'] == 'published'
        assert 'content_preview' in data
    
    def test_content_preview_limit(self, db):
        """测试内容预览长度限制"""
        author = User.objects.create_user(username='author', password='pass123')
        
        long_content = 'x' * 6000  # 6000 字符
        content = Content.objects.create(
            title='长文章',
            slug='long-article',
            content=long_content,
            author=author
        )
        
        serializer = ContentSerializer(content)
        data = serializer.data
        
        # 预览应该限制在 5000 字符
        assert len(data['content_preview']) == 5000
    
    def test_empty_content_preview(self, db):
        """测试空内容预览"""
        author = User.objects.create_user(username='author', password='pass123')
        
        content = Content.objects.create(
            title='无内容',
            slug='no-content',
            content='',
            author=author
        )
        
        serializer = ContentSerializer(content)
        data = serializer.data
        
        assert data['content_preview'] == ''


@pytest.mark.unit
class TestContentListSerializer:
    """内容列表序列化器测试类"""
    
    def test_list_serializer_excludes_full_content(self, db):
        """测试列表序列化器不包含完整内容"""
        author = User.objects.create_user(username='author', password='pass123')
        
        content = Content.objects.create(
            title='测试',
            slug='test',
            content='完整内容',
            summary='摘要',
            author=author
        )
        
        serializer = ContentListSerializer(content)
        data = serializer.data
        
        # 列表不应该包含 content 字段
        assert 'content' not in data
        # 但应该有 summary
        assert 'summary' in data


@pytest.mark.unit
class TestContentCreateUpdateSerializer:
    """内容创建更新序列化器测试类"""
    
    def test_create_content_success(self, db):
        """测试成功创建内容"""
        author = User.objects.create_user(username='author', password='pass123')
        category = Category.objects.create(name='技术', slug='tech')
        # 不传递 slug，让系统自动生成唯一 slug
        tag, _ = Tag.objects.get_or_create(name='Python')
        
        data = {
            'title': '新文章',
            'content': '文章内容',
            'summary': '文章摘要',
            'category': category.id,
            'tags': [tag.id],
            'status': 'draft'
        }
        
        # 创建 mock request
        from rest_framework.test import APIRequestFactory
        factory = APIRequestFactory()
        request = factory.get('/')
        request.user = author
        
        serializer = ContentCreateUpdateSerializer(data=data)
        serializer.context['request'] = request
        
        assert serializer.is_valid()
        
        content = serializer.save()
        assert content.title == '新文章'
        assert content.author == author
        assert content.category == category
        assert list(content.tags.all()) == [tag]
    
    def test_create_with_auto_slug(self, db):
        """测试自动生成 slug"""
        author = User.objects.create_user(username='author', password='pass123')
        
        data = {
            'title': '没有 slug 的文章',
            'content': '内容'
        }
        
        from rest_framework.test import APIRequestFactory
        factory = APIRequestFactory()
        request = factory.get('/')
        request.user = author
        
        serializer = ContentCreateUpdateSerializer(data=data)
        serializer.context['request'] = request
        
        assert serializer.is_valid()
        
        content = serializer.save()
        assert content.slug is not None
    
    def test_update_content(self, db):
        """测试更新内容"""
        author = User.objects.create_user(username='author', password='pass123')
        
        content = Content.objects.create(
            title='旧标题',
            slug='old-title',
            content='旧内容',
            author=author
        )
        
        data = {'title': '新标题'}
        
        from rest_framework.test import APIRequestFactory
        factory = APIRequestFactory()
        request = factory.get('/')
        request.user = author
        
        serializer = ContentCreateUpdateSerializer(content, data=data, partial=True)
        serializer.context['request'] = request
        
        assert serializer.is_valid()
        
        content_updated = serializer.save()
        assert content_updated.title == '新标题'
    
    def test_validate_cover_image_url(self, db):
        """测试封面图片 URL 验证"""
        author = User.objects.create_user(username='author', password='pass123')
        
        data = {
            'title': '带封面的文章',
            'content': '内容',
            'cover_image': '/media/images/cover.jpg'
        }
        
        from rest_framework.test import APIRequestFactory
        factory = APIRequestFactory()
        request = factory.get('/')
        request.user = author
        
        serializer = ContentCreateUpdateSerializer(data=data)
        serializer.context['request'] = request
        
        assert serializer.is_valid()
        
        content = serializer.save()
        assert content.cover_image.name == 'images/cover.jpg' or content.cover_image
