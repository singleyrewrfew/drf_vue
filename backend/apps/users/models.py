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
        return self.role and self.role.code == 'admin'

    @property
    def is_editor(self):
        return self.role and self.role.code in ['admin', 'editor']

    def has_permission(self, permission_code):
        if not self.role:
            return False
        return self.role.permissions.filter(code=permission_code).exists()
