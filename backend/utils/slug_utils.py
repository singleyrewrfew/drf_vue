"""
Slug 工具函数

提供 URL 友好的 slug 生成和唯一性保证功能。
"""

from django.utils.text import slugify
from django.db import models


def generate_unique_slug(model_class, name, instance=None, field_name='slug'):
    """
    生成唯一的 slug
    
    Args:
        model_class: Django 模型类
        name: 用于生成 slug 的文本（如标题、名称）
        instance: 当前实例（更新时排除自身）
        field_name: slug 字段名，默认为 'slug'
    
    Returns:
        str: 唯一的 slug 字符串
    
    Example:
        >>> generate_unique_slug(Category, 'Python 编程')
        'python-bian-cheng'
        
        >>> generate_unique_slug(Category, 'Python 编程', existing_instance)
        'python-bian-cheng-1'  # 如果已存在则添加数字后缀
    """
    # 生成基础 slug
    base_slug = slugify(name)
    
    if not base_slug:
        # 如果 slugify 后为空，使用随机字符串
        import uuid
        base_slug = f'slug-{uuid.uuid4().hex[:8]}'
    
    slug = base_slug
    counter = 1
    
    # 构建查询条件
    queryset = model_class.objects.filter(**{field_name: slug})
    
    # 如果是更新操作，排除当前实例
    if instance and instance.pk:
        queryset = queryset.exclude(pk=instance.pk)
    
    # 如果 slug 已存在，添加数字后缀
    while queryset.exists():
        slug = f'{base_slug}-{counter}'
        queryset = model_class.objects.filter(**{field_name: slug})
        if instance and instance.pk:
            queryset = queryset.exclude(pk=instance.pk)
        counter += 1
    
    return slug
