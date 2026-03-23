from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.users.permissions import IsEditorUser
from utils.mixins import SlugOrUUIDMixin

from .models import Category
from .serializers import (
    CategoryCreateUpdateSerializer,
    CategoryListSerializer,
    CategorySerializer,
)


class CategoryViewSet(SlugOrUUIDMixin, viewsets.ModelViewSet):
    """
    分类视图集
    
    提供对分类模型的完整 CRUD 操作，支持根据动作动态选择序列化器，
    并对写操作进行编辑权限验证。
    
    Attributes:
        queryset: 查询集，包含所有分类对象
        permission_classes: 权限类列表，读操作允许认证用户或只读，写操作需要编辑权限
        lookup_field: 查找字段名称，用于获取单个对象
        lookup_url_kwarg: URL 关键字参数名称，用于从 URL 中获取查找值
    
    Methods:
        get_serializer_class: 根据当前动作动态返回对应的序列化器类
        get_permissions: 根据当前动作动态返回对应的权限实例列表
    """
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'

    def get_serializer_class(self):
        """
        获取序列化器类
        
        根据当前的 action 动态选择使用对应的序列化器：
        - list 操作使用列表序列化器
        - create、update、partial_update 操作使用创建/更新序列化器
        - 其他操作（如 retrieve）使用详细序列化器
        
        Returns:
            type: 序列化器类，CategoryListSerializer、CategoryCreateUpdateSerializer 或 CategorySerializer
        
        Raises:
            无
        """
        if self.action == 'list':
            return CategoryListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return CategoryCreateUpdateSerializer
        return CategorySerializer

    def get_permissions(self):
        """
        获取权限实例列表
        
        根据当前的 action 动态分配权限：
        - 对于写操作（创建、更新、部分更新、删除），要求用户具备编辑权限
        - 对于读操作，使用默认的权限配置（认证用户或只读）
        
        Returns:
            list: 权限实例列表，包含 IsEditorUser 实例或父类的权限实例
        
        Raises:
            无
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsEditorUser()]
        return super().get_permissions()
