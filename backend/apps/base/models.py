"""
基础模型类

提供通用的基础字段和方法，所有模型应继承此类以获得：
- UUID 主键
- created_at/updated_at 自动时间戳
- 软删除支持（可选）
"""

import uuid
from django.db import models


class BaseModel(models.Model):
    """
    基础模型类，提供通用字段和方法

    所有模型应继承此类以获得：
    - UUID 主键
    - created_at/updated_at 自动时间戳
    - 刷新实例方法
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        abstract = True  # 不会创建数据库表

    @property
    def model_name(self):
        """返回模型名称"""
        return self.__class__.__name__


class SoftDeleteModel(BaseModel):
    """
    支持软删除的基础模型

    继承 BaseModel，额外提供：
    - is_deleted 标记
    - deleted_at 时间戳
    - delete() 软删除方法
    - hard_delete() 真删除方法
    """
    is_deleted = models.BooleanField(default=False, verbose_name='是否删除')
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name='删除时间')

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """软删除"""
        from django.utils import timezone
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=['is_deleted', 'deleted_at'])

    def hard_delete(self, using=None, keep_parents=False):
        """真删除（调用父类方法）"""
        super().delete(using=using, keep_parents=keep_parents)
