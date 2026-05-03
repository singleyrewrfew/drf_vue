"""
Event Handlers - 领域事件处理器

这里演示如何监听和处理领域事件

使用场景:
1. 内容发布后通知关注者
2. 内容发布后更新搜索引擎索引
3. 内容归档后清理缓存
4. 评论审核后发送通知
5. 媒体上传后触发异步处理任务

配置方法:
在 apps.py 的 ready() 方法中导入此模块即可自动注册监听器
"""
import logging
from django.dispatch import receiver
from apps.core.events import (
    content_published,
    content_archived,
    comment_approved,
)
# 注意: media_uploaded 和 media_processed 在 apps/media/receivers.py 中处理

logger = logging.getLogger(__name__)


# ==========================================
# Content Event Handlers
# ==========================================

@receiver(content_published)
def notify_followers_on_publish(sender, content, user, **kwargs):
    """
    内容发布时通知关注者
    
    实际项目中可以:
    - 发送站内通知
    - 发送邮件推送
    - 发送 WebSocket 实时消息
    """
    try:
        logger.info(f'Content published: {content.title} by {user.username}')
        
        # TODO: 实现通知逻辑
        # followers = user.followers.all()
        # for follower in followers:
        #     Notification.objects.create(
        #         user=follower,
        #         type='new_content',
        #         content=content,
        #         message=f'{user.username} 发布了新内容: {content.title}'
        #     )
        
    except Exception as e:
        # 事件处理器异常不应影响主业务流程
        logger.error(f'Failed to notify followers: {e}', exc_info=True)


@receiver(content_published)
def update_search_index(sender, content, **kwargs):
    """
    内容发布后更新搜索引擎索引
    
    实际项目中可以:
    - 更新 Elasticsearch 索引
    - 更新全文搜索索引
    - 更新推荐系统数据
    """
    try:
        logger.info(f'Updating search index for content: {content.id}')
        
        # TODO: 实现搜索索引更新
        # from apps.search.tasks import update_content_index
        # update_content_index.delay(content.id)
        
    except Exception as e:
        logger.error(f'Failed to update search index: {e}', exc_info=True)


@receiver(content_published)
def clear_cache_on_publish(sender, content, **kwargs):
    """
    内容发布后清除相关缓存
    
    实际项目中可以:
    - 清除首页缓存
    - 清除分类列表缓存
    - 清除标签列表缓存
    """
    try:
        logger.info(f'Clearing cache for content: {content.id}')
        
        # TODO: 实现缓存清理
        # from django.core.cache import cache
        # cache.delete(f'homepage_contents')
        # cache.delete(f'category_{content.category_id}_contents')
        
    except Exception as e:
        logger.error(f'Failed to clear cache: {e}', exc_info=True)


@receiver(content_archived)
def handle_content_archive(sender, content, user, **kwargs):
    """
    内容归档时的处理
    
    实际项目中可以:
    - 记录归档日志
    - 发送通知给作者
    - 清理相关缓存
    """
    try:
        logger.info(f'Content archived: {content.title} by {user.username if user else "system"}')
        
        # TODO: 实现归档逻辑
        
    except Exception as e:
        logger.error(f'Failed to handle content archive: {e}', exc_info=True)


# ==========================================
# Comment Event Handlers
# ==========================================

@receiver(comment_approved)
def notify_comment_author(sender, comment, approved_by, **kwargs):
    """
    评论审核通过时通知评论者
    
    实际项目中可以:
    - 发送站内通知
    - 发送邮件通知
    """
    try:
        logger.info(f'Comment approved: {comment.id}')
        
        # TODO: 实现通知逻辑
        # Notification.objects.create(
        #     user=comment.user,
        #     type='comment_approved',
        #     comment=comment,
        #     message='您的评论已通过审核'
        # )
        
    except Exception as e:
        logger.error(f'Failed to notify comment author: {e}', exc_info=True)


# ==========================================
# Media Event Handlers
# ==========================================
# 
# 注意: media_uploaded 的实际处理逻辑在 apps/media/receivers.py 中
# 这里保留示例供参考，实际项目中可以添加其他媒体事件处理器
#
# @receiver(media_processed)
# def notify_on_media_processed(sender, media_id, success, processing_type, **kwargs):
#     """媒体处理完成后通知用户"""
#     if success:
#         logger.info(f'Media {media_id} processed successfully: {processing_type}')
#     else:
#         logger.warning(f'Media {media_id} processing failed: {processing_type}')


# ==========================================
# 更多事件处理器可以在这里添加
# ==========================================
# 
# @receiver(user_registered)
# def send_welcome_email(sender, user, **kwargs):
#     """用户注册后发送欢迎邮件"""
#     pass
#
# @receiver(category_created)
# def invalidate_category_cache(sender, category, **kwargs):
#     """分类创建后清除缓存"""
#     pass
