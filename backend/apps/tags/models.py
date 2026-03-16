import uuid
from django.db import models
from django.utils.text import slugify

def generate_slug(name):
    """
    生成 slug，支持中文
    
    步骤：
    1. 使用 pypinyin 将中文转换为拼音
    2. 使用 slugify 清理特殊字符
    3. 如果 slug 为空，返回空字符串
    
    参数：
        name: 标签名称（可以是中文或英文）
    
    返回：
        生成的 slug 字符串
    """
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
    """
    标签模型
    
    功能：
    - 存储标签信息
    - 自动生成 URL 友好的 slug
    - 支持中文标签名称
    """
    # 主键：使用 UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 标签名称：唯一，最大长度 30
    name = models.CharField(max_length=30, unique=True, verbose_name='标签名称')
    # URL 别名：唯一，用于 URL 路由
    slug = models.SlugField(max_length=30, unique=True, blank=True, verbose_name='URL别名')
    # 创建时间：自动记录
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
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
        """
        保存标签时自动生成 slug
        
        步骤：
        1. 如果 slug 为空，自动生成
        2. 使用 generate_slug 函数生成基础 slug
        3. 如果 slug 已存在，添加数字后缀
        4. 如果无法生成 slug，使用 UUID 前 8 位
        """
        if not self.slug:
            base_slug = generate_slug(self.name)
            if base_slug:
                slug = base_slug
                counter = 1
                # 检查 slug 是否已存在，如果存在则添加数字后缀
                while Tag.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                    slug = f'{base_slug}-{counter}'
                    counter += 1
                self.slug = slug
            else:
                # 如果无法生成 slug，使用 UUID
                self.slug = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)
