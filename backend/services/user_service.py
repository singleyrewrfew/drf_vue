from django.conf import settings
from django.db.models import Count, Sum, Q

from apps.comments.models import Comment
from apps.contents.models import Content
from apps.core.models import User
from apps.media.models import Media
from services.base import ModelService
from utils.cache_utils import cache_get, cache_set, get_cache_key


class UserService(ModelService):
    """
    用户业务逻辑服务层
    
    封装所有与用户相关的业务逻辑
    """
    model_class = User

    @classmethod
    def authenticate(cls, username, password):
        """
        验证用户登录
        
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            tuple: (用户对象, 错误信息)
        """
        if not username or not password:
            return None, '用户名和密码不能为空'

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None, '用户名或密码错误'

        if not user.check_password(password):
            return None, '用户名或密码错误'

        if not user.is_active:
            return None, '账户已被禁用'

        return user, None

    @classmethod
    def get_popular_authors(cls, limit=10):
        """
        获取热门作者列表
        
        Args:
            limit: 返回数量限制
            
        Returns:
            list: 热门作者列表
        """
        cache_key = get_cache_key('popular_authors', limit)
        cached = cache_get(cache_key)
        if cached is not None:
            return cached

        users = User.objects.filter(
            contents__status='published'
        ).annotate(
            article_count=Count('contents')
        ).order_by('-article_count')[:limit]

        result = [
            {
                'id': str(user.id),
                'username': user.username,
                'avatar': user.avatar.url if user.avatar else None,
                'article_count': user.article_count,
            }
            for user in users
        ]

        cache_set(cache_key, result, settings.CACHE_TTL['POPULAR'])
        return result

    @classmethod
    def get_admin_statistics(cls):
        """
        获取管理员仪表盘统计数据
        
        Returns:
            dict: 统计数据
        """
        cache_key = get_cache_key('stats', 'admin')
        cached = cache_get(cache_key)
        if cached is not None:
            return cached

        content_stats = Content.objects.aggregate(
            total=Count('id'),
            published=Count('id', filter=Q(status='published')),
            drafts=Count('id', filter=Q(status='draft')),
            total_views=Sum('view_count')
        )

        recent_contents = Content.objects.filter(
            status='published'
        ).select_related('author').order_by('-created_at')[:5]

        result = {
            'contents': content_stats['total'],
            'published': content_stats['published'],
            'drafts': content_stats['drafts'],
            'comments': Comment.objects.count(),
            'users': User.objects.count(),
            'media': Media.objects.count(),
            'views': content_stats['total_views'] or 0,
            'recent_contents': [
                {
                    'id': str(content.id),
                    'title': content.title,
                    'author_name': content.author.username,
                    'view_count': content.view_count,
                    'created_at': content.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                }
                for content in recent_contents
            ],
        }

        cache_set(cache_key, result, settings.CACHE_TTL['STATS'])
        return result

    @classmethod
    def get_user_statistics(cls, user):
        """
        获取用户仪表盘统计数据
        
        Args:
            user: 用户对象
            
        Returns:
            dict: 统计数据
        """
        cache_key = get_cache_key('stats', 'user', user.id)
        cached = cache_get(cache_key)
        if cached is not None:
            return cached

        content_stats = Content.objects.filter(author=user).aggregate(
            total=Count('id'),
            published=Count('id', filter=Q(status='published')),
            drafts=Count('id', filter=Q(status='draft')),
            total_views=Sum('view_count')
        )

        recent_contents = Content.objects.filter(
            author=user,
            status='published'
        ).order_by('-created_at')[:5]

        result = {
            'my_contents': content_stats['total'],
            'my_published': content_stats['published'],
            'my_drafts': content_stats['drafts'],
            'my_comments': Comment.objects.filter(user=user).count(),
            'my_views': content_stats['total_views'] or 0,
            'recent_contents': [
                {
                    'id': str(content.id),
                    'title': content.title,
                    'view_count': content.view_count,
                    'created_at': content.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                }
                for content in recent_contents
            ],
        }

        cache_set(cache_key, result, settings.CACHE_TTL['STATS'])
        return result

    @classmethod
    def change_password(cls, user, old_password, new_password):
        """
        修改用户密码
        
        Args:
            user: 用户对象
            old_password: 原密码
            new_password: 新密码
            
        Returns:
            tuple: (是否成功, 错误信息)
        """
        if not user.check_password(old_password):
            return False, '原密码错误'

        user.set_password(new_password)
        user.save(update_fields=['password'])
        return True, None

    @classmethod
    def update_profile(cls, user, **kwargs):
        """
        更新用户资料
        
        Args:
            user: 用户对象
            **kwargs: 要更新的字段
            
        Returns:
            User: 更新后的用户对象
        """
        for attr, value in kwargs.items():
            if hasattr(user, attr):
                setattr(user, attr, value)
        user.save()
        return user

    @classmethod
    def can_user_modify(cls, target_user, current_user):
        """
        检查用户是否可以修改目标用户
        
        Args:
            target_user: 目标用户对象
            current_user: 当前用户对象
            
        Returns:
            bool: 是否可以修改
        """
        if current_user.is_admin or current_user.is_superuser:
            return True
        return target_user.id == current_user.id
