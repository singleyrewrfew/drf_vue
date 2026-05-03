from django.utils import timezone
from django.db import transaction
from django.http import Http404
from rest_framework.exceptions import APIException, PermissionDenied, ValidationError
from apps.contents.models import Content


class ContentService:
    """
    内容业务逻辑服务层
    
    封装所有与内容相关的业务逻辑，使 ViewSet 保持简洁
    """
    
    @staticmethod
    def create_content(validated_data, author):
        """
        创建内容
        
        Args:
            validated_data: 已验证的数据字典
            author: 作者对象
            
        Returns:
            Content: 创建的内容对象
        """
        return Content.objects.create(author=author, **validated_data)
    
    @staticmethod
    @transaction.atomic
    def publish_content(content, user=None):
        """
        发布内容
        
        Args:
            content: 要发布的内容对象
            user: 操作用户（可选，用于权限检查）
            
        Returns:
            Content: 发布后的内容对象
            
        Raises:
            ValueError: 如果内容已经发布
            PermissionDenied: 如果用户无发布权限
        """
        # 权限检查（如果提供了用户）
        if user is not None:
            # is_admin 已包含 is_superuser 检查
            if not (user.is_admin or (hasattr(user, 'has_permission') and user.has_permission('content_publish'))):
                raise PermissionDenied('无发布权限')
        
        if content.status == 'published':
            exc = APIException(detail='内容已发布')
            exc.status_code = 409
            raise exc
        
        content.status = 'published'
        content.published_at = timezone.now()
        content.save(update_fields=['status', 'published_at'])
        return content
    
    @staticmethod
    @transaction.atomic
    def archive_content(content, user=None):
        """
        归档内容
        
        Args:
            content: 要归档的内容对象
            user: 操作用户（可选，用于权限检查）
            
        Returns:
            Content: 归档后的内容对象
            
        Raises:
            PermissionDenied: 如果用户无归档权限
        """
        # 权限检查（如果提供了用户）
        if user is not None:
            # is_admin 已包含 is_superuser 检查
            if not (user.is_admin or (hasattr(user, 'has_permission') and user.has_permission('content_archive'))):
                raise PermissionDenied('无归档权限')
        
        content.status = 'archived'
        content.save(update_fields=['status'])
        return content
    
    @staticmethod
    def can_user_edit(content, user):
        """
        检查用户是否可以编辑内容
        
        Args:
            content: 内容对象
            user: 用户对象
            
        Returns:
            bool: 是否可以编辑
        """
        # is_admin 已包含 is_superuser 检查
        if user.is_admin:
            return True
        return content.author == user
    
    @staticmethod
    def can_user_delete(content, user):
        """
        检查用户是否可以删除内容
        
        Args:
            content: 内容对象
            user: 用户对象
            
        Returns:
            bool: 是否可以删除
        """
        # is_admin 已包含 is_superuser 检查
        if user.is_admin:
            return True
        return content.author == user
    
    @staticmethod
    def get_content_or_error(pk):
        """
        获取内容或抛出异常
        
        Args:
            pk: 内容主键或 UUID
            
        Returns:
            Content: 内容对象
            
        Raises:
            Http404: 如果内容不存在
        """
        try:
            return Content.objects.select_related('author', 'category')\
                                  .prefetch_related('tags').get(pk=pk)
        except Content.DoesNotExist:
            raise Http404('内容不存在')
    
    @staticmethod
    def get_published_contents():
        """
        获取所有已发布的内容
        
        Returns:
            QuerySet: 已发布内容的查询集
        """
        return Content.objects.filter(status='published')
    
    @staticmethod
    def get_contents_by_author(author):
        """
        获取指定作者的内容列表
        
        Args:
            author: 作者对象
            
        Returns:
            QuerySet: 该作者的内容查询集
        """
        return Content.objects.filter(author=author)
    
    @staticmethod
    def search_contents(keyword):
        """
        搜索内容
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            QuerySet: 匹配的内容查询集
        """
        return Content.objects.filter(
            status='published',
            title__icontains=keyword
        )
