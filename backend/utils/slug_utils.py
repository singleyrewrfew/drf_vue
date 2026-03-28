"""
Slug 工具函数

提供统一的 slug 生成功能，支持中文转拼音
"""
import uuid
from django.utils.text import slugify


def generate_slug_from_text(text):
    """
    从文本生成 slug，支持中文
    
    Args:
        text: 原始文本（可以是中文或英文）
    
    Returns:
        str: 生成的 slug 字符串，如果无法生成则返回空字符串
    
    Example:
        >>> generate_slug_from_text('Python教程')
        'python-jiao-cheng'
        >>> generate_slug_from_text('Django REST Framework')
        'django-rest-framework'
    """
    if not text:
        return ''
    
    try:
        from pypinyin import lazy_pinyin
        pinyin_list = lazy_pinyin(text)
        base_slug = '-'.join(pinyin_list).lower()
    except ImportError:
        base_slug = text
    
    base_slug = slugify(base_slug) or slugify(text)
    
    return base_slug if base_slug else ''


def generate_unique_slug(model_class, base_text, instance=None, slug_field='slug'):
    """
    为 Django 模型实例生成唯一的 slug
    
    Args:
        model_class: Django 模型类
        base_text: 要转换为 slug 的原始文本
        instance: 当前实例对象（用于更新操作），在唯一性检查时会排除此实例
        slug_field: slug 字段的名称，默认为 'slug'
    
    Returns:
        str: 在数据库中唯一的 slug 字符串
    
    Example:
        >>> slug = generate_unique_slug(Category, 'Python教程')
        >>> print(slug)
        'python-jiao-cheng'
    """
    base_slug = generate_slug_from_text(base_text)
    
    if not base_slug:
        base_slug = uuid.uuid4().hex[:8]
    
    slug = base_slug
    counter = 1
    
    queryset = model_class.objects.all()
    if instance and instance.pk:
        queryset = queryset.exclude(pk=instance.pk)
    
    while queryset.filter(**{slug_field: slug}).exists():
        slug = f'{base_slug}-{counter}'
        counter += 1
    
    return slug
