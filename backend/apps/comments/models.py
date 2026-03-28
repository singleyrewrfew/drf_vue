import uuid

from django.db import models

from apps.contents.models import Content
from apps.core.models import User


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(verbose_name='评论内容')
    article = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='comments', verbose_name='关联文章')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='评论用户')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies', verbose_name='父评论')
    reply_to = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='replied_comments', verbose_name='回复对象')
    is_approved = models.BooleanField(default=True, verbose_name='是否审核通过')
    like_count = models.PositiveIntegerField(default=0, verbose_name='点赞数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

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


class CommentLike(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes', verbose_name='评论')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_likes', verbose_name='用户')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

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
