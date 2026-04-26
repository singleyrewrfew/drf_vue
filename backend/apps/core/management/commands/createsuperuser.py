import sys
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

User = get_user_model()


class Command(BaseCommand):
    """
    Django 管理命令：创建超级用户并分配角色
    
    扩展了 Django 默认的 createsuperuser 命令，增加了角色分配功能。
    支持命令行参数和交互式输入两种方式创建用户。
    
    主要特性：
    - 支持通过命令行参数指定用户名、邮箱、密码和角色
    - 支持交互式输入，提供角色列表供选择
    - 自动验证密码一致性
    - 使用数据库事务确保数据完整性
    - 自动设置 is_superuser 和 is_staff 为 True
    
    使用方法：
        # 交互式模式
        python manage.py createsuperuser
        
        # 非交互式模式（命令行参数）
        python manage.py createsuperuser --username=admin --email=admin@example.com --password=123456 --role=admin
        
        # 使用角色代码
        python manage.py createsuperuser --username=admin --password=123456 --role=editor
        
        # 跳过交互确认
        python manage.py createsuperuser --noinput --username=admin --password=123456 --role=1
    """
    help = '创建超级用户，支持角色选择'

    def add_arguments(self, parser):
        """
        添加命令行参数配置
        
        定义命令支持的参数选项，包括用户基本信息和角色配置。
        
        Args:
            parser: ArgumentParser 实例，用于注册命令行参数
        
        Returns:
            None
        """
        parser.add_argument(
            '--username',
            dest='username',
            default=None,
            help='用户名',
        )
        parser.add_argument(
            '--email',
            dest='email',
            default='',
            help='邮箱地址',
        )
        parser.add_argument(
            '--password',
            dest='password',
            default=None,
            help='密码',
        )
        parser.add_argument(
            '--role',
            dest='role',
            default=None,
            help='角色 ID 或角色代码',
        )
        parser.add_argument(
            '--noinput',
            action='store_true',
            dest='noinput',
            default=False,
            help='不进行交互式输入',
        )

    def handle(self, *args, **options):
        """
        执行创建超级用户命令
        
        处理流程：
        1. 解析命令行参数
        2. 如果未启用 noinput 模式且缺少必要信息，进入交互式输入
           - 收集用户名、邮箱、密码（需二次确认）
           - 显示可用角色列表并让用户选择
        3. 在数据库事务中创建用户
           - 设置 is_superuser=True 和 is_staff=True
           - 根据提供的角色 ID 或代码查找并分配角色
        4. 输出创建结果或错误信息
        
        Args:
            *args: 位置参数（未使用）
            **options: 关键字参数字典，包含以下键：
                - username (str): 用户名
                - email (str): 邮箱地址
                - password (str): 密码
                - role (str): 角色 ID 或角色代码
                - noinput (bool): 是否跳过交互式输入
        
        Returns:
            None
        
        Raises:
            CommandError: 当密码不一致、角色不存在或创建失败时抛出
        """
        username = options.get('username')
        email = options.get('email', '')
        password = options.get('password')
        role = options.get('role')
        noinput = options.get('noinput')

        # 交互式输入模式：收集用户信息和角色选择
        if not noinput:
            print('创建超级用户')
            print('=' * 30)

            if not username:
                username = input('用户名：')
            if not email:
                email = input('邮箱 (可选): ') or ''
            if not password:
                password = input('密码：')
                password_confirm = input('确认密码：')
                if password != password_confirm:
                    print(self.style.ERROR('两次密码不一致'))
                    raise CommandError('两次密码不一致')
            
            # 显示角色列表并让用户选择
            if not role:
                from apps.roles.models import Role
                roles = Role.objects.all()
                
                if not roles.exists():
                    print(self.style.ERROR('系统中没有可用的角色，请先创建角色'))
                    raise CommandError('系统中没有可用的角色')
                
                print('')
                print('可用角色列表:')
                print('-' * 50)
                print(f'{"ID":<38} {"代码":<15} {"名称":<20}')
                print('-' * 50)
                for r in roles:
                    print(f'{str(r.id):<38} {r.code:<15} {r.name:<20}')
                print('-' * 50)
                print('')
                
                role = input('请输入角色 ID 或角色代码：')
                while not role:
                    print(self.style.ERROR('角色不能为空'))
                    role = input('请输入角色 ID 或角色代码：')

        # 在事务中创建用户并分配角色
        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    is_superuser=True,
                    is_staff=True,
                )

                # 查找并分配角色（支持 ID 或代码）
                from apps.roles.models import Role
                try:
                    role_obj = Role.objects.get(id=role) if str(role).isdigit() else Role.objects.get(code=role)
                    user.role = role_obj
                    user.save()
                    print(self.style.SUCCESS(f'已分配角色：{role_obj.name}'))
                except Role.DoesNotExist:
                    print(self.style.WARNING(f'角色 "{role}" 不存在，用户未分配角色'))

                print(self.style.SUCCESS(f'超级用户 "{username}" 创建成功'))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'创建超级用户失败：{str(e)}'))
            raise CommandError(f'创建超级用户失败：{str(e)}')
