from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from apps.users.permissions import IsEditorUser
from utils.mixins import SlugOrUUIDMixin
from utils.response import StandardResponse
from .models import Tag
from .serializers import TagCreateUpdateSerializer, TagSerializer


class TagSerializerMixin:
    """标签序列化器选择 Mixin"""

    default_serializer_class = TagSerializer

    def get_serializer_class(self):
        """根据 action 选择合适的序列化器（配置化）"""
        serializer_mapping = {
            'create': TagCreateUpdateSerializer,
            'update': TagCreateUpdateSerializer,
            'partial_update': TagCreateUpdateSerializer,
        }
        return serializer_mapping.get(self.action, self.default_serializer_class)


class TagPermissionMixin:
    """标签权限控制 Mixin"""

    def get_permissions(self):
        """根据 action 动态分配权限"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsEditorUser()]  # 仅编辑可写
        return super().get_permissions()


class TagViewSet(
    TagPermissionMixin,
    TagSerializerMixin,
    SlugOrUUIDMixin,
    viewsets.ModelViewSet
):
    """标签视图集 - 提供标签的 CRUD 操作"""
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'

    def list(self, request, *args, **kwargs):
        """
        获取标签列表（统一响应格式）

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
