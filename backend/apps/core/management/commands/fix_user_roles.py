from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.roles.models import Role

User = get_user_model()


class Command(BaseCommand):
    """
    Django 管理命令：修复用户角色分配
    
    该命令用于确保所有用户都有有效的角色分配。主要功能包括：
    1. 创建或获取默认的普通用户角色
    2. 为没有角色的用户分配默认角色
    3. 显示所有用户的当前角色信息
    
    使用场景：
    - 数据库迁移后角色数据丢失
    - 手动清理了角色数据需要恢复
    - 检查用户角色分配的完整性
    
    使用方法：
        python manage.py fix_user_roles
    """
    help = '修复用户角色'

    def handle(self, *args, **options):
        """
        执行用户角色修复命令
        
        处理流程：
        1. 获取或创建默认的普通用户角色（code='user'）
        2. 查找所有未分配角色的用户
        3. 为这些用户批量分配默认角色
        4. 输出所有用户的角色分配情况
        
        Args:
            *args: 位置参数（未使用）
            **options: 关键字参数（未使用）
        
        Returns:
            None
        
        Raises:
            无显式异常抛出，数据库错误由 Django ORM 处理
        """
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
            self.stdout.write(self.style.SUCCESS(f'创建默认角色: {default_role.name}'))
        
        # 查找并修复未分配角色的用户
        users_without_role = User.objects.filter(role__isnull=True)
        count = users_without_role.count()
        
        if count > 0:
            for user in users_without_role:
                user.role = default_role
                user.save()
                self.stdout.write(self.style.SUCCESS(f'为用户 {user.username} 分配角色: {default_role.name}'))
            
            self.stdout.write(self.style.SUCCESS(f'成功修复 {count} 个用户的角色'))
        else:
            self.stdout.write(self.style.SUCCESS('所有用户都已分配角色'))
        
        # 显示所有用户的角色分配情况
        self.stdout.write('\n用户角色列表:')
        for user in User.objects.all():
            role_name = user.role.name if user.role else '未分配'
            role_code = user.role.code if user.role else 'N/A'
            self.stdout.write(f'  {user.username}: {role_name} ({role_code})')
