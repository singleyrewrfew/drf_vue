"""
序列化器 Mixin 类

提供常用的序列化器功能扩展。
"""

from rest_framework import serializers
from utils.slug_utils import generate_unique_slug


class AutoSlugMixin:
    """
    自动生成 slug 的 Mixin
    
    使用方法：
    1. 在序列化器中继承此 Mixin
    2. 设置 slug_source_field 指定用于生成 slug 的字段名
    3. slug 字段必须是只读的（read_only_fields 中包含 'slug'）
    
    Example:
        class CategoryCreateUpdateSerializer(AutoSlugMixin, serializers.ModelSerializer):
            slug_source_field = 'name'
            
            class Meta:
                model = Category
                fields = ['id', 'name', 'slug']
                read_only_fields = ['id', 'slug']
    """
    slug_source_field = None  # 需要在子类中指定
    
    def validate(self, attrs):
        """
        验证数据时自动生成 slug

        如果 slug 字段为空且指定了 slug_source_field，
        则根据源字段自动生成唯一的 slug。
        """
        if not self.slug_source_field:
            return super().validate(attrs)

        slug_value = attrs.get('slug')
        if slug_value:
            return super().validate(attrs)

        source_value = attrs.get(self.slug_source_field)
        if not source_value:
            return super().validate(attrs)

        model_class = self.Meta.model
        instance = getattr(self, 'instance', None)

        attrs['slug'] = generate_unique_slug(
            model_class=model_class,
            name=source_value,
            instance=instance,
            field_name='slug'
        )

        return super().validate(attrs)
