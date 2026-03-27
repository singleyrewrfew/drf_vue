"""
- ✅ 创建默认的"普通用户"角色
- ✅ 为没有角色的用户分配默认角色
- ✅ 显示修复结果
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth import get_user_model
from apps.roles.models import Role

User = get_user_model()

# 获取或创建默认用户角色
default_role, created = Role.objects.get_or_create(
    code='user',
    defaults={
        'name': '普通用户',
        'description': '普通用户，只能查看和评论',
        'is_system': True,
    }
)

if created:
    print(f'创建默认角色: {default_role.name}')

# 查找没有角色的用户
users_without_role = User.objects.filter(role__isnull=True)
count = users_without_role.count()

if count > 0:
    for user in users_without_role:
        user.role = default_role
        user.save()
        print(f'为用户 {user.username} 分配角色: {default_role.name}')
    
    print(f'成功修复 {count} 个用户的角色')
else:
    print('所有用户都已分配角色')

# 显示所有用户的角色信息
print('\n用户角色列表:')
for user in User.objects.all():
    role_name = user.role.name if user.role else '未分配'
    role_code = user.role.code if user.role else 'N/A'
    print(f'  {user.username}: {role_name} ({role_code})')
