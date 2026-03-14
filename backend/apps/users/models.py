import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='头像')
    role = models.ForeignKey('roles.Role', on_delete=models.SET_NULL, null=True, blank=True, related_name='users', verbose_name='角色')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        if self.is_superuser:
            return True
        if self.role and self.role.code == 'admin':
            return True
        if self.role and self.role.permissions.filter(code='role_manage').exists():
            return True
        return False

    @property
    def is_editor(self):
        if self.is_superuser:
            return True
        if self.role and self.role.code in ['admin', 'editor']:
            return True
        if self.role and self.role.permissions.filter(code__in=['content_create', 'content_update']).exists():
            return True
        return False

    def has_permission(self, permission_code):
        if self.is_superuser:
            return True
        if not self.role:
            return False
        return self.role.permissions.filter(code=permission_code).exists()

    def has_any_permission(self, permission_codes):
        if self.is_superuser:
            return True
        if not self.role:
            return False
        return self.role.permissions.filter(code__in=permission_codes).exists()

    def get_permission_codes(self):
        if self.is_superuser:
            return ['*']
        if not self.role:
            return []
        return list(self.role.permissions.values_list('code', flat=True))
