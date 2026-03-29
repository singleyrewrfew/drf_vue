"""
Content Service

内容管理业务逻辑服务
"""
import logging
from django.utils import timezone
from django.db import DatabaseError, IntegrityError, transaction
from rest_framework.exceptions import PermissionDenied, ValidationError

from apps.contents.models import Content
from services.base import ModelService

logger = logging.getLogger(__name__)


class ContentService(ModelService):
    """
    内容服务类
    
    处理内容相关的业务逻辑
    """
    
    model_class = Content
    
    @staticmethod
    def publish_content(content: Content, user) -> Content:
        """
        发布内容
        
        Args:
            content: 内容实例
            user: 用户实例
        
        Returns:
            发布后的内容实例
        
        Raises:
            PermissionDenied: 无发布权限
            ValidationError: 内容已发布
        """
        if not user.has_permission('content_publish') and not user.is_editor:
            raise PermissionDenied('无发布权限')
        
        if content.status == 'published':
            raise ValidationError('内容已发布')
        
        try:
            content.status = 'published'
            content.published_at = timezone.now()
            content.save()
            logger.info(f"Content {content.id} published by user {user.id}")
            return content
        except (DatabaseError, IntegrityError) as e:
            logger.error(f"Failed to publish content {content.id}: {type(e).__name__}: {e}", exc_info=True)
            raise ValidationError('发布失败，请稍后重试')
    
    @staticmethod
    def archive_content(content: Content, user) -> Content:
        """
        归档内容
        
        Args:
            content: 内容实例
            user: 用户实例
        
        Returns:
            归档后的内容实例
        
        Raises:
            PermissionDenied: 无归档权限
        """
        if not user.has_permission('content_archive') and not user.is_editor:
            raise PermissionDenied('无归档权限')
        
        try:
            content.status = 'archived'
            content.save()
            logger.info(f"Content {content.id} archived by user {user.id}")
            return content
        except (DatabaseError, IntegrityError) as e:
            logger.error(f"Failed to archive content {content.id}: {type(e).__name__}: {e}", exc_info=True)
            raise ValidationError('归档失败，请稍后重试')
    
    @staticmethod
    def increment_view_count(content: Content) -> Content:
        """
        增加浏览量
        
        Args:
            content: 内容实例
        
        Returns:
            更新后的内容实例
        """
        content.view_count += 1
        content.save(update_fields=['view_count'])
        return content
    
    @staticmethod
    def can_user_edit(content: Content, user) -> bool:
        """
        检查用户是否可以编辑内容
        
        Args:
            content: 内容实例
            user: 用户实例
        
        Returns:
            是否可以编辑
        """
        if user.is_superuser or user.is_admin:
            return True
        
        if content.author == user:
            return True
        
        return False
    
    @staticmethod
    def can_user_delete(content: Content, user) -> bool:
        """
        检查用户是否可以删除内容
        
        Args:
            content: 内容实例
            user: 用户实例
        
        Returns:
            是否可以删除
        """
        if user.is_superuser or user.is_admin:
            return True
        
        if content.author == user:
            return True
        
        return False
    
    @classmethod
    def get_published_contents(cls, limit: int = None):
        """
        获取已发布的内容列表
        
        Args:
            limit: 限制数量
        
        Returns:
            内容查询集
        """
        queryset = cls.model_class.objects.filter(status='published')
        
        if limit:
            queryset = queryset[:limit]
        
        return queryset
    
    @classmethod
    def get_contents_by_author(cls, author, status: str = None):
        """
        获取作者的内容列表
        
        Args:
            author: 作者实例
            status: 内容状态过滤
        
        Returns:
            内容查询集
        """
        queryset = cls.model_class.objects.filter(author=author)
        
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset
    
    @classmethod
    def get_contents_by_category(cls, category, status: str = 'published'):
        """
        获取分类下的内容列表
        
        Args:
            category: 分类实例或ID
            status: 内容状态过滤
        
        Returns:
            内容查询集
        """
        queryset = cls.model_class.objects.filter(category=category)
        
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset
    
    @classmethod
    def get_contents_by_tag(cls, tag, status: str = 'published'):
        """
        获取标签下的内容列表
        
        Args:
            tag: 标签实例或ID
            status: 内容状态过滤
        
        Returns:
            内容查询集
        """
        queryset = cls.model_class.objects.filter(tags=tag)
        
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset
    
    @classmethod
    def search_contents(cls, keyword: str, status: str = 'published'):
        """
        搜索内容
        
        Args:
            keyword: 搜索关键词
            status: 内容状态过滤
        
        Returns:
            内容查询集
        """
        queryset = cls.model_class.objects.filter(
            title__icontains=keyword
        )
        
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset
    
    @classmethod
    def get_hot_contents(cls, limit: int = 10):
        """
        获取热门内容
        
        Args:
            limit: 限制数量
        
        Returns:
            内容查询集
        """
        return cls.model_class.objects.filter(
            status='published'
        ).order_by('-view_count')[:limit]
    
    @classmethod
    def get_recent_contents(cls, limit: int = 10):
        """
        获取最新内容
        
        Args:
            limit: 限制数量
        
        Returns:
            内容查询集
        """
        return cls.model_class.objects.filter(
            status='published'
        ).order_by('-created_at')[:limit]
