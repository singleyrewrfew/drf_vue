"""
Base Service Classes

提供服务层的基础类和工具
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from django.db import models
from rest_framework.exceptions import PermissionDenied, ValidationError


class BaseService(ABC):
    """
    服务基类
    
    所有业务服务类都应该继承此类
    """
    
    @staticmethod
    def validate_permission(user, permission_code: str, message: str = None):
        """
        验证用户权限
        
        Args:
            user: 用户实例
            permission_code: 权限代码
            message: 错误消息
        
        Raises:
            PermissionDenied: 权限不足时抛出
        """
        if not user.has_permission(permission_code):
            raise PermissionDenied(message or f'需要 {permission_code} 权限')
    
    @staticmethod
    def validate_condition(condition: bool, message: str):
        """
        验证条件
        
        Args:
            condition: 条件
            message: 错误消息
        
        Raises:
            ValidationError: 条件不满足时抛出
        """
        if not condition:
            raise ValidationError(message)


class ModelService(BaseService):
    """
    模型服务基类
    
    为特定模型提供通用的CRUD操作
    """
    
    model_class = None
    
    @classmethod
    def get_by_id(cls, id: Any) -> models.Model:
        """
        通过ID获取模型实例
        
        Args:
            id: 模型ID
        
        Returns:
            模型实例
        
        Raises:
            model_class.DoesNotExist: 实例不存在
        """
        return cls.model_class.objects.get(id=id)
    
    @classmethod
    def get_by_id_or_none(cls, id: Any) -> Optional[models.Model]:
        """
        通过ID获取模型实例，不存在返回None
        
        Args:
            id: 模型ID
        
        Returns:
            模型实例或None
        """
        try:
            return cls.model_class.objects.get(id=id)
        except cls.model_class.DoesNotExist:
            return None
    
    @classmethod
    def create(cls, **kwargs) -> models.Model:
        """
        创建模型实例
        
        Args:
            **kwargs: 模型字段值
        
        Returns:
            创建的模型实例
        """
        return cls.model_class.objects.create(**kwargs)
    
    @classmethod
    def update(cls, instance: models.Model, **kwargs) -> models.Model:
        """
        更新模型实例
        
        Args:
            instance: 模型实例
            **kwargs: 要更新的字段
        
        Returns:
            更新后的模型实例
        """
        for attr, value in kwargs.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
    @classmethod
    def delete(cls, instance: models.Model) -> bool:
        """
        删除模型实例
        
        Args:
            instance: 模型实例
        
        Returns:
            是否删除成功
        """
        instance.delete()
        return True
    
    @classmethod
    def bulk_create(cls, instances: List[models.Model]) -> List[models.Model]:
        """
        批量创建模型实例
        
        Args:
            instances: 模型实例列表
        
        Returns:
            创建的模型实例列表
        """
        return cls.model_class.objects.bulk_create(instances)
    
    @classmethod
    def bulk_update(cls, instances: List[models.Model], fields: List[str]) -> List[models.Model]:
        """
        批量更新模型实例
        
        Args:
            instances: 模型实例列表
            fields: 要更新的字段列表
        
        Returns:
            更新的模型实例列表
        """
        return cls.model_class.objects.bulk_update(instances, fields)


class ServiceResult:
    """
    服务操作结果
    
    用于封装服务操作的返回结果
    """
    
    def __init__(self, success: bool, data: Any = None, message: str = None, errors: Dict = None):
        """
        初始化结果对象
        
        Args:
            success: 是否成功
            data: 返回数据
            message: 消息
            errors: 错误信息
        """
        self.success = success
        self.data = data
        self.message = message
        self.errors = errors or {}
    
    @classmethod
    def success_result(cls, data: Any = None, message: str = None) -> 'ServiceResult':
        """
        创建成功结果
        
        Args:
            data: 返回数据
            message: 消息
        
        Returns:
            成功结果实例
        """
        return cls(success=True, data=data, message=message)
    
    @classmethod
    def error_result(cls, message: str, errors: Dict = None) -> 'ServiceResult':
        """
        创建错误结果
        
        Args:
            message: 错误消息
            errors: 错误信息
        
        Returns:
            错误结果实例
        """
        return cls(success=False, message=message, errors=errors)
    
    def to_dict(self) -> Dict:
        """
        转换为字典
        
        Returns:
            字典表示
        """
        return {
            'success': self.success,
            'data': self.data,
            'message': self.message,
            'errors': self.errors
        }
