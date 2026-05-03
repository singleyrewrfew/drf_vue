from django.db.models import Count, Prefetch, Q
from django.conf import settings
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.users.permissions import IsEditorUser
from utils.viewset_mixins import CachedListMixin, OptimizedQuerySetMixin, SlugOrUUIDMixin

from .models import Category
from .serializers import (
    CategoryCreateUpdateSerializer,
    CategoryListSerializer,
    CategorySerializer,
)


class CategorySerializerMixin:
    default_serializer_class = CategorySerializer

    def get_serializer_class(self):
        serializer_mapping = {
            'list': CategoryListSerializer,
            'create': CategoryCreateUpdateSerializer,
            'update': CategoryCreateUpdateSerializer,
            'partial_update': CategoryCreateUpdateSerializer,
        }
        return serializer_mapping.get(self.action, self.default_serializer_class)


class CategoryPermissionMixin:
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsEditorUser()]
        return super().get_permissions()


@extend_schema_view(
    list=extend_schema(summary='列出分类', description='获取分类列表，支持分页'),
    retrieve=extend_schema(summary='获取分类详情', description='获取单个分类的详细信息'),
    create=extend_schema(summary='创建分类', description='创建新的分类（需要编辑权限）'),
    update=extend_schema(summary='更新分类', description='更新分类信息（需要编辑权限）'),
    partial_update=extend_schema(summary='部分更新分类', description='部分更新分类信息（需要编辑权限）'),
    destroy=extend_schema(summary='删除分类', description='删除分类（需要编辑权限）'),
)
class CategoryViewSet(
    CachedListMixin,
    OptimizedQuerySetMixin,
    CategoryPermissionMixin,
    CategorySerializerMixin,
    SlugOrUUIDMixin,
    viewsets.ModelViewSet
):
    """
    分类视图集
    
    缓存配置：
    - cache_key_prefix: 'categories:list' - 列表缓存前缀
    - cache_timeout: 使用 settings.CACHE_TTL['CATEGORY_LIST']
    
    QuerySet 优化配置：
    - select_related_fields: ['parent'] - 预加载父分类
    - action_specific_optimizations: 针对 retrieve 动作的复杂优化
    
    扩展示例（如需清除额外缓存）：
        additional_cache_patterns = ['content_categories', 'related_stats']
        
        def post_invalidate_cache(self):
            # 自定义缓存失效逻辑
            from utils.cache_utils import invalidate_pattern
            invalidate_pattern('custom_pattern')
    """
    cache_key_prefix = 'categories:list'
    cache_timeout = settings.CACHE_TTL['CATEGORY_LIST']
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    
    # QuerySet 优化配置
    select_related_fields = ['parent']
    prefetch_related_fields = []
    
    # 针对不同 action 的优化配置
    action_specific_optimizations = {
        'list': {
            'select_related': ['parent'],
            'prefetch_related': [],
        },
        'retrieve': {
            'select_related': ['parent'],
            'prefetch_related': [
                Prefetch(
                    'children',
                    queryset=Category.objects.annotate(
                        content_count=Count('contents', filter=Q(contents__status='published'))
                    ),
                    to_attr='prefetched_children'
                )
            ],
        }
    }

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
