from django.utils.text import slugify
from rest_framework import serializers
from .models import Tag

class TagSerializer(serializers.ModelSerializer):
    """
    标签序列化器
    
    用于返回标签信息，包含内容数量
    """
    # 内容数量：使用方法字段动态计算
    content_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Tag
        # 包含的字段：ID、名称、slug、创建时间、内容数量
        fields = ['id', 'name', 'slug', 'created_at', 'content_count']
        # 只读字段：不允许通过 API 修改
        read_only_fields = ['id', 'slug', 'created_at']
    
    def get_content_count(self, obj):
        """
        获取标签关联的已发布内容数量
        
        返回：
            标签关联的已发布文章数量
        """
        return obj.contents.filter(status='published').count()

class TagCreateUpdateSerializer(serializers.ModelSerializer):
    """
    标签创建和更新序列化器
    
    用于创建和更新标签，自动生成 slug
    """
    class Meta:
        model = Tag
        # 创建和更新时可以修改的字段
        fields = ['name', 'slug']
    
    def validate(self, data):
        """
        验证并自动生成 slug
        
        步骤：
        1. 如果 slug 为空，自动生成
        2. 使用 slugify 生成基础 slug
        3. 如果 slug 已存在，添加数字后缀
        """
        if not data.get('slug'):
            base_slug = slugify(data['name'])
            slug = base_slug
            counter = 1
            # 检查 slug 是否已存在，如果存在则添加数字后缀
            while Tag.objects.filter(slug=slug).exclude(id=self.instance.id if self.instance else None).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            data['slug'] = slug
        return data
