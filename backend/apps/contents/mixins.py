from apps.users.permissions import IsEditorUser, IsOwnerOrAdmin
from utils.query_utils import get_object_by_slug_or_id


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

    SERIALIZER_MAPPING = {
        'list': None,
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
        queryset = queryset.select_related('author', 'category').prefetch_related('tags')
        return self._apply_filters(queryset)

    def _apply_filters(self, queryset):
        """应用请求参数过滤"""
        category = self.request.query_params.get('category')
        if category:
            queryset = self._filter_by_category(queryset, category)

        tag = self.request.query_params.get('tag')
        if tag:
            queryset = self._filter_by_tag(queryset, tag)

        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(author_id=author)

        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)

        return queryset

    def _filter_by_category(self, queryset, category):
        """按分类过滤（支持 slug 或 UUID）"""
        from apps.categories.models import Category

        category_obj = get_object_by_slug_or_id(Category, category)
        return queryset.filter(category=category_obj) if category_obj else queryset.none()

    def _filter_by_tag(self, queryset, tag):
        """按标签过滤（支持 slug 或 UUID）"""
        from apps.tags.models import Tag

        tag_obj = get_object_by_slug_or_id(Tag, tag)
        return queryset.filter(tags=tag_obj) if tag_obj else queryset.none()
