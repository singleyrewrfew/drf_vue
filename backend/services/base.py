"""
Base Service Classes

提供服务层的基础类和工具
"""
from abc import ABC
from typing import Any, List, Optional
from django.db import models


class BaseService(ABC):
    """
    服务基类
    
    所有业务服务类都应该继承此类
    
    Note: 权限验证和条件验证应直接在具体 Service 方法中实现，
          无需使用此基类的静态方法。
    """
    pass


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
