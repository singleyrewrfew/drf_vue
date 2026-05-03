from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.conf import settings
from django.db.models import Count, Q

from apps.users.permissions import IsEditorUser
from utils.viewset_mixins import CachedListMixin, OptimizedQuerySetMixin, SlugOrUUIDMixin
from .models import Tag
from .serializers import TagCreateUpdateSerializer, TagSerializer


class TagSerializerMixin:
    default_serializer_class = TagSerializer

    def get_serializer_class(self):
        serializer_mapping = {
            'create': TagCreateUpdateSerializer,
            'update': TagCreateUpdateSerializer,
            'partial_update': TagCreateUpdateSerializer,
        }
        return serializer_mapping.get(self.action, self.default_serializer_class)


class TagPermissionMixin:
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsEditorUser()]
        return super().get_permissions()


class TagViewSet(
    CachedListMixin,
    OptimizedQuerySetMixin,
    TagPermissionMixin,
    TagSerializerMixin,
    SlugOrUUIDMixin,
    viewsets.ModelViewSet
):
    """
    标签视图集
    
    缓存配置：
    - cache_key_prefix: 'tags:list' - 列表缓存前缀
    - cache_timeout: 使用 settings.CACHE_TTL['TAG_LIST']
    
    QuerySet 优化配置：
    - 自动为所有查询添加内容数量统计
    
    扩展示例（如需清除额外缓存）：
        additional_cache_patterns = ['content_tags', 'trending_tags']
        
        def post_invalidate_cache(self):
            # 自定义缓存失效逻辑
            from utils.cache_utils import invalidate_pattern
            invalidate_pattern('custom_pattern')
    """
    cache_key_prefix = 'tags:list'
    cache_timeout = settings.CACHE_TTL['TAG_LIST']
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    
    # QuerySet 优化配置（Tag 没有外键，无需 select_related）
    select_related_fields = []
    prefetch_related_fields = []

    def get_queryset(self):
        """
        获取优化后的查询集
        
        在 OptimizedQuerySetMixin 的基础上，添加 annotate 统计信息。
        """
        queryset = super().get_queryset()
        
        # 为所有 action 添加内容数量统计
        queryset = queryset.annotate(
            content_count=Count('contents', filter=Q(contents__status='published'))
        )
        
        return queryset
