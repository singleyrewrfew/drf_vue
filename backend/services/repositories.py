"""
Repository Layer - Data Access Abstraction

提供统一的数据访问接口，分离数据访问与业务逻辑
"""
from django.utils import timezone
from django.db.models import Count, Prefetch, Q
from apps.contents.models import Content
from apps.comments.models import Comment, CommentLike
from apps.media.models import Media
from apps.categories.models import Category
from apps.tags.models import Tag


class ContentRepository:
    """
    内容数据访问层
    
    职责：
    - 封装所有数据库查询操作
    - 提供统一的查询接口
    - 不包含业务逻辑
    """
    
    @staticmethod
    def create(author, **kwargs):
        """创建内容"""
        return Content.objects.create(author=author, **kwargs)
    
    @staticmethod
    def get_by_id(content_id):
        """根据 ID 获取内容"""
        try:
            return Content.objects.select_related('author', 'category')\
                                  .prefetch_related('tags').get(pk=content_id)
        except Content.DoesNotExist:
            return None
    
    @staticmethod
    def get_published():
        """获取已发布的内容"""
        return Content.objects.filter(status='published')
    
    @staticmethod
    def get_by_author(author):
        """获取作者的内容列表"""
        return Content.objects.filter(author=author)
    
    @staticmethod
    def search(keyword):
        """搜索内容"""
        return Content.objects.filter(
            status='published',
            title__icontains=keyword
        )
    
    @staticmethod
    def update_status(content, status, **extra_fields):
        """更新内容状态"""
        content.status = status
        for field, value in extra_fields.items():
            setattr(content, field, value)
        content.save(update_fields=['status'] + list(extra_fields.keys()))
        return content
    
    @staticmethod
    def publish(content):
        """发布内容（仅更新字段，不包含业务逻辑）"""
        return ContentRepository.update_status(
            content, 
            'published',
            published_at=timezone.now()
        )
    
    @staticmethod
    def archive(content):
        """归档内容（仅更新字段，不包含业务逻辑）"""
        return ContentRepository.update_status(content, 'archived')


class CommentRepository:
    """
    评论数据访问层
    
    职责：
    - 封装所有评论相关的数据库查询操作
    - 提供统一的查询接口
    - 不包含业务逻辑
    """
    
    @staticmethod
    def create(user, article, content, parent=None, reply_to=None):
        """创建评论"""
        return Comment.objects.create(
            user=user,
            article=article,
            content=content,
            parent=parent,
            reply_to=reply_to
        )
    
    @staticmethod
    def get_approved():
        """获取已审核的评论"""
        return Comment.objects.filter(is_approved=True)
    
    @staticmethod
    def get_root_comments():
        """获取根评论（非回复）"""
        return Comment.objects.filter(is_approved=True, parent__isnull=True)
    
    @staticmethod
    def get_by_article(article):
        """获取文章的评论列表（带回复统计）"""
        return Comment.objects.filter(
            article=article,
            is_approved=True,
            parent__isnull=True
        ).annotate(
            reply_count=Count('replies', filter=Q(replies__is_approved=True))
        ).prefetch_related(
            Prefetch('replies', queryset=Comment.objects.filter(is_approved=True))
        )
    
    @staticmethod
    def get_by_user(user):
        """获取用户的评论列表"""
        return Comment.objects.filter(user=user)
    
    @staticmethod
    def approve(comment):
        """审核通过评论"""
        comment.is_approved = True
        comment.save(update_fields=['is_approved'])
        return comment
    
    @staticmethod
    def toggle_like(comment, user):
        """
        切换评论点赞状态
        
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
    
    @staticmethod
    def get_user_liked_comment_ids(user):
        """获取用户点赞的评论 ID 列表"""
        return set(
            CommentLike.objects.filter(user=user).values_list('comment_id', flat=True)
        )


class MediaRepository:
    """
    媒体文件数据访问层
    
    职责：
    - 封装所有媒体文件相关的数据库查询操作
    - 提供统一的查询接口
    - 不包含业务逻辑
    """
    
    @staticmethod
    def get_by_user(user, file_type=None):
        """获取用户的媒体文件列表"""
        queryset = Media.objects.select_related('uploader').filter(uploader=user)
        if file_type:
            queryset = queryset.filter(file_type__startswith=file_type)
        return queryset
    
    @staticmethod
    def get_all(file_type=None):
        """获取所有媒体文件列表"""
        queryset = Media.objects.select_related('uploader')
        if file_type:
            queryset = queryset.filter(file_type__startswith=file_type)
        return queryset
    
    @staticmethod
    def get_statistics(user=None):
        """获取媒体文件统计信息"""
        queryset = Media.objects.all()
        if user:
            queryset = queryset.filter(uploader=user)

        return {
            'total_count': queryset.count(),
            'image_count': queryset.filter(file_type__startswith='image/').count(),
            'video_count': queryset.filter(file_type__startswith='video/').count(),
            'other_count': queryset.exclude(
                file_type__startswith='image/'
            ).exclude(
                file_type__startswith='video/'
            ).count(),
        }


class CategoryRepository:
    """
    分类数据访问层
    
    职责：
    - 封装所有分类相关的数据库查询操作
    - 提供统一的查询接口
    - 不包含业务逻辑
    """
    
    @staticmethod
    def get_root_categories():
        """获取根分类列表"""
        return Category.objects.filter(parent__isnull=True)
    
    @staticmethod
    def get_with_content_count():
        """获取分类列表（包含已发布内容数量）"""
        return Category.objects.select_related('parent').annotate(
            content_count=Count('contents', filter=Q(contents__status='published'))
        )
    
    @staticmethod
    def get_by_id_with_children(category_id):
        """获取分类及其子分类"""
        children_qs = Category.objects.annotate(
            content_count=Count('contents', filter=Q(contents__status='published'))
        )
        
        return Category.objects.prefetch_related(
            Prefetch('children', queryset=children_qs, to_attr='prefetched_children')
        ).annotate(
            content_count=Count('contents', filter=Q(contents__status='published'))
        ).get(id=category_id)
    
    @staticmethod
    def create(name, parent=None, description='', sort_order=0):
        """创建分类"""
        return Category.objects.create(
            name=name,
            parent=parent,
            description=description,
            sort_order=sort_order
        )
    
    @staticmethod
    def get_statistics():
        """获取分类统计信息"""
        total_count = Category.objects.count()
        used_count = Category.objects.annotate(
            content_count=Count('contents')
        ).filter(content_count__gt=0).count()
        
        return {
            'total_count': total_count,
            'used_count': used_count,
            'unused_count': total_count - used_count,
        }


class TagRepository:
    """
    标签数据访问层
    
    职责：
    - 封装所有标签相关的数据库查询操作
    - 提供统一的查询接口
    - 不包含业务逻辑
    """
    
    @staticmethod
    def get_with_content_count():
        """获取标签列表（包含已发布内容数量）"""
        return Tag.objects.annotate(
            content_count=Count('contents', filter=Q(contents__status='published'))
        )
    
    @staticmethod
    def get_popular(limit=10):
        """获取热门标签"""
        return Tag.objects.annotate(
            content_count=Count('contents', filter=Q(contents__status='published'))
        ).filter(content_count__gt=0).order_by('-content_count')[:limit]
    
    @staticmethod
    def get_or_create_by_name(name):
        """根据名称获取或创建标签"""
        return Tag.objects.get_or_create(name=name)
    
    @staticmethod
    def create(name):
        """创建标签"""
        return Tag.objects.create(name=name)
    
    @staticmethod
    def search(keyword):
        """搜索标签"""
        return Tag.objects.filter(name__icontains=keyword)
    
    @staticmethod
    def get_statistics():
        """获取标签统计信息"""
        total_count = Tag.objects.count()
        used_count = Tag.objects.annotate(
            content_count=Count('contents')
        ).filter(content_count__gt=0).count()
        
        return {
            'total_count': total_count,
            'used_count': used_count,
            'unused_count': total_count - used_count,
        }
