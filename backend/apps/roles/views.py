from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.users.permissions import IsAdminUser

from .models import Permission, Role
from .serializers import PermissionSerializer, RoleListSerializer, RoleSerializer


class PermissionViewSet(viewsets.ModelViewSet):
    """
    权限视图集
    
    提供对权限模型的完整 CRUD 操作，仅允许认证且具备管理员权限的用户访问。
    
    Attributes:
        queryset: 查询集，包含所有权限对象
        serializer_class: 序列化器类，用于处理权限数据的序列化和反序列化
        permission_classes: 权限类列表，要求用户必须认证且为管理员
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class RoleViewSet(viewsets.ModelViewSet):
    """
    角色视图集
    
    提供对角色模型的完整 CRUD 操作，支持预加载关联的权限数据，
    仅允许认证且具备管理员权限的用户访问。
    
    Attributes:
        queryset: 查询集，包含所有角色对象并预加载关联的权限数据
        permission_classes: 权限类列表，要求用户必须认证且为管理员
    
    Methods:
        get_serializer_class: 根据当前动作动态返回对应的序列化器类
    """
    queryset = Role.objects.prefetch_related('permissions')
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        """
        获取序列化器类
        
        根据当前的 action 动态选择使用列表序列化器还是详细序列化器。
        列表操作使用简化版序列化器，其他操作使用完整版序列化器。
        
        Returns:
            type: 序列化器类，RoleListSerializer 或 RoleSerializer
        
        Raises:
            无
        """
        if self.action == 'list':
            return RoleListSerializer
        return RoleSerializer
