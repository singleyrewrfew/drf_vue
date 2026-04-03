from django.db import models

from apps.base.models import BaseModel
from utils.slug_utils import generate_unique_slug


class Category(BaseModel):
    """
    分类模型
    
    继承 BaseModel，提供：
    - UUID 主键
    - created_at 自动时间戳
    """
    # 注意：id, created_at 由 BaseModel 提供
    name = models.CharField(max_length=50, verbose_name='分类名称')
    slug = models.SlugField(max_length=50, unique=True, blank=True, verbose_name='URL别名')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children', verbose_name='父分类')
    description = models.TextField(blank=True, verbose_name='描述')
    sort_order = models.IntegerField(default=0, verbose_name='排序')
    # 注意：created_at 由 BaseModel 提供

    class Meta:
        db_table = 'categories'
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['sort_order', '-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Category, self.name, self)
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        if self.parent:
            return f'{self.parent.full_name} > {self.name}'
        return self.name
