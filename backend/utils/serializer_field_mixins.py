"""
Serializer Mixins

提供通用的序列化器混入类，减少代码重复
"""


class ContentCountMixin:
    """
    内容数量统计混入类
    
    为分类、标签等模型提供内容数量统计功能
    """
    
    def get_content_count(self, obj):
        """
        获取关联的已发布内容数量
        
        Args:
            obj: 模型实例（必须有 contents 关联字段）
        
        Returns:
            int: 已发布内容的数量
        """
        return obj.contents.filter(status='published').count()


class CommentStatsMixin:
    """
    评论统计混入类
    
    为评论序列化器提供点赞和回复统计功能
    """
    
    def get_is_liked(self, obj):
        """
        检查当前用户是否点赞了该评论
        
        Args:
            obj: Comment 模型实例
        
        Returns:
            bool: 是否已点赞
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False
    
    def get_reply_count(self, obj):
        """
        获取评论的回复数量
        
        Args:
            obj: Comment 模型实例
        
        Returns:
            int: 已审核的回复数量
        """
        return obj.replies.filter(is_approved=True).count()


class AuthorInfoMixin:
    """
    作者信息混入类
    
    为内容、评论等模型提供作者信息字段
    """
    
    def get_author_name(self, obj):
        """
        获取作者用户名
        
        Args:
            obj: 有 author 字段的模型实例
        
        Returns:
            str: 作者用户名
        """
        return obj.author.username if obj.author else None
    
    def get_author_avatar(self, obj):
        """
        获取作者头像
        
        Args:
            obj: 有 author 字段的模型实例
        
        Returns:
            str: 作者头像 URL
        """
        if obj.author and obj.author.avatar:
            return obj.author.avatar.url
        return None


class UserInfoMixin:
    """
    用户信息混入类
    
    为评论等模型提供用户信息字段
    """
    
    def get_user_name(self, obj):
        """
        获取用户名
        
        Args:
            obj: 有 user 字段的模型实例
        
        Returns:
            str: 用户名
        """
        return obj.user.username if obj.user else None
    
    def get_user_avatar(self, obj):
        """
        获取用户头像
        
        Args:
            obj: 有 user 字段的模型实例
        
        Returns:
            str: 用户头像 URL
        """
        if obj.user and obj.user.avatar:
            return obj.user.avatar.url
        return None
    
    def get_user_id(self, obj):
        """
        获取用户ID
        
        Args:
            obj: 有 user 字段的模型实例
        
        Returns:
            str: 用户ID
        """
        return str(obj.user.id) if obj.user else None


class TimestampMixin:
    """
    时间戳格式化混入类
    
    提供统一的时间戳格式化方法
    """
    
    def get_created_at(self, obj):
        """
        格式化创建时间
        
        Args:
            obj: 有 created_at 字段的模型实例
        
        Returns:
            str: 格式化后的创建时间
        """
        if obj.created_at:
            return obj.created_at.strftime('%Y-%m-%d %H:%M:%S')
        return None
    
    def get_updated_at(self, obj):
        """
        格式化更新时间
        
        Args:
            obj: 有 updated_at 字段的模型实例
        
        Returns:
            str: 格式化后的更新时间
        """
        if obj.updated_at:
            return obj.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        return None


class FileURLMixin:
    """
    文件URL混入类
    
    为文件字段提供URL获取方法
    """
    
    def get_file_url(self, obj, field_name='file'):
        """
        获取文件URL
        
        Args:
            obj: 有文件字段的模型实例
            field_name: 文件字段名称，默认为 'file'
        
        Returns:
            str: 文件URL
        """
        file_field = getattr(obj, field_name, None)
        if file_field:
            return file_field.url
        return None


class MediaInfoMixin:
    """
    媒体信息混入类
    
    为媒体模型提供文件信息字段
    """
    
    def get_file_size_display(self, obj):
        """
        获取文件大小的可读格式
        
        Args:
            obj: Media 模型实例
        
        Returns:
            str: 文件大小（如：1.5 MB）
        """
        if not obj.file_size:
            return '0 B'
        
        size = obj.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f'{size:.1f} {unit}'
            size /= 1024.0
        return f'{size:.1f} TB'
    
    def get_file_extension(self, obj):
        """
        获取文件扩展名
        
        Args:
            obj: Media 模型实例
        
        Returns:
            str: 文件扩展名（小写）
        """
        if obj.filename:
            return obj.filename.rsplit('.', 1)[-1].lower()
        return None
