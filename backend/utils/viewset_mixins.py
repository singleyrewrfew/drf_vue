"""
ViewSet Mixin 类

提供常用的 ViewSet 功能扩展。
"""

import uuid
from django.core.cache import cache
from utils.cache_utils import get_cache_key, invalidate_pattern
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
    - 返回 StandardResponse 格式的响应

    使用方法：
    1. 在 ViewSet 中继承此 Mixin
    2. 设置 cache_key_prefix 属性（如 'categories:list'）

    Example:
        class CategoryViewSet(CachedListMixin, viewsets.ModelViewSet):
            cache_key_prefix = 'categories:list'
    """

    cache_key_prefix = None
    cache_timeout = 300

    def _get_cache_key(self, request):
        """生成包含分页参数的缓存键"""
        limit = request.query_params.get('limit', '')
        offset = request.query_params.get('offset', '')
        return get_cache_key(self.cache_key_prefix, limit, offset)

    def list(self, request, *args, **kwargs):
        if not self.cache_key_prefix:
            return super().list(request, *args, **kwargs)

        cache_key = self._get_cache_key(request)
        cached_data = cache.get(cache_key)
        if cached_data:
            return StandardResponse(cached_data)

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data).data
            cache.set(cache_key, paginated_data, self.cache_timeout)
            return StandardResponse(paginated_data)

        serializer = self.get_serializer(queryset, many=True)
        cache.set(cache_key, serializer.data, self.cache_timeout)
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
