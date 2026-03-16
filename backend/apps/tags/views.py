from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from apps.users.permissions import IsEditorUser
from .models import Tag
from .serializers import TagCreateUpdateSerializer, TagSerializer

class TagViewSet(viewsets.ModelViewSet):
    """
    标签视图集
    
    提供标签相关的 API 端点：
    - 列表、创建、更新、删除
    - 支持通过 UUID 或 slug 查找标签
    """
    queryset = Tag.objects.all()
    # 默认权限：认证用户可读写，未认证用户只读
    permission_classes = [IsAuthenticatedOrReadOnly]
    # 查找字段：主键
    lookup_field = 'pk'
    # URL 参数名：用于路由
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
    
    def get_object(self):
        """
        获取单个标签对象
        
        功能：
        - 支持通过 UUID 查找
        - 支持通过 slug 查找
        - 自动检查对象权限
        """
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs.get(lookup_url_kwarg)
        
        # 尝试通过 slug 或 UUID 查找
        try:
            import uuid
            uuid.UUID(lookup_value)
            # 如果是有效的 UUID，使用默认查找方式
            return super().get_object()
        except (ValueError, AttributeError):
            # 如果不是有效的 UUID，尝试通过 slug 查找
            try:
                obj = Tag.objects.get(slug=lookup_value)
                # 检查对象权限
                self.check_object_permissions(self.request, obj)
                return obj
            except Tag.DoesNotExist:
                from django.http import Http404
                raise Http404('No Tag matches the given query.')
    
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
