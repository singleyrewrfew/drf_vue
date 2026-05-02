"""
ViewSet Mixin 类

提供常用的 ViewSet 功能扩展。
"""

import uuid
from utils.cache_utils import cache_get, cache_set, get_cache_key, invalidate_pattern
from utils.response import StandardResponse


class StandardListMixin:
    """
    提供统一响应格式的 list 方法

    功能：
    - 自动处理分页
    - 返回 StandardResponse 格式的响应
    """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data).data
            return StandardResponse(paginated_data)

        serializer = self.get_serializer(queryset, many=True)
        return StandardResponse(serializer.data)


class CachedListMixin:
    """
    提供带缓存功能的 list 方法

    功能：
    - 自动缓存列表数据
    - 支持分页（每页独立缓存）
    - 通过 get_cache_scope() 按数据范围隔离缓存，避免不同权限用户数据串读
    - 返回 StandardResponse 格式的响应

    使用方法：
    1. 在 ViewSet 中继承此 Mixin
    2. 设置 cache_key_prefix 属性（如 'categories:list'）
    3. 如果不同角色看到的数据不同，覆盖 get_cache_scope() 返回数据范围标识

    Example:
        class CategoryViewSet(CachedListMixin, viewsets.ModelViewSet):
            cache_key_prefix = 'categories:list'
            # 数据不随角色变化，无需覆盖 get_cache_scope

        class ContentViewSet(CachedListMixin, viewsets.ModelViewSet):
            cache_key_prefix = 'contents:list'

            def get_cache_scope(self, request):
                # 不同角色看到的数据范围不同，需按范围隔离
                if request.user.is_admin or request.user.is_superuser:
                    return 'all'                        # 管理员看全部
                elif request.user.is_editor:
                    return f'own:{request.user.id}'     # 编辑只看自己的，按 user_id 隔离
                return 'published'                      # 其他用户和匿名看已发布
    """

    cache_key_prefix = None
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

    def _invalidate_cache(self):
        if self.cache_key_prefix:
            invalidate_pattern(self.cache_key_prefix)

    def perform_create(self, serializer):
        super().perform_create(serializer)
        self._invalidate_cache()

    def perform_update(self, serializer):
        super().perform_update(serializer)
        self._invalidate_cache()

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        self._invalidate_cache()


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
