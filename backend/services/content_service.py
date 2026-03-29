from django.utils import timezone
from django.db import transaction
from apps.contents.models import Content


class ContentService:
    """
    内容业务逻辑服务层
    
    封装所有与内容相关的业务逻辑，使 ViewSet 保持简洁
    """
    
    def create_content(self, validated_data, author):
        """
        创建内容
        
        Args:
            validated_data: 已验证的数据字典
            author: 作者对象
            
        Returns:
            Content: 创建的内容对象
        """
        return Content.objects.create(author=author, **validated_data)
    
    @transaction.atomic
    def publish_content(self, content):
        """
        发布内容
        
        Args:
            content: 要发布的内容对象
            
        Returns:
            Content: 发布后的内容对象
            
        Raises:
            ValueError: 如果内容已经发布
        """
        if content.status == 'published':
            raise ValueError('内容已发布')
        
        content.status = 'published'
        content.published_at = timezone.now()
        content.save(update_fields=['status', 'published_at'])
        return content
    
    @transaction.atomic
    def archive_content(self, content):
        """
        归档内容
        
        Args:
            content: 要归档的内容对象
            
        Returns:
            Content: 归档后的内容对象
        """
        content.status = 'archived'
        content.save(update_fields=['status'])
        return content
    
    def get_content_or_error(self, pk):
        """
        获取内容或抛出异常
        
        Args:
            pk: 内容主键或 UUID
            
        Returns:
            Content: 内容对象
            
        Raises:
            Http404: 如果内容不存在
        """
        from django.http import Http404
        
        try:
            return Content.objects.select_related('author', 'category')\
                                  .prefetch_related('tags').get(pk=pk)
        except Content.DoesNotExist:
            raise Http404('内容不存在')
