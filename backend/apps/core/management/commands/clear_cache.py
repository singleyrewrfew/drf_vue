"""
管理命令：清空 Redis 缓存

使用方法：
    python manage.py clear_cache
    
可选参数：
    --pattern PATTERN   只清除匹配指定模式的缓存（如 'contents:*'）
    --prefix PREFIX     只清除指定前缀的缓存（如 'cms'）
    
示例：
    # 清空所有缓存
    python manage.py clear_cache
    
    # 只清除内容相关的缓存
    python manage.py clear_cache --pattern 'contents:*'
    
    # 只清除指定前缀的缓存
    python manage.py clear_cache --prefix 'cms'
"""
from django.core.management.base import BaseCommand, CommandError
from utils.cache_utils import invalidate_pattern


class Command(BaseCommand):
    help = '清空 Redis 缓存，避免更新后出现缓存影响'

    def add_arguments(self, parser):
        parser.add_argument(
            '--pattern',
            type=str,
            default='*',
            help='缓存键模式（支持通配符 *），默认为 *（所有缓存）',
        )
        parser.add_argument(
            '--prefix',
            type=str,
            default=None,
            help='缓存键前缀，如果指定则只清除该前缀的缓存',
        )

    def handle(self, *args, **options):
        pattern = options['pattern']
        prefix = options['prefix']
        
        # 如果指定了前缀，组合成模式
        if prefix:
            pattern = f'{prefix}:*'
        
        self.stdout.write(
            self.style.WARNING(f'\n⚠️  即将清空匹配的缓存：{pattern}\n')
        )
        
        # 确认操作
        confirm = input('确认执行？(yes/no): ')
        if confirm.lower() not in ['yes', 'y']:
            self.stdout.write(self.style.NOTICE('操作已取消'))
            return
        
        try:
            # 执行清除
            count = invalidate_pattern(pattern)
            
            self.stdout.write(
                self.style.SUCCESS(f'\n✅ 成功清除 {count} 个缓存键\n')
            )
            
            # 显示统计信息
            self.stdout.write(self.style.HTTP_INFO('缓存清除完成！'))
            self.stdout.write(self.style.NOTICE(f'模式：{pattern}'))
            self.stdout.write(self.style.NOTICE(f'清除数量：{count}\n'))
            
        except Exception as e:
            raise CommandError(f'清除缓存失败：{str(e)}')
