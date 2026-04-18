from django.db import models
from apps.base.models import BaseModel


class Permission(BaseModel):
    code = models.CharField(max_length=100, unique=True, verbose_name='权限代码')
    name = models.CharField(max_length=100, verbose_name='权限名称')
    description = models.TextField(blank=True, verbose_name='描述')

    class Meta:
        db_table = 'permissions'
        verbose_name = '权限'
        verbose_name_plural = verbose_name
        ordering = ['code']

    def __str__(self):
        return self.name


class Role(BaseModel):
    code = models.CharField(max_length=50, unique=True, verbose_name='角色代码')
    name = models.CharField(max_length=50, verbose_name='角色名称')
    description = models.TextField(blank=True, verbose_name='描述')
    permissions = models.ManyToManyField(Permission, blank=True, related_name='roles', verbose_name='权限')
    is_system = models.BooleanField(default=False, verbose_name='系统角色')

    class Meta:
        db_table = 'roles'
        verbose_name = '角色'
        verbose_name_plural = verbose_name
        ordering = ['created_at']

    def __str__(self):
        return self.name

    def has_permission(self, code):
        return self.permissions.filter(code=code).exists()
