"""
清理上传临时文件的管理命令

用法：python manage.py cleanup_upload_temp
"""
from django.core.management.base import BaseCommand
from utils.upload_manager import cleanup_upload_temp_files


class Command(BaseCommand):
    help = '清理过期的上传临时文件'
    
    def handle(self, *args, **options):
        self.stdout.write('开始清理上传临时文件...')
        
        stats = cleanup_upload_temp_files()
        
        self.stdout.write(
            self.style.SUCCESS(f'清理完成！')
        )
        self.stdout.write(f'当前临时文件数：{stats["file_count"]}')
        self.stdout.write(f'当前临时目录数：{stats["directory_count"]}')
        self.stdout.write(f'当前总大小：{stats["total_size"] / 1024 / 1024:.2f} MB')
