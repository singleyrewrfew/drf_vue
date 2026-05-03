from django.utils import timezone
from django.db import transaction
from django.http import Http404
from rest_framework.exceptions import APIException, PermissionDenied, ValidationError
from apps.contents.models import Content
from services.repositories import ContentRepository
from apps.core.events import content_published, content_archived


class ContentService:
    """
    内容业务逻辑服务层
    
    职责：
    - 封装业务逻辑（权限检查、状态转换、事件触发）
    - 协调多个 Repository 操作
    - 不包含直接的数据库查询
    
    注意：简单的数据访问应该直接使用 Repository 或 Model Manager
    """
    
    # Repository 实例（用于依赖注入测试）
    repo = ContentRepository
    
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
        # 委托给 Repository 层
        return ContentRepository.create(author=author, **validated_data)
    
    @staticmethod
    @transaction.atomic
    def publish_content(content, user=None):
        """
        发布内容（业务逻辑层）
        
        职责：
        1. 权限检查
        2. 状态验证
        3. 调用 Repository 更新状态
        4. 触发相关事件（如果有）
        
        Args:
            content: 要发布的内容对象
            user: 操作用户（可选，用于权限检查）
            
        Returns:
            Content: 发布后的内容对象
            
        Raises:
            ValueError: 如果内容已经发布
            PermissionDenied: 如果用户无发布权限
        """
        # 1. 权限检查（如果提供了用户）
        if user is not None:
            # is_admin 已包含 is_superuser 检查
            if not (user.is_admin or (hasattr(user, 'has_permission') and user.has_permission('content_publish'))):
                raise PermissionDenied('无发布权限')
        
        # 2. 状态验证
        if content.status == 'published':
            exc = APIException(detail='内容已发布')
            exc.status_code = 409
            raise exc
        
        # 3. 委托给 Repository 更新状态（数据访问）
        published_content = ContentRepository.publish(content)
        
        # 4. 触发领域事件（解耦模块依赖）
        content_published.send(
            sender=ContentService,
            content=published_content,
            user=user,
            published_at=published_content.published_at
        )
        
        return published_content
    
    @staticmethod
    @transaction.atomic
    def archive_content(content, user=None):
        """
        归档内容（业务逻辑层）
        
        职责：
        1. 权限检查
        2. 调用 Repository 更新状态
        
        Args:
            content: 要归档的内容对象
            user: 操作用户（可选，用于权限检查）
            
        Returns:
            Content: 归档后的内容对象
            
        Raises:
            PermissionDenied: 如果用户无归档权限
        """
        # 1. 权限检查（如果提供了用户）
        if user is not None:
            # is_admin 已包含 is_superuser 检查
            if not (user.is_admin or (hasattr(user, 'has_permission') and user.has_permission('content_archive'))):
                raise PermissionDenied('无归档权限')
        
        # 2. 委托给 Repository 更新状态（数据访问）
        archived_content = ContentRepository.archive(content)
        
        # 3. 触发领域事件（解耦模块依赖）
        content_archived.send(
            sender=ContentService,
            content=archived_content,
            user=user
        )
        
        return archived_content
    
    # 以下方法为纯数据访问，建议直接使用 Repository 或 Model Manager
    # 保留这些方法是为了向后兼容，但应该标记为 deprecated
    
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
        
        ⚠️  建议使用: ContentRepository.get_by_id(pk)
        
        Args:
            pk: 内容主键或 UUID
            
        Returns:
            Content: 内容对象
            
        Raises:
            Http404: 如果内容不存在
        """
        content = ContentRepository.get_by_id(pk)
        if content is None:
            raise Http404('内容不存在')
        return content
    
    @staticmethod
    def get_published_contents():
        """
        获取所有已发布的内容
        
        ⚠️  建议使用: ContentRepository.get_published()
        
        Returns:
            QuerySet: 已发布内容的查询集
        """
        return ContentRepository.get_published()
    
    @staticmethod
    def get_contents_by_author(author):
        """
        获取指定作者的内容列表
        
        ⚠️  建议使用: ContentRepository.get_by_author(author)
        
        Args:
            author: 作者对象
            
        Returns:
            QuerySet: 该作者的内容查询集
        """
        return ContentRepository.get_by_author(author)
    
    @staticmethod
    def search_contents(keyword):
        """
        搜索内容
        
        ⚠️  建议使用: ContentRepository.search(keyword)
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            QuerySet: 匹配的内容查询集
        """
        return ContentRepository.search(keyword)
