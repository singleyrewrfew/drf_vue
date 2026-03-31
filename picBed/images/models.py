from django.db import models
from django.conf import settings
from core.models import UserOwnedModel


class Album(UserOwnedModel):
    name = models.CharField(max_length=100, verbose_name='相册名称')
    description = models.TextField(blank=True, verbose_name='相册描述')
    cover = models.ImageField(upload_to='album_covers/', null=True, blank=True, verbose_name='封面图片')
    is_public = models.BooleanField(default=False, verbose_name='是否公开')
    
    class Meta:
        db_table = 'albums'
        verbose_name = '相册'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username} - {self.name}'
    
    @property
    def image_count(self):
        return self.images.count()


def image_upload_path(instance, filename):
    import os
    from datetime import datetime
    import hashlib
    
    ext = filename.split('.')[-1].lower()
    date_path = datetime.now().strftime('%Y/%m/%d')
    
    hash_input = f'{instance.user.id}{datetime.now().timestamp()}{filename}'.encode()
    file_hash = hashlib.md5(hash_input).hexdigest()
    
    return f'images/{date_path}/{file_hash}.{ext}'


class Image(UserOwnedModel):
    album = models.ForeignKey(
        Album,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='images',
        verbose_name='所属相册'
    )
    
    file = models.ImageField(upload_to=image_upload_path, verbose_name='图片文件')
    filename = models.CharField(max_length=255, verbose_name='原始文件名')
    file_size = models.BigIntegerField(verbose_name='文件大小(字节)')
    file_hash = models.CharField(max_length=64, unique=True, verbose_name='文件哈希')
    
    width = models.IntegerField(verbose_name='图片宽度')
    height = models.IntegerField(verbose_name='图片高度')
    format = models.CharField(max_length=10, verbose_name='图片格式')
    
    title = models.CharField(max_length=200, blank=True, verbose_name='图片标题')
    description = models.TextField(blank=True, verbose_name='图片描述')
    tags = models.JSONField(default=list, blank=True, verbose_name='标签')
    
    is_public = models.BooleanField(default=False, verbose_name='是否公开')
    access_count = models.IntegerField(default=0, verbose_name='访问次数')
    
    storage_backend = models.CharField(max_length=50, default='local', verbose_name='存储后端')
    storage_path = models.TextField(verbose_name='存储路径')
    
    class Meta:
        db_table = 'images'
        verbose_name = '图片'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['album', '-created_at']),
            models.Index(fields=['file_hash']),
            models.Index(fields=['is_public']),
        ]
    
    def __str__(self):
        return f'{self.user.username} - {self.filename}'
    
    @property
    def url(self):
        if self.storage_backend == 'local':
            return self.file.url
        return self.storage_path
    
    def increment_access_count(self):
        self.access_count += 1
        self.save(update_fields=['access_count'])


class UploadChunk(models.Model):
    upload_id = models.CharField(max_length=64, verbose_name='上传ID')
    chunk_number = models.IntegerField(verbose_name='分块序号')
    chunk_size = models.IntegerField(verbose_name='分块大小')
    total_chunks = models.IntegerField(verbose_name='总分块数')
    total_size = models.BigIntegerField(verbose_name='文件总大小')
    filename = models.CharField(max_length=255, verbose_name='文件名')
    file_hash = models.CharField(max_length=64, verbose_name='文件哈希')
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='upload_chunks',
        verbose_name='上传用户'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'upload_chunks'
        verbose_name = '上传分块'
        verbose_name_plural = verbose_name
        unique_together = ['upload_id', 'chunk_number']
        indexes = [
            models.Index(fields=['upload_id']),
            models.Index(fields=['user', 'created_at']),
        ]
    
    def __str__(self):
        return f'{self.upload_id} - Chunk {self.chunk_number}/{self.total_chunks}'
