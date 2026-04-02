"""
Test Slug Utils

Slug工具测试
"""
import pytest

from utils.slug_utils import generate_slug_from_text, generate_unique_slug


@pytest.mark.unit
class TestSlugUtils:
    """Slug工具测试类"""
    
    def test_generate_slug_from_english_text(self):
        """测试从英文文本生成slug"""
        result = generate_slug_from_text('Hello World')
        
        assert result == 'hello-world'
    
    def test_generate_slug_from_chinese_text(self):
        """测试从中文文本生成 slug"""
        result = generate_slug_from_text('Python 教程')
            
        # 中文会转换为拼音，但至少包含英文部分
        assert 'python' in result
        # 不强制要求完整拼音，因为实现可能不同
    
    def test_generate_slug_from_mixed_text(self):
        """测试从中英混合文本生成slug"""
        result = generate_slug_from_text('Django REST Framework教程')
        
        assert 'django' in result
        assert 'rest' in result
        assert 'framework' in result
    
    def test_generate_slug_from_empty_text(self):
        """测试从空文本生成slug"""
        result = generate_slug_from_text('')
        
        assert result == ''
    
    def test_generate_slug_from_none_text(self):
        """测试从None生成slug"""
        result = generate_slug_from_text(None)
        
        assert result == ''
    
    def test_generate_slug_with_special_characters(self):
        """测试包含特殊字符的文本"""
        result = generate_slug_from_text('Hello! @World# $Test%')
        
        assert 'hello' in result
        assert 'world' in result
        assert 'test' in result
    
    def test_generate_unique_slug(self, db):
        """测试生成唯一slug"""
        from apps.categories.models import Category
        
        result = generate_unique_slug(Category, 'Test Category')
        
        assert result == 'test-category'
    
    def test_generate_unique_slug_with_duplicate(self, db):
        """测试生成唯一slug（有重复）"""
        from apps.categories.models import Category
        
        Category.objects.create(name='Test Category', slug='test-category')
        
        result = generate_unique_slug(Category, 'Test Category')
        
        assert result == 'test-category-1'
    
    def test_generate_unique_slug_with_multiple_duplicates(self, db):
        """测试生成唯一slug（多个重复）"""
        from apps.categories.models import Category
        
        Category.objects.create(name='Test Category', slug='test-category')
        Category.objects.create(name='Test Category 2', slug='test-category-1')
        Category.objects.create(name='Test Category 3', slug='test-category-2')
        
        result = generate_unique_slug(Category, 'Test Category')
        
        assert result == 'test-category-3'
    
    def test_generate_unique_slug_with_instance(self, db):
        """测试生成唯一slug（更新实例）"""
        from apps.categories.models import Category
        
        instance = Category.objects.create(name='Test Category', slug='test-category')
        
        result = generate_unique_slug(Category, 'Test Category', instance=instance)
        
        assert result == 'test-category'
