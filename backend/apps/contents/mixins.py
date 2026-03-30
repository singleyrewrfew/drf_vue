from rest_framework.permissions import IsAuthenticatedOrReadOnly
from apps.users.permissions import IsEditorUser, IsOwnerOrAdmin


class ContentPermissionMixin:
    """
    内容权限控制 Mixin
    
    只负责处理权限相关逻辑，符合单一职责原则
    """
    
    def get_permissions(self):
        """根据 action 动态分配权限"""
        if self.action in ['create']:
            return [IsEditorUser()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return super().get_permissions()


class ContentSerializerMixin:
    """
    内容序列化器选择 Mixin
    
    只负责根据 action 选择合适的序列化器
    """
    
    # 序列化器映射配置 - 使用配置化代替条件判断
    SERIALIZER_MAPPING = {
        'list': None,  # 在 get_serializer_class 中动态设置
        'create': None,
        'update': None,
        'partial_update': None,
    }
    
    def get_serializer_class(self):
        """根据 action 选择合适的序列化器"""
        serializer_mapping = self._get_serializer_mapping()
        return serializer_mapping.get(self.action, self.default_serializer_class)
    
    def _get_serializer_mapping(self):
        """获取序列化器映射（由子类实现）"""
        raise NotImplementedError("子类必须实现 _get_serializer_mapping 方法")


class ContentQuerySetMixin:
    """
    内容查询集构建 Mixin
    
    只负责处理查询集和过滤逻辑
    """
    
    def get_queryset(self):
        """获取基础查询集（预加载关联数据）"""
        queryset = super().get_queryset()
        
        # 预加载关联数据，避免 N+1 查询
        queryset = queryset.select_related('author', 'category')\
                          .prefetch_related('tags')
        
        # 应用过滤
        queryset = self._apply_filters(queryset)
        
        return queryset
    
    def _apply_filters(self, queryset):
        """
        应用请求参数过滤
        
        Args:
            queryset: 基础查询集
            
        Returns:
            QuerySet: 过滤后的查询集
        """
        # 分类过滤
        category = self.request.query_params.get('category')
        if category:
            queryset = self._filter_by_category(queryset, category)
        
        # 标签过滤
        tag = self.request.query_params.get('tag')
        if tag:
            queryset = self._filter_by_tag(queryset, tag)
        
        # 作者过滤
        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(author_id=author)
        
        # 搜索
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)
        
        return queryset
    
    def _filter_by_category(self, queryset, category):
        """按分类过滤"""
        from apps.categories.models import Category
        import uuid
        
        category_obj = None
        
        # 1. 先尝试通过 slug 查找（最常见的情况）
        category_obj = Category.objects.filter(slug=category).first()
        
        # 2. 如果没找到，尝试通过 UUID 查找
        if not category_obj:
            try:
                # 验证是否为有效的 UUID 格式
                uuid.UUID(str(category))
                category_obj = Category.objects.filter(id=category).first()
            except (ValueError, AttributeError):
                # 不是有效的 UUID，忽略
                pass
        
        if category_obj:
            return queryset.filter(category=category_obj)
        
        # 如果都没找到，返回空查询集
        return queryset.none()
    
    def _filter_by_tag(self, queryset, tag):
        """按标签过滤"""
        from apps.tags.models import Tag
        import uuid
        
        tag_obj = None
        
        # 1. 先尝试通过 slug 查找（最常见的情况）
        tag_obj = Tag.objects.filter(slug=tag).first()
        
        # 2. 如果没找到，尝试通过 UUID 查找
        if not tag_obj:
            try:
                # 验证是否为有效的 UUID 格式
                uuid.UUID(str(tag))
                tag_obj = Tag.objects.filter(id=tag).first()
            except (ValueError, AttributeError):
                # 不是有效的 UUID，忽略
                pass
        
        if tag_obj:
            return queryset.filter(tags=tag_obj)
        
        # 如果都没找到，返回空查询集
        return queryset.none()
