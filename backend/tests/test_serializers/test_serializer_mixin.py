"""
序列化器字段重复优化测试

验证使用Mixin模式重构后，序列化器字段是否正确继承和工作。
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.contents.models import Content
from apps.contents.serializers import (
    ContentSerializer,
    ContentListSerializer,
    ContentAuthorFieldsMixin,
    ContentCategoryFieldsMixin,
)
from apps.categories.models import Category

User = get_user_model()


@pytest.mark.django_db
class TestSerializerFieldInheritance:
    """测试序列化器字段继承"""

    def test_author_fields_mixin_exists(self):
        """测试作者字段Mixin存在且包含正确的字段"""
        mixin = ContentAuthorFieldsMixin()
        assert hasattr(mixin, 'fields')
        assert 'author_name' in mixin.fields
        assert 'author_avatar' in mixin.fields
        
        # 验证字段类型
        from rest_framework import serializers
        assert isinstance(mixin.fields['author_name'], serializers.CharField)
        assert isinstance(mixin.fields['author_avatar'], serializers.ImageField)

    def test_category_fields_mixin_exists(self):
        """测试分类字段Mixin存在且包含正确的字段"""
        mixin = ContentCategoryFieldsMixin()
        assert hasattr(mixin, 'fields')
        assert 'category_name' in mixin.fields
        
        # 验证字段类型
        from rest_framework import serializers
        assert isinstance(mixin.fields['category_name'], serializers.CharField)

    def test_content_serializer_inherits_author_fields(self):
        """测试ContentSerializer继承了作者字段"""
        serializer = ContentSerializer()
        
        # 应该从Mixin继承这些字段
        assert 'author_name' in serializer.fields
        assert 'author_avatar' in serializer.fields
        
        # 也应该有自己的字段
        assert 'category_slug' in serializer.fields
        assert 'content_preview' in serializer.fields
        assert 'tags' in serializer.fields

    def test_content_serializer_inherits_category_fields(self):
        """测试ContentSerializer继承了分类字段"""
        serializer = ContentSerializer()
        
        # 应该从Mixin继承这个字段
        assert 'category_name' in serializer.fields
        
        # 也应该有自己定义的category_slug
        assert 'category_slug' in serializer.fields

    def test_content_list_serializer_inherits_author_fields(self):
        """测试ContentListSerializer继承了作者字段"""
        serializer = ContentListSerializer()
        
        # 应该从Mixin继承这些字段
        assert 'author_name' in serializer.fields
        assert 'author_avatar' in serializer.fields
        
        # 也应该有自己的字段
        assert 'tags' in serializer.fields

    def test_content_list_serializer_inherits_category_fields(self):
        """测试ContentListSerializer继承了分类字段"""
        serializer = ContentListSerializer()
        
        # 应该从Mixin继承这个字段
        assert 'category_name' in serializer.fields

    def test_no_duplicate_field_definitions(self):
        """验证没有重复的字段定义"""
        # ContentSerializer的字段应该只出现一次
        serializer = ContentSerializer()
        field_names = list(serializer.fields.keys())
        
        # 检查关键字段只出现一次
        assert field_names.count('author_name') == 1
        assert field_names.count('author_avatar') == 1
        assert field_names.count('category_name') == 1

    def test_serialization_with_mixin_fields(self):
        """测试使用Mixin字段的序列化功能"""
        # 创建测试数据
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        category = Category.objects.create(name='Test Category', slug='test-category')
        content = Content.objects.create(
            title='Test Content',
            slug='test-content',
            summary='Test summary',
            content='Test content body',
            author=user,
            category=category,
            status='published'
        )
        
        # 测试ContentSerializer
        serializer = ContentSerializer(content)
        data = serializer.data
        
        # 验证Mixin提供的字段被正确序列化
        assert 'author_name' in data
        assert data['author_name'] == 'testuser'
        assert 'author_avatar' in data
        assert 'category_name' in data
        assert data['category_name'] == 'Test Category'
        
        # 测试ContentListSerializer
        list_serializer = ContentListSerializer(content)
        list_data = list_serializer.data
        
        # 验证Mixin提供的字段在列表序列化器中也正常工作
        assert 'author_name' in list_data
        assert list_data['author_name'] == 'testuser'
        assert 'category_name' in list_data
        assert list_data['category_name'] == 'Test Category'
        
        # 验证列表序列化器不包含完整内容
        assert 'content' not in list_data
        assert 'content_preview' not in list_data

    def test_mixin_field_source_mapping(self):
        """测试Mixin字段的source映射是否正确"""
        serializer = ContentSerializer()
        
        # 验证author_name的source配置
        author_name_field = serializer.fields['author_name']
        assert author_name_field.source_attrs == ['author', 'username']
        
        # 验证author_avatar的source配置
        author_avatar_field = serializer.fields['author_avatar']
        assert author_avatar_field.source_attrs == ['author', 'avatar']
        
        # 验证category_name的source配置
        category_name_field = serializer.fields['category_name']
        assert category_name_field.source_attrs == ['category', 'name']

    def test_both_serializers_share_same_mixin_fields(self):
        """验证两个序列化器共享相同的Mixin字段定义"""
        detail_serializer = ContentSerializer()
        list_serializer = ContentListSerializer()
        
        # 两个序列化器都应该有来自Mixin的相同字段
        common_fields = {'author_name', 'author_avatar', 'category_name'}
        
        for field_name in common_fields:
            assert field_name in detail_serializer.fields
            assert field_name in list_serializer.fields
            
            # 验证字段类型相同
            detail_field = detail_serializer.fields[field_name]
            list_field = list_serializer.fields[field_name]
            assert type(detail_field) == type(list_field)
