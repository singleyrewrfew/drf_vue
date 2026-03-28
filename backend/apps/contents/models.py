import uuid

from django.db import models

from apps.categories.models import Category
from apps.core.models import User
from apps.tags.models import Tag
from apps.base.models import BaseModel


class Content(BaseModel):
    """
    内容模型
    
    继承 BaseModel，提供：
    - UUID 主键
    - created_at/updated_at 自动时间戳
    """
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('published', '已发布'),
        ('archived', '已归档'),
    ]
    
    # 注意：id, created_at, updated_at 由 BaseModel 提供
    title = models.CharField(max_length=200, verbose_name='标题')
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name='URL别名')
    summary = models.TextField(blank=True, verbose_name='摘要')
    content = models.TextField(verbose_name='正文内容')
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True, verbose_name='封面图')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contents', verbose_name='作者')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='contents', verbose_name='分类')
    tags = models.ManyToManyField(Tag, blank=True, related_name='contents', verbose_name='标签')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='状态')
    view_count = models.PositiveIntegerField(default=0, verbose_name='浏览量')
    is_top = models.BooleanField(default=False, verbose_name='是否置顶')
    published_at = models.DateTimeField(blank=True, null=True, verbose_name='发布时间')
    # 注意：created_at, updated_at 由 BaseModel 提供

    class Meta:
        db_table = 'contents'
        verbose_name = '内容'
        verbose_name_plural = verbose_name
        ordering = ['-is_top', '-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at'], name='content_status_created_idx'),
            models.Index(fields=['status', '-published_at'], name='content_status_published_idx'),
            models.Index(fields=['-is_top', '-created_at'], name='content_top_created_idx'),
            models.Index(fields=['slug'], name='content_slug_idx'),
            models.Index(fields=['author', 'status'], name='content_author_status_idx'),
        ]

    def __str__(self):
        return self.title

    def increment_view_count(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])
