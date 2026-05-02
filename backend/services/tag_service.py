from django.db.models import Count, Q

from apps.tags.models import Tag
from services.base import ModelService


class TagService(ModelService):
    """
    标签业务逻辑服务层
    
    封装所有与标签相关的业务逻辑
    """
    model_class = Tag

    @classmethod
    def get_tags_with_content_count(cls):
        """
        获取标签列表（包含已发布内容数量）
        
        Returns:
            QuerySet: 带内容计数的标签查询集
        """
        return Tag.objects.annotate(
            content_count=Count('contents', filter=Q(contents__status='published'))
        )

    @classmethod
    def get_popular_tags(cls, limit=10):
        """
        获取热门标签
        
        Args:
            limit: 返回数量限制
            
        Returns:
            QuerySet: 热门标签查询集
        """
        return Tag.objects.annotate(
            content_count=Count('contents', filter=Q(contents__status='published'))
        ).filter(content_count__gt=0).order_by('-content_count')[:limit]

    @classmethod
    def get_or_create_by_name(cls, name):
        """
        根据名称获取或创建标签
        
        Args:
            name: 标签名称
            
        Returns:
            tuple: (标签对象, 是否创建)
        """
        return Tag.objects.get_or_create(name=name)

    @classmethod
    def create_tag(cls, name):
        """
        创建标签
        
        Args:
            name: 标签名称
            
        Returns:
            Tag: 创建的标签对象
        """
        return Tag.objects.create(name=name)

    @classmethod
    def search_tags(cls, keyword):
        """
        搜索标签
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            QuerySet: 匹配的标签查询集
        """
        return Tag.objects.filter(name__icontains=keyword)

    @classmethod
    def can_user_modify(cls, user):
        """
        检查用户是否可以修改标签
        
        Args:
            user: 用户对象
            
        Returns:
            bool: 是否可以修改
        """
        return user.is_admin or user.is_superuser or (user.role and user.role.code == 'editor')

    @classmethod
    def get_tag_statistics(cls):
        """
        获取标签统计信息
        
        Returns:
            dict: 统计信息
        """
        total_count = Tag.objects.count()
        used_count = Tag.objects.annotate(
            content_count=Count('contents')
        ).filter(content_count__gt=0).count()
        
        return {
            'total_count': total_count,
            'used_count': used_count,
            'unused_count': total_count - used_count,
        }
