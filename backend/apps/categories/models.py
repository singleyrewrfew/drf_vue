import uuid

from django.db import models
from django.utils.text import slugify


def generate_slug(name):
    """生成 slug，支持中文"""
    from pypinyin import lazy_pinyin
    
    if not name:
        return ''
    
    # 先尝试将中文转换为拼音
    pinyin_list = lazy_pinyin(name)
    base_slug = '-'.join(pinyin_list).lower()
    # 使用 slugify 清理特殊字符
    base_slug = slugify(base_slug) or slugify(name)
    
    # 确保返回非空字符串
    return base_slug if base_slug else ''


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
            base_slug = generate_slug(self.name)
            if base_slug:
                slug = base_slug
                counter = 1
                while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                    slug = f'{base_slug}-{counter}'
                    counter += 1
                self.slug = slug
            else:
                # 如果无法生成 slug，使用 UUID
                self.slug = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        if self.parent:
            return f'{self.parent.full_name} > {self.name}'
        return self.name
