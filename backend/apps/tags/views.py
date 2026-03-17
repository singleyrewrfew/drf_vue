from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from apps.users.permissions import IsEditorUser
from utils.mixins import SlugOrUUIDMixin
from .models import Tag
from .serializers import TagCreateUpdateSerializer, TagSerializer

class TagViewSet(SlugOrUUIDMixin, viewsets.ModelViewSet):
    """
    标签视图集
    
    提供标签相关的 API 端点：
    - 列表、创建、更新、删除
    - 支持通过 UUID 或 slug 查找标签
    """
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    
    def get_serializer_class(self):
        """
        根据不同的操作返回不同的序列化器
        
        序列化器映射：
        - create/update/partial_update: TagCreateUpdateSerializer（创建和更新）
        - 其他: TagSerializer（读取）
        """
        if self.action in ['create', 'update', 'partial_update']:
            return TagCreateUpdateSerializer
        return TagSerializer
    
    def get_permissions(self):
        """
        根据不同的操作返回不同的权限类
        
        权限规则：
        - create/update/partial_update/destroy: 需要编辑者权限
        - 其他: 使用默认权限（认证用户可读写，未认证用户只读）
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsEditorUser()]
        return super().get_permissions()
