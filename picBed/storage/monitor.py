import os
import shutil
from datetime import datetime, timedelta
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from images.models import Image
from users.models import User
import logging

logger = logging.getLogger('picBed')


class StorageMonitor:
    def __init__(self):
        self.media_root = settings.MEDIA_ROOT
    
    def get_storage_stats(self):
        total_size = 0
        total_files = 0
        
        for root, dirs, files in os.walk(self.media_root):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    total_size += os.path.getsize(file_path)
                    total_files += 1
                except OSError:
                    continue
        
        return {
            'total_size': total_size,
            'total_size_mb': total_size / (1024 * 1024),
            'total_files': total_files,
            'media_root': self.media_root
        }
    
    def get_user_storage_stats(self, user):
        images = Image.objects.filter(user=user)
        total_size = sum(img.file_size for img in images)
        
        return {
            'user_id': user.id,
            'username': user.username,
            'storage_used': total_size,
            'storage_quota': user.storage_quota,
            'storage_available': user.storage_quota - total_size,
            'usage_percentage': (total_size / user.storage_quota * 100) if user.storage_quota > 0 else 0,
            'image_count': images.count()
        }
    
    def cleanup_orphaned_files(self, dry_run=True):
        db_files = set()
        for image in Image.objects.all():
            if image.file:
                db_files.add(image.file.path)
        
        orphaned_files = []
        for root, dirs, files in os.walk(self.media_root):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path not in db_files:
                    orphaned_files.append(file_path)
        
        if not dry_run:
            for file_path in orphaned_files:
                try:
                    os.remove(file_path)
                    logger.info(f'Deleted orphaned file: {file_path}')
                except OSError as e:
                    logger.error(f'Failed to delete orphaned file {file_path}: {str(e)}')
        
        return {
            'orphaned_files_count': len(orphaned_files),
            'orphaned_files': orphaned_files,
            'dry_run': dry_run
        }
    
    def cleanup_old_images(self, days=365, dry_run=True):
        cutoff_date = timezone.now() - timedelta(days=days)
        old_images = Image.objects.filter(created_at__lt=cutoff_date)
        
        deleted_count = 0
        deleted_size = 0
        
        if not dry_run:
            for image in old_images:
                deleted_size += image.file_size
                if image.file:
                    image.file.delete(save=False)
                image.delete()
                deleted_count += 1
                logger.info(f'Deleted old image: {image.filename} (ID: {image.id})')
        
        return {
            'old_images_count': old_images.count() if dry_run else deleted_count,
            'deleted_size': deleted_size,
            'cutoff_date': cutoff_date,
            'dry_run': dry_run
        }
    
    def cleanup_unused_images(self, days=90, dry_run=True):
        cutoff_date = timezone.now() - timedelta(days=days)
        unused_images = Image.objects.filter(
            access_count=0,
            created_at__lt=cutoff_date
        )
        
        deleted_count = 0
        deleted_size = 0
        
        if not dry_run:
            for image in unused_images:
                deleted_size += image.file_size
                if image.file:
                    image.file.delete(save=False)
                image.delete()
                deleted_count += 1
                logger.info(f'Deleted unused image: {image.filename} (ID: {image.id})')
        
        return {
            'unused_images_count': unused_images.count() if dry_run else deleted_count,
            'deleted_size': deleted_size,
            'cutoff_date': cutoff_date,
            'dry_run': dry_run
        }
    
    def update_user_storage_usage(self):
        users = User.objects.all()
        updated_count = 0
        
        for user in users:
            actual_usage = Image.objects.filter(user=user).aggregate(
                total=models.Sum('file_size')
            )['total'] or 0
            
            if user.storage_used != actual_usage:
                user.storage_used = actual_usage
                user.save(update_fields=['storage_used'])
                updated_count += 1
                logger.info(f'Updated storage usage for user {user.username}: {actual_usage} bytes')
        
        return {
            'updated_users_count': updated_count,
            'total_users': users.count()
        }


from django.db import models
