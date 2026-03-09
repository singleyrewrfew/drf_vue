from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'article', 'user', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['content', 'user__username', 'article__title']
    raw_id_fields = ['article', 'user', 'parent']
    actions = ['approve_comments']

    @admin.action(description='审核通过选中评论')
    def approve_comments(self, request, queryset):
        count = queryset.update(is_approved=True)
        self.message_user(request, f'已审核通过 {count} 条评论')
