from rest_framework import serializers

from utils.serializer_mixins import AutoSlugMixin
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    分类序列化器 - 用于完整的分类数据序列化
    
    功能：
    - 支持嵌套的子分类数据（children）
    - 计算已发布内容数量（content_count）
    - 提供完整的分类信息，包括所有字段和关联数据
    
    使用场景：
    - 单个分类详情查询（retrieve）
    - 删除操作时返回完整数据
    - 需要展示完整分类树结构的场景
    
    Attributes:
        children: SerializerMethodField，递归序列化子分类列表
        content_count: SerializerMethodField，统计该分类下已发布的内容数量
    """
    children = serializers.SerializerMethodField()
    content_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'description', 'sort_order', 'created_at', 'children', 'content_count']
        read_only_fields = ['id', 'slug', 'created_at']

    def get_children(self, obj):
        """
        获取并序列化子分类列表（递归）
        
        Args:
            self: 序列化器实例
            obj: Category 模型实例，当前要序列化的分类对象
        
        Returns:
            list: 子分类的序列化数据列表，每个子分类也使用 CategorySerializer 进行递归序列化，
                  形成嵌套的树形结构数据。如果没有子分类则返回空列表 []
        
        Raises:
            无
        """
        children = obj.children.all()
        return CategorySerializer(children, many=True).data

    def get_content_count(self, obj):
        """
        获取分类下已发布内容的数量
        
        Args:
            self: 序列化器实例
            obj: Category 模型实例，当前要序列化的分类对象
        
        Returns:
            int: 该分类下状态为 'published' 的内容数量，通过反向关系 obj.contents 查询得到。
                 如果没有已发布内容则返回 0
        
        Raises:
            无
        """
        return obj.contents.filter(status='published').count()


class CategoryListSerializer(serializers.ModelSerializer):
    """
    分类列表序列化器 - 用于列表展示的分类数据序列化
    
    功能：
    - 提供父分类名称（parent_name），避免前端二次请求
    - 计算已发布内容数量（content_count）
    - 扁平化数据结构，不包含嵌套的子分类，适合列表展示
    
    与 CategorySerializer 的区别：
    - 不包含 children 字段，避免深层嵌套导致的性能问题
    - 添加 parent_name 字段，直接显示父分类名称而非仅 ID
    - 更适合列表页批量展示场景
    
    Attributes:
        parent_name: CharField，从父分类对象获取名称（source='parent.name'），只读
        content_count: SerializerMethodField，统计该分类下已发布的内容数量
    """
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    content_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'parent_name', 'description', 'sort_order', 'created_at', 'content_count']

    def get_content_count(self, obj):
        """
        获取分类下已发布内容的数量
        
        Args:
            self: 序列化器实例
            obj: Category 模型实例，当前要序列化的分类对象
        
        Returns:
            int: 该分类下状态为 'published' 的内容数量，通过反向关系 obj.contents 查询得到。
                 如果没有已发布内容则返回 0
        
        Raises:
            无
        """
        return obj.contents.filter(status='published').count()


class CategoryCreateUpdateSerializer(AutoSlugMixin, serializers.ModelSerializer):
    """
    分类创建/更新序列化器 - 用于分类的增删改操作
    
    功能：
    - 集成 AutoSlugMixin，根据 name 字段自动生成唯一的 slug
    - 提供分类创建和更新所需的字段验证和序列化
    - 不包含只读字段（如 created_at）和计算字段（如 content_count）
    
    Mixin 说明：
    - AutoSlugMixin: 自动从 slug_source_field 指定的字段生成 slug，确保唯一性
    
    使用场景：
    - 创建新分类（create）
    - 更新现有分类（update/partial_update）
    
    Attributes:
        slug_source_field: str，指定用于生成 slug 的源字段名，这里使用 'name' 字段
    """
    slug_source_field = 'name'
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'description', 'sort_order']
