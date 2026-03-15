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


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, unique=True, verbose_name='标签名称')
    slug = models.SlugField(max_length=30, unique=True, blank=True, verbose_name='URL别名')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'tags'
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = generate_slug(self.name)
            if base_slug:
                slug = base_slug
                counter = 1
                while Tag.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                    slug = f'{base_slug}-{counter}'
                    counter += 1
                self.slug = slug
            else:
                # 如果无法生成 slug，使用 UUID
                self.slug = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)
