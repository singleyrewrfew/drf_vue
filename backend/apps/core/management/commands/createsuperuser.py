import sys
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

User = get_user_model()


class Command(BaseCommand):
    help = '创建超级用户，支持角色选择'

    def add_arguments(self, parser):
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
        username = options.get('username')
        email = options.get('email', '')
        password = options.get('password')
        role = options.get('role')
        noinput = options.get('noinput')

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

        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    is_superuser=True,
                    is_staff=True,
                )

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
