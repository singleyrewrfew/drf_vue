from django.core.management.base import BaseCommand
from storage.monitor import StorageMonitor


class Command(BaseCommand):
    help = '清理存储空间'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--orphaned',
            action='store_true',
            help='清理孤立文件',
        )
        parser.add_argument(
            '--old',
            type=int,
            default=365,
            help='清理超过指定天数的旧图片',
        )
        parser.add_argument(
            '--unused',
            type=int,
            default=90,
            help='清理超过指定天数且未被访问的图片',
        )
        parser.add_argument(
            '--update-usage',
            action='store_true',
            help='更新用户存储使用量',
        )
        parser.add_argument(
            '--stats',
            action='store_true',
            help='显示存储统计信息',
        )
        parser.add_argument(
            '--no-dry-run',
            action='store_true',
            help='实际执行删除操作(默认为dry-run模式)',
        )
    
    def handle(self, *args, **options):
        monitor = StorageMonitor()
        dry_run = not options['no_dry_run']
        
        if options['stats']:
            stats = monitor.get_storage_stats()
            self.stdout.write('存储统计信息:')
            self.stdout.write(f"  总大小: {stats['total_size_mb']:.2f} MB")
            self.stdout.write(f"  文件数量: {stats['total_files']}")
            self.stdout.write(f"  存储路径: {stats['media_root']}")
        
        if options['orphaned']:
            result = monitor.cleanup_orphaned_files(dry_run=dry_run)
            self.stdout.write(f"\n孤立文件清理:")
            self.stdout.write(f"  发现孤立文件: {result['orphaned_files_count']} 个")
            if dry_run:
                self.stdout.write(self.style.WARNING('  (dry-run模式,未实际删除)'))
        
        if options['old']:
            result = monitor.cleanup_old_images(days=options['old'], dry_run=dry_run)
            self.stdout.write(f"\n旧图片清理(>{options['old']}天):")
            self.stdout.write(f"  发现旧图片: {result['old_images_count']} 张")
            if dry_run:
                self.stdout.write(self.style.WARNING('  (dry-run模式,未实际删除)'))
        
        if options['unused']:
            result = monitor.cleanup_unused_images(days=options['unused'], dry_run=dry_run)
            self.stdout.write(f"\n未使用图片清理(>{options['unused']}天未访问):")
            self.stdout.write(f"  发现未使用图片: {result['unused_images_count']} 张")
            if dry_run:
                self.stdout.write(self.style.WARNING('  (dry-run模式,未实际删除)'))
        
        if options['update_usage']:
            result = monitor.update_user_storage_usage()
            self.stdout.write(f"\n用户存储使用量更新:")
            self.stdout.write(f"  更新用户数: {result['updated_users_count']}/{result['total_users']}")
