from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.users.permissions import IsEditorUser
from utils.viewset_mixins import SlugOrUUIDMixin
from utils.response import StandardResponse

from .models import Category
from .serializers import (
    CategoryCreateUpdateSerializer,
    CategoryListSerializer,
    CategorySerializer,
)


class CategorySerializerMixin:
    """
    分类序列化器选择 Mixin
    
    功能：
    - 根据不同的视图动作（action）动态选择合适的序列化器
    - 提供默认的序列化器配置
    
    使用场景：
    - list: 使用 CategoryListSerializer，返回扁平化的列表数据
    - create/update/partial_update: 使用 CategoryCreateUpdateSerializer，支持自动 slug 生成
    - retrieve/destroy: 使用默认的 CategorySerializer，返回完整的嵌套数据
    """
    
    default_serializer_class = CategorySerializer
    
    def get_serializer_class(self):
        """
        根据 action 选择合适的序列化器（配置化）
        
        Args:
            self: 视图集实例，包含 action 属性标识当前请求的动作
        
        Returns:
            type: 序列化器类，根据 action 从映射表中获取对应的序列化器类，
                  如果 action 不在映射表中则返回 default_serializer_class
        
        Raises:
            无
        """
        serializer_mapping = {
            'list': CategoryListSerializer,
            'create': CategoryCreateUpdateSerializer,
            'update': CategoryCreateUpdateSerializer,
            'partial_update': CategoryCreateUpdateSerializer,
        }
        return serializer_mapping.get(self.action, self.default_serializer_class)


class CategoryPermissionMixin:
    """
    分类权限控制 Mixin
    
    功能：
    - 根据不同的视图动作动态分配权限
    - 写操作（增删改）需要编辑者权限
    - 读操作使用基类的默认权限配置（IsAuthenticatedOrReadOnly）
    
    权限策略：
    - create/update/partial_update/destroy: 需要 IsEditorUser 权限
    - list/retrieve: 继承基类权限（允许任何人读取，认证用户可写入）
    """
    
    def get_permissions(self):
        """
        根据 action 动态分配权限
        
        Args:
            self: 视图集实例，包含 action 属性标识当前请求的动作
        
        Returns:
            list: 权限对象列表，对于写操作返回 [IsEditorUser()]，
                  其他操作调用父类的 get_permissions 方法
        
        Raises:
            无
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsEditorUser()]
        return super().get_permissions()


class CategoryViewSet(
    CategoryPermissionMixin,
    CategorySerializerMixin,
    SlugOrUUIDMixin,
    viewsets.ModelViewSet
):
    """
    分类视图集 - 提供分类的 CRUD 操作
    
    功能：
    - 提供分类的完整 CRUD 功能（创建、查询、更新、删除）
    - 支持通过 UUID 或 slug 查找单个分类对象（SlugOrUUIDMixin）
    - 根据操作类型动态选择序列化器（CategorySerializerMixin）
    - 根据操作类型动态分配权限（CategoryPermissionMixin）
    - 列表查询支持分页和统一响应格式
    
    Mixin 继承顺序说明：
    - CategoryPermissionMixin: 优先处理权限逻辑
    - CategorySerializerMixin: 其次处理序列化器选择
    - SlugOrUUIDMixin: 提供对象查找增强功能
    - viewsets.ModelViewSet: DRF 基础视图集功能
    
    Attributes:
        queryset: 查询集，获取所有分类对象
        permission_classes: 默认权限类列表，允许任何人读取，认证用户可写入
        lookup_field: 指定用于检索单个对象的数据库字段名，默认为 'pk'（主键）
        lookup_url_kwarg: 指定 URL 路径中传递参数的关键字名称，与 lookup_field 对应
    """
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
