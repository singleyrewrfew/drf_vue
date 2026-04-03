from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.base.models import BaseModel


class User(AbstractUser, BaseModel):
    """
    自定义用户模型
    
    继承 Django AbstractUser 和 BaseModel，提供：
    - UUID 主键
    - 自动时间戳
    - 头像、角色等扩展字段
    """
    
    # 头像字段：允许上传图片，可以为空
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='头像')
    
    # 外键：关联到角色表，删除角色时用户角色设为 NULL
    # roles - 应用标签（app_label），对应 backend/apps/roles/ 目录
    # Role - 模型类名，在 roles/models.py 中定义
    role = models.ForeignKey('roles.Role', on_delete=models.SET_NULL, null=True, blank=True, related_name='users', verbose_name='角色')
    
    # 注意：id, created_at, updated_at 由 BaseModel 提供
    
    class Meta:
        # 数据库表名
        db_table = 'users'
        # 模型的可读名称
        verbose_name = '用户'
        # 模型的复数形式名称
        verbose_name_plural = verbose_name
        # 默认排序：按创建时间倒序
        ordering = ['-created_at']
    
    def __str__(self):
        # 返回用户的用户名作为字符串表示
        return self.username
    
    @property
    def is_admin(self):
        """
        判断用户是否为管理员
        
        权限优先级：
        1. 超级用户（is_superuser）- 拥有所有权限
        2. 角色代码为 'admin' - 管理员角色
        3. 拥有 'role_manage' 权限 - 可以管理角色
        """
        # 超级用户自动拥有所有权限
        if self.is_superuser:
            return True
        # 角色代码为 admin 的用户是管理员
        if self.role and self.role.code == 'admin':
            return True
        # 拥有角色管理权限的用户也是管理员
        if self.role and self.role.permissions.filter(code='role_manage').exists():
            return True
        # 其他情况不是管理员
        return False
    
    @property
    def is_editor(self):
        """
        判断用户是否为编辑者
        
        权限优先级：
        1. 超级用户（is_superuser）- 拥有所有权限
        2. 角色代码为 'admin' 或 'editor' - 管理员或编辑者角色
        3. 拥有内容创建和更新权限 - 可以编辑内容
        """
        # 超级用户自动拥有所有权限
        if self.is_superuser:
            return True
        # 管理员或编辑者角色
        if self.role and self.role.code in ['admin', 'editor']:
            return True
        # 拥有内容创建和更新权限
        if self.role and self.role.permissions.filter(code__in=['content_create', 'content_update']).exists():
            return True
        # 其他情况不是编辑者
        return False
    
    def has_permission(self, permission_code):
        """
        检查用户是否拥有特定权限
        
        参数：
            permission_code: 权限代码，如 'content_create', 'user_delete' 等
        
        返回：
            True: 拥有该权限
            False: 不拥有该权限
        """
        # 超级用户拥有所有权限
        if self.is_superuser:
            return True
        # 没有角色的用户没有任何权限
        if not self.role:
            return False
        # 检查角色是否包含指定权限
        return self.role.permissions.filter(code=permission_code).exists()
    
    def has_any_permission(self, permission_codes):
        """
        检查用户是否拥有任意一个权限
        
        参数：
            permission_codes: 权限代码列表，如 ['content_create', 'content_update']
        
        返回：
            True: 拥有列表中的任意一个权限
            False: 不拥有列表中的任何权限
        """
        # 超级用户拥有所有权限
        if self.is_superuser:
            return True
        # 没有角色的用户没有任何权限
        if not self.role:
            return False
        # 检查角色是否包含列表中的任意一个权限
        return self.role.permissions.filter(code__in=permission_codes).exists()
    
    def get_permission_codes(self):
        """
        获取用户拥有的所有权限代码列表
        
        返回：
            ['*']: 超级用户，返回通配符
            []: 没有角色
            ['code1', 'code2', ...]: 角色的所有权限代码列表
        """
        # 超级用户返回通配符，表示拥有所有权限
        if self.is_superuser:
            return ['*']
        # 没有角色的用户返回空列表
        if not self.role:
            return []
        # 返回角色的所有权限代码
        return list(self.role.permissions.values_list('code', flat=True))
