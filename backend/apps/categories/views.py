from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.users.permissions import IsEditorUser
from utils.mixins import SlugOrUUIDMixin
from utils.response import StandardResponse

from .models import Category
from .serializers import (
    CategoryCreateUpdateSerializer,
    CategoryListSerializer,
    CategorySerializer,
)


class CategorySerializerMixin:
    """分类序列化器选择 Mixin"""
    
    default_serializer_class = CategorySerializer
    
    def get_serializer_class(self):
        """根据 action 选择合适的序列化器（配置化）"""
        serializer_mapping = {
            'list': CategoryListSerializer,
            'create': CategoryCreateUpdateSerializer,
            'update': CategoryCreateUpdateSerializer,
            'partial_update': CategoryCreateUpdateSerializer,
        }
        return serializer_mapping.get(self.action, self.default_serializer_class)


class CategoryPermissionMixin:
    """分类权限控制 Mixin"""
    
    def get_permissions(self):
        """根据 action 动态分配权限"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsEditorUser()]
        return super().get_permissions()


class CategoryViewSet(
    CategoryPermissionMixin,
    CategorySerializerMixin,
    SlugOrUUIDMixin,
    viewsets.ModelViewSet
):
    """分类视图集 - 提供分类的 CRUD 操作"""
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    # 作用：指定数据库模型中，用于检索单个对象的字段名。
    # 原理：当请求 /api/items/1/ 时，DRF 会执行查询：Item.objects.get(pk=1)。
    lookup_field = 'pk'
    # 作用：指定 URL 路径中，传递参数的关键字名称
    # 原理：DRF 会从 URL 的关键字参数 self.kwargs 中，取出名为 pk 的值（如 1），然后用它去匹配 lookup_field（pk）。
    lookup_url_kwarg = 'pk'

    def list(self, request, *args, **kwargs):
        """
        获取分类列表（统一响应格式）
        
        Args:
            request: HTTP 请求对象
            *args: 位置参数
            **kwargs: 关键字参数
        
        Returns:
            Response: 包含分页数据的统一格式响应，HTTP 状态码为 200
        
        Raises:
            无
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data).data
            return StandardResponse(paginated_data)
        
        serializer = self.get_serializer(queryset, many=True)
        return StandardResponse(serializer.data)
