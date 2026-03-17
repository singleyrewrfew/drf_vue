from rest_framework import serializers
from utils.serializer_mixins import AutoSlugMixin
from .models import Tag

class TagSerializer(serializers.ModelSerializer):
    """
    标签序列化器
    
    用于返回标签信息，包含内容数量
    """
    content_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'created_at', 'content_count']
        read_only_fields = ['id', 'slug', 'created_at']
    
    def get_content_count(self, obj):
        """
        获取标签关联的已发布内容数量
        
        返回：
            标签关联的已发布文章数量
        """
        return obj.contents.filter(status='published').count()

class TagCreateUpdateSerializer(AutoSlugMixin, serializers.ModelSerializer):
    """
    标签创建和更新序列化器
    
    用于创建和更新标签，自动生成 slug
    """
    slug_source_field = 'name'
    
    class Meta:
        model = Tag
        fields = ['name', 'slug']
