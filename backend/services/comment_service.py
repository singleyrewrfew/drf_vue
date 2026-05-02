from django.db.models import Count, Prefetch, Q

from apps.comments.models import Comment, CommentLike
from services.base import ModelService


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
        if user.is_admin or user.is_superuser:
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
