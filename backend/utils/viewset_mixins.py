"""
ViewSet Mixin 类

提供常用的 ViewSet 功能扩展。
"""
import uuid
from django.db.models import Prefetch
from drf_spectacular.utils import extend_schema
from utils.cache_utils import cache_get, cache_set, get_cache_key, invalidate_pattern
from utils.response import StandardResponse


class OptimizedQuerySetMixin:
    """
    提供声明式 QuerySet 优化机制

    功能：
    - 支持配置 select_related（外键预加载）
    - 支持配置 prefetch_related（反向关系/多对多预加载）
    - 支持按 action 配置不同的优化策略
    - 自动应用优化，无需手动重写 get_queryset()

    使用方法：
    1. 在 ViewSet 中继承此 Mixin
    2. 设置 select_related_fields 和 prefetch_related_fields 属性
    3. 可选：使用 action_specific_optimizations 为不同 action 配置不同优化

    Example:
        # 基础用法 - 所有 action 使用相同优化
        class CategoryViewSet(OptimizedQuerySetMixin, viewsets.ModelViewSet):
            select_related_fields = ['parent']
            prefetch_related_fields = []

        # 高级用法 - 不同 action 使用不同优化
        class ContentViewSet(OptimizedQuerySetMixin, viewsets.ModelViewSet):
            # 默认优化
            select_related_fields = ['author', 'category']
            prefetch_related_fields = ['tags']

            # 针对特定 action 的优化
            action_specific_optimizations = {
                'list': {
                    'select_related': ['author'],
                    'prefetch_related': ['tags'],
                },
                'retrieve': {
                    'select_related': ['author', 'category'],
                    'prefetch_related': ['tags', 'comments'],
                }
            }

        # 使用 Prefetch 对象进行复杂优化
        from django.db.models import Count, Q, Prefetch

        class AdvancedViewSet(OptimizedQuerySetMixin, viewsets.ModelViewSet):
            def get_prefetch_related(self):
                return [
                    Prefetch(
                        'children',
                        queryset=Model.objects.annotate(count=Count('items')),
                        to_attr='prefetched_children'
                    )
                ]
    """

    # 默认的 select_related 字段列表
    select_related_fields = []

    # 默认的 prefetch_related 字段列表
    prefetch_related_fields = []

    # 针对特定 action 的优化配置
    # 格式: {'action_name': {'select_related': [...], 'prefetch_related': [...]}}
    action_specific_optimizations = {}

    def get_select_related(self):
        """
        获取当前 action 的 select_related 配置

        优先级：
        1. action_specific_optimizations 中的配置
        2. 默认的 select_related_fields

        Returns:
            list: select_related 字段列表
        """
        action_opts = self.action_specific_optimizations.get(self.action, {})
        if 'select_related' in action_opts:
            return action_opts['select_related']
        return self.select_related_fields

    def get_prefetch_related(self):
        """
        获取当前 action 的 prefetch_related 配置

        优先级：
        1. action_specific_optimizations 中的配置
        2. 默认的 prefetch_related_fields

        Returns:
            list: prefetch_related 字段列表或 Prefetch 对象列表
        """
        action_opts = self.action_specific_optimizations.get(self.action, {})
        if 'prefetch_related' in action_opts:
            return action_opts['prefetch_related']
        return self.prefetch_related_fields

    def get_queryset(self):
        """
        获取优化后的查询集

        自动应用 select_related 和 prefetch_related 优化。
        子类可以在 super().get_queryset() 后继续添加其他过滤逻辑。
        """
        queryset = super().get_queryset()

        # 应用 select_related
        select_related = self.get_select_related()
        if select_related:
            queryset = queryset.select_related(*select_related)

        # 应用 prefetch_related
        prefetch_related = self.get_prefetch_related()
        if prefetch_related:
            queryset = queryset.prefetch_related(*prefetch_related)

        return queryset


class StandardListMixin:
    """
    提供统一响应格式的 list 方法

    功能：
    - 自动处理分页
    - 返回 StandardResponse 格式的响应
    """

    @extend_schema(
        summary='列出资源',
        description='获取资源列表，支持分页和过滤'
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data).data
            return StandardResponse(paginated_data)

        serializer = self.get_serializer(queryset, many=True)
        return StandardResponse(serializer.data)


class CacheInvalidationMixin:
    """
    提供灵活的缓存失效机制

    功能：
    - 支持主缓存失效（当前 ViewSet 的列表缓存）
    - 支持额外缓存模式失效（通过 additional_cache_patterns 配置）
    - 支持自定义失效逻辑（通过重写 post_invalidate_cache hook）

    使用方法：
    1. 在 ViewSet 中继承此 Mixin
    2. 设置 cache_key_prefix 属性（如 'categories:list'）
    3. 可选：设置 additional_cache_patterns 列表，指定需要额外清除的缓存模式
    4. 可选：重写 post_invalidate_cache() 方法添加自定义失效逻辑

    Example:
        # 基础用法 - 只清除自身缓存
        class CategoryViewSet(CacheInvalidationMixin, viewsets.ModelViewSet):
            cache_key_prefix = 'categories:list'

        # 高级用法 - 清除多个相关缓存
        class ContentViewSet(CacheInvalidationMixin, viewsets.ModelViewSet):
            cache_key_prefix = 'contents:list'
            additional_cache_patterns = ['stats', 'popular_authors']

            def post_invalidate_cache(self):
                # 自定义失效逻辑
                logger.info('Content cache invalidated')
    """

    cache_key_prefix = None
    additional_cache_patterns = []

    def _invalidate_main_cache(self):
        """清除主缓存（当前 ViewSet 的列表缓存）"""
        if self.cache_key_prefix:
            invalidate_pattern(self.cache_key_prefix)

    def _invalidate_additional_caches(self):
        """清除额外的缓存模式"""
        for pattern in self.additional_cache_patterns:
            invalidate_pattern(pattern)

    def post_invalidate_cache(self):
        """
        缓存失效后的钩子方法

        子类可以重写此方法添加自定义的缓存失效逻辑。
        在主要缓存和额外缓存都清除后调用。
        """
        pass

    def _invalidate_cache(self):
        """
        执行完整的缓存失效流程

        流程：
        1. 清除主缓存
        2. 清除额外缓存
        3. 调用钩子方法
        """
        self._invalidate_main_cache()
        self._invalidate_additional_caches()
        self.post_invalidate_cache()

    def perform_create(self, serializer):
        super().perform_create(serializer)
        self._invalidate_cache()

    def perform_update(self, serializer):
        super().perform_update(serializer)
        self._invalidate_cache()

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        self._invalidate_cache()


class CachedListMixin(CacheInvalidationMixin):
    """
    提供带缓存功能的 list 方法

    功能：
    - 自动缓存列表数据
    - 支持分页（每页独立缓存）
    - 通过 get_cache_scope() 按数据范围隔离缓存，避免不同权限用户数据串读
    - 返回 StandardResponse 格式的响应
    - 自动在增删改操作时清除缓存（继承自 CacheInvalidationMixin）

    使用方法：
    1. 在 ViewSet 中继承此 Mixin
    2. 设置 cache_key_prefix 属性（如 'categories:list'）
    3. 如果不同角色看到的数据不同，覆盖 get_cache_scope() 返回数据范围标识
    4. 可选：设置 additional_cache_patterns 清除额外的相关缓存

    Example:
        # 基础用法
        class CategoryViewSet(CachedListMixin, viewsets.ModelViewSet):
            cache_key_prefix = 'categories:list'
            # 数据不随角色变化，无需覆盖 get_cache_scope

        # 高级用法 - 多缓存清除
        class ContentViewSet(CachedListMixin, viewsets.ModelViewSet):
            cache_key_prefix = 'contents:list'
            additional_cache_patterns = ['stats', 'popular_authors']

            def get_cache_scope(self, request):
                # 不同角色看到的数据范围不同，需按范围隔离
                # is_admin 已包含 is_superuser 检查
                if request.user.is_admin:
                    return 'all'                        # 管理员看全部
                elif request.user.is_editor:
                    return f'own:{request.user.id}'     # 编辑只看自己的，按 user_id 隔离
                return 'published'                      # 其他用户和匿名看已发布
    """

    cache_timeout = 300

    def get_cache_scope(self, request):
        """
        返回当前请求的数据范围标识，用于缓存 key 隔离

        默认返回 'all'（所有用户共享同一份数据）。
        如果不同角色/用户看到的数据不同，必须在子类中覆盖此方法。

        返回值会作为缓存 key 的一部分，相同 scope 的请求共享缓存。
        因此 scope 必须准确反映数据范围，否则会导致：
        - scope 过大：数据泄露（低权限用户看到高权限数据）
        - scope 过小：缓存命中率低（相同数据存多份）

        Returns:
            str: 数据范围标识，如 'all'、'published'、'own:{user_id}'
        """
        return 'all'

    def _get_cache_key(self, request):
        """生成包含数据范围和分页参数的缓存键"""
        scope = self.get_cache_scope(request)
        parts = [scope]

        limit = request.query_params.get('limit')
        offset = request.query_params.get('offset')
        if limit is not None:
            parts.append(f'limit:{limit}')
        if offset is not None:
            parts.append(f'offset:{offset}')

        return get_cache_key(self.cache_key_prefix, *parts)

    @extend_schema(
        summary='列出资源（带缓存）',
        description='获取资源列表，支持分页、过滤和缓存'
    )
    def list(self, request, *args, **kwargs):
        if not self.cache_key_prefix:
            return super().list(request, *args, **kwargs)

        cache_key = self._get_cache_key(request)
        cached_data = cache_get(cache_key)
        if cached_data:
            return StandardResponse(cached_data)

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data).data
            cache_set(cache_key, paginated_data, self.cache_timeout)
            return StandardResponse(paginated_data)

        serializer = self.get_serializer(queryset, many=True)
        cache_set(cache_key, serializer.data, self.cache_timeout)
        return StandardResponse(serializer.data)




class SlugOrUUIDMixin:
    """
    支持通过 slug 或 UUID 查找对象的 Mixin

    使用方法：
    1. 在 ViewSet 中继承此 Mixin
    2. 确保模型有 slug 字段和 UUID 主键（或 id 字段）

    功能：
    - 自动识别 lookup_field 的值是 slug 还是 UUID
    - 如果是 UUID，直接按 ID 查找
    - 如果是 slug，按 slug 字段查找

    Example:
        class CategoryViewSet(SlugOrUUIDMixin, viewsets.ModelViewSet):
            queryset = Category.objects.all()
            lookup_field = 'pk'  # 可以是 pk、id 或 slug
    """

    def get_object(self):
        """
        重写获取对象方法，支持 slug 或 UUID

        根据 lookup_field 的值智能判断：
        - 如果是有效的 UUID 格式，按主键查找
        - 否则尝试按 slug 字段查找（如果模型有 slug 字段）
        - 最后按主键查找
        """
        queryset = self.filter_queryset(self.get_queryset())

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs[lookup_url_kwarg]

        try:
            uuid.UUID(str(lookup_value))
            filter_kwargs = {self.lookup_field: lookup_value}
        except (ValueError, AttributeError):
            model = self.queryset.model
            if hasattr(model, 'slug'):
                filter_kwargs = {'slug': lookup_value}
            else:
                filter_kwargs = {self.lookup_field: lookup_value}

        obj = queryset.filter(**filter_kwargs).first()

        if obj is None:
            from rest_framework.exceptions import NotFound
            raise NotFound(f'未找到{self.queryset.model._meta.verbose_name}')

        self.check_object_permissions(self.request, obj)

        return obj
