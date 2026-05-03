from django.db.models import Count, Prefetch, Q
from django.core.cache import cache
import logging

from apps.comments.models import Comment, CommentLike
from services.base import ModelService
from utils.error_codes import ErrorTypes
from rest_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)


class CommentService(ModelService):
    """
    评论业务逻辑服务层
    
    封装所有与评论相关的业务逻辑
    """
    model_class = Comment

    @classmethod
    def get_approved_comments(cls):
        """
        获取已审核的评论列表
        
        Returns:
            QuerySet: 已审核评论的查询集
        """
        return Comment.objects.filter(is_approved=True)

    @classmethod
    def get_root_comments(cls):
        """
        获取根评论（非回复）
        
        Returns:
            QuerySet: 根评论的查询集
        """
        return Comment.objects.filter(is_approved=True, parent__isnull=True)

    @classmethod
    def get_comments_by_article(cls, article):
        """
        获取文章的评论列表
        
        Args:
            article: 文章对象
            
        Returns:
            QuerySet: 该文章的评论查询集
        """
        return Comment.objects.filter(
            article=article,
            is_approved=True,
            parent__isnull=True
        ).annotate(
            reply_count=Count('replies', filter=Q(replies__is_approved=True))
        ).prefetch_related(
            Prefetch('replies', queryset=Comment.objects.filter(is_approved=True))
        )

    @classmethod
    def get_comments_by_user(cls, user):
        """
        获取用户的评论列表
        
        Args:
            user: 用户对象
            
        Returns:
            QuerySet: 该用户的评论查询集
        """
        return Comment.objects.filter(user=user)

    @classmethod
    def create_comment(cls, user, article, content, parent=None, reply_to=None):
        """
        创建评论
        
        Args:
            user: 用户对象
            article: 文章对象
            content: 评论内容
            parent: 父评论（可选）
            reply_to: 回复对象（可选）
            
        Returns:
            Comment: 创建的评论对象
        """
        return Comment.objects.create(
            user=user,
            article=article,
            content=content,
            parent=parent,
            reply_to=reply_to
        )

    @classmethod
    def approve_comment(cls, comment):
        """
        审核通过评论
        
        Args:
            comment: 评论对象
            
        Returns:
            Comment: 更新后的评论对象
        """
        comment.is_approved = True
        comment.save(update_fields=['is_approved'])
        return comment

    @classmethod
    def toggle_like(cls, comment, user):
        """
        切换评论点赞状态
        
        Args:
            comment: 评论对象
            user: 用户对象
            
        Returns:
            tuple: (评论对象, 是否点赞)
        """
        like, created = CommentLike.objects.get_or_create(
            comment=comment,
            user=user
        )
        
        if created:
            comment.like_count += 1
            comment.save(update_fields=['like_count'])
            return comment, True
        else:
            like.delete()
            comment.like_count -= 1
            comment.save(update_fields=['like_count'])
            return comment, False

    @classmethod
    def get_user_liked_comment_ids(cls, user):
        """
        获取用户点赞的评论 ID 列表
        
        Args:
            user: 用户对象
            
        Returns:
            set: 点赞的评论 ID 集合
        """
        return set(
            CommentLike.objects.filter(user=user).values_list('comment_id', flat=True)
        )

    @classmethod
    def can_user_modify(cls, comment, user):
        """
        检查用户是否可以修改评论
        
        Args:
            comment: 评论对象
            user: 用户对象
            
        Returns:
            bool: 是否可以修改
        """
        # is_admin 已包含 is_superuser 检查
        if user.is_admin:
            return True
        return comment.user_id == user.id

    @classmethod
    def get_comment_statistics(cls, article=None):
        """
        获取评论统计信息
        
        Args:
            article: 文章对象（可选，用于筛选文章的评论）
            
        Returns:
            dict: 统计信息
        """
        queryset = Comment.objects.all()
        if article:
            queryset = queryset.filter(article=article)

        return {
            'total_count': queryset.count(),
            'approved_count': queryset.filter(is_approved=True).count(),
            'pending_count': queryset.filter(is_approved=False).count(),
            'root_count': queryset.filter(parent__isnull=True).count(),
            'reply_count': queryset.filter(parent__isnull=False).count(),
        }

    @classmethod
    def check_comment_rate_limit(cls, user, article_id=None):
        """
        检查用户评论频率限制
        
        防刷策略：
        - 每用户每分钟最多 10 条评论（全局）
        - 每用户对同一篇文章每分钟最多 5 条评论
        
        Args:
            user: 用户对象
            article_id: 文章 ID（可选，用于更严格的限制）
            
        Raises:
            ValidationError: 如果超出频率限制
        """
        # 全局频率限制：每分钟 10 条
        global_rate_key = f'comment_rate_global_{user.id}'
        global_count = cache.get(global_rate_key, 0)
        
        if global_count >= 10:
            logger.warning(f'用户 {user.username} (ID:{user.id}) 评论频率超限（全局）')
            raise ValidationError({
                'content': ['评论过于频繁，请稍后再试（每分钟最多 10 条）']
            })
        
        # 文章级别频率限制：每分钟 5 条（针对同一篇文章）
        if article_id:
            article_rate_key = f'comment_rate_article_{user.id}_{article_id}'
            article_count = cache.get(article_rate_key, 0)
            
            if article_count >= 5:
                logger.warning(f'用户 {user.username} (ID:{user.id}) 对文章 {article_id} 评论频率超限')
                raise ValidationError({
                    'content': ['对该文章评论过于频繁，请稍后再试（每分钟最多 5 条）']
                })
            
            # 增加文章级别计数
            cache.set(article_rate_key, article_count + 1, timeout=60)
        
        # 增加全局计数
        cache.set(global_rate_key, global_count + 1, timeout=60)
        
        logger.info(f'用户 {user.username} (ID:{user.id}) 评论频率检查通过')

    @classmethod
    def check_like_rate_limit(cls, user):
        """
        检查用户点赞频率限制
        
        防刷策略：
        - 每用户每分钟最多 20 次点赞操作
        
        Args:
            user: 用户对象
            
        Raises:
            ValidationError: 如果超出频率限制
        """
        rate_key = f'like_rate_{user.id}'
        like_count = cache.get(rate_key, 0)
        
        if like_count >= 20:
            logger.warning(f'用户 {user.username} (ID:{user.id}) 点赞频率超限')
            raise ValidationError({
                'detail': '点赞操作过于频繁，请稍后再试（每分钟最多 20 次）'
            })
        
        # 增加计数
        cache.set(rate_key, like_count + 1, timeout=60)
        logger.debug(f'用户 {user.username} (ID:{user.id}) 点赞频率检查通过')
