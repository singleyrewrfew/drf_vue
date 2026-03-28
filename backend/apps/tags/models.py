import uuid
from django.db import models
from utils.slug_utils import generate_unique_slug
from apps.base.models import BaseModel


class Tag(BaseModel):
    """
    标签模型
    
    功能：
    - 存储标签信息
    - 自动生成 URL 友好的 slug
    - 支持中文标签名称
    
    继承 BaseModel，提供：
    - UUID 主键
    - created_at 自动时间戳
    """
    # 注意：id, created_at 由 BaseModel 提供
    # 标签名称：唯一，最大长度 30
    name = models.CharField(max_length=30, unique=True, verbose_name='标签名称')
    # URL 别名：唯一，用于 URL 路由
    slug = models.SlugField(max_length=30, unique=True, blank=True, verbose_name='URL 别名')
    
    class Meta:
        # 数据库表名
        db_table = 'tags'
        # 模型的可读名称
        verbose_name = '标签'
        # 模型的复数形式名称
        verbose_name_plural = verbose_name
        # 默认排序：按创建时间倒序
        ordering = ['-created_at']
    
    def __str__(self):
        # 返回标签名称作为字符串表示
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Tag, self.name, self)
        super().save(*args, **kwargs)
