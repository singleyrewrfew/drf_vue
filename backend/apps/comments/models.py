import uuid

from django.contrib.auth import get_user_model
from django.db import models

from apps.contents.models import Content

User = get_user_model()


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(verbose_name='评论内容')
    article = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='comments', verbose_name='关联文章')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='评论用户')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies', verbose_name='父评论')
    is_approved = models.BooleanField(default=False, verbose_name='是否审核通过')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'comments'
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username}: {self.content[:50]}'

    @property
    def is_reply(self):
        return self.parent is not None
