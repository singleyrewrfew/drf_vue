from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='邮箱')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='头像')
    bio = models.TextField(max_length=500, blank=True, verbose_name='个人简介')
    
    storage_quota = models.BigIntegerField(default=1073741824, verbose_name='存储配额 (字节)')
    storage_used = models.BigIntegerField(default=0, verbose_name='已用存储 (字节)')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        verbose_name='用户组',
        help_text='The groups this user belongs to.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        verbose_name='权限',
        help_text='Specific permissions for this user.',
    )
    
    def __str__(self):
        return self.username
    
    @property
    def storage_available(self):
        return self.storage_quota - self.storage_used
    
    @property
    def storage_usage_percentage(self):
        if self.storage_quota == 0:
            return 0
        return (self.storage_used / self.storage_quota) * 100
