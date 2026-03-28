import uuid

from django.db import models

from apps.contents.models import Content
from apps.core.models import User
from apps.base.models import BaseModel


class Comment(BaseModel):
    """
    评论模型
    
    继承 BaseModel，提供：
    - UUID 主键
    - created_at 自动时间戳
    """
    # 注意：id, created_at 由 BaseModel 提供
    content = models.TextField(verbose_name='评论内容')
    article = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='comments', verbose_name='关联文章')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='评论用户')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies', verbose_name='父评论')
    reply_to = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='replied_comments', verbose_name='回复对象')
    is_approved = models.BooleanField(default=True, verbose_name='是否审核通过')
    like_count = models.PositiveIntegerField(default=0, verbose_name='点赞数')
    # 注意：created_at 由 BaseModel 提供

    class Meta:
        db_table = 'comments'
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['article', '-created_at'], name='comment_article_created_idx'),
            models.Index(fields=['user', '-created_at'], name='comment_user_created_idx'),
            models.Index(fields=['is_approved', '-created_at'], name='comment_approved_created_idx'),
            models.Index(fields=['parent'], name='comment_parent_idx'),
        ]

    def __str__(self):
        return f'{self.user.username}: {self.content[:50]}'

    @property
    def is_reply(self):
        return self.parent is not None


class CommentLike(BaseModel):
    """
    评论点赞模型
    
    继承 BaseModel，提供：
    - UUID 主键
    - created_at 自动时间戳
    """
    # 注意：id, created_at 由 BaseModel 提供
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes', verbose_name='评论')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_likes', verbose_name='用户')
    # 注意：created_at 由 BaseModel 提供

    class Meta:
        db_table = 'comment_likes'
        verbose_name = '评论点赞'
        verbose_name_plural = verbose_name
        unique_together = ['comment', 'user']
        indexes = [
            models.Index(fields=['user'], name='comment_like_user_idx'),
        ]

    def __str__(self):
        return f'{self.user.username} liked {self.comment.id}'
