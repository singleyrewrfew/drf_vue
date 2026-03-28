"""
ViewSet Mixins

提供通用的 ViewSet 混入类，减少代码重复
"""
from rest_framework import permissions


class DynamicSerializerMixin:
    """
    动态序列化器混入类
    
    根据 action 自动选择对应的序列化器
    
    使用示例:
        class MyViewSet(DynamicSerializerMixin, viewsets.ModelViewSet):
            serializer_class_mapping = {
                'list': ListSerializer,
                'create': CreateSerializer,
                'update': UpdateSerializer,
                'default': DetailSerializer
            }
    """
    serializer_class_mapping = {}
    
    def get_serializer_class(self):
        """
        根据 action 动态返回序列化器类
        
        Returns:
            type: 序列化器类
        """
        serializer_class = self.serializer_class_mapping.get(self.action)
        
        if serializer_class is None:
            serializer_class = self.serializer_class_mapping.get('default', self.serializer_class)
        
        return serializer_class


class DynamicPermissionMixin:
    """
    动态权限混入类
    
    根据 action 自动选择对应的权限类
    
    使用示例:
        class MyViewSet(DynamicPermissionMixin, viewsets.ModelViewSet):
            permission_mapping = {
                'create': [IsAuthenticated()],
                'update': [IsOwnerOrAdmin()],
                'destroy': [IsAdminUser()],
                'default': [IsAuthenticatedOrReadOnly()]
            }
    """
    permission_mapping = {}
    
    def get_permissions(self):
        """
        根据 action 动态返回权限实例列表
        
        Returns:
            list: 权限实例列表
        """
        permission_classes = self.permission_mapping.get(self.action)
        
        if permission_classes is None:
            permission_classes = self.permission_mapping.get('default', self.permission_classes)
        
        if permission_classes is None:
            return super().get_permissions()
        
        return [permission() if callable(permission) else permission 
                for permission in permission_classes]


class ActionSerializerMixin:
    """
    基于动作的序列化器混入类（简化版）
    
    针对常见的 CRUD 场景提供简化的配置方式
    
    使用示例:
        class MyViewSet(ActionSerializerMixin, viewsets.ModelViewSet):
            list_serializer_class = ListSerializer
            create_serializer_class = CreateSerializer
            detail_serializer_class = DetailSerializer
    """
    list_serializer_class = None
    create_serializer_class = None
    update_serializer_class = None
    detail_serializer_class = None
    
    def get_serializer_class(self):
        """
        根据 action 返回对应的序列化器
        
        Returns:
            type: 序列化器类
        """
        if self.action == 'list' and self.list_serializer_class:
            return self.list_serializer_class
        elif self.action == 'create' and self.create_serializer_class:
            return self.create_serializer_class
        elif self.action in ['update', 'partial_update'] and self.update_serializer_class:
            return self.update_serializer_class
        elif self.detail_serializer_class:
            return self.detail_serializer_class
        
        return super().get_serializer_class()


class ActionPermissionMixin:
    """
    基于动作的权限混入类（简化版）
    
    针对常见的权限场景提供简化的配置方式
    
    使用示例:
        class MyViewSet(ActionPermissionMixin, viewsets.ModelViewSet):
            create_permission_classes = [IsAuthenticated]
            update_permission_classes = [IsOwnerOrAdmin]
            destroy_permission_classes = [IsAdminUser]
    """
    list_permission_classes = None
    create_permission_classes = None
    update_permission_classes = None
    destroy_permission_classes = None
    retrieve_permission_classes = None
    
    def get_permissions(self):
        """
        根据 action 返回对应的权限类
        
        Returns:
            list: 权限实例列表
        """
        permission_classes = None
        
        if self.action == 'list' and self.list_permission_classes:
            permission_classes = self.list_permission_classes
        elif self.action == 'create' and self.create_permission_classes:
            permission_classes = self.create_permission_classes
        elif self.action in ['update', 'partial_update'] and self.update_permission_classes:
            permission_classes = self.update_permission_classes
        elif self.action == 'destroy' and self.destroy_permission_classes:
            permission_classes = self.destroy_permission_classes
        elif self.action == 'retrieve' and self.retrieve_permission_classes:
            permission_classes = self.retrieve_permission_classes
        
        if permission_classes is None:
            return super().get_permissions()
        
        return [permission() for permission in permission_classes]
