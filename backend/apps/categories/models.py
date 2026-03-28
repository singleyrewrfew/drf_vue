import uuid

from django.db import models
from utils.slug_utils import generate_unique_slug


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, verbose_name='分类名称')
    slug = models.SlugField(max_length=50, unique=True, blank=True, verbose_name='URL别名')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children', verbose_name='父分类')
    description = models.TextField(blank=True, verbose_name='描述')
    sort_order = models.IntegerField(default=0, verbose_name='排序')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

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
