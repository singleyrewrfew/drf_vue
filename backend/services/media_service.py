import logging
import os
import shutil

from django.conf import settings

from apps.media.models import Media
from services.base import ModelService
from services.repositories import MediaRepository

logger = logging.getLogger(__name__)


class MediaService(ModelService):
    """
    媒体文件业务逻辑服务层
    
    职责：
    - 封装业务逻辑（权限检查、引用计数、物理文件删除）
    - 协调多个 Repository 操作
    - 不包含直接的数据库查询
    """
    model_class = Media
    
    # Repository 实例
    repo = MediaRepository

    @classmethod
    def get_user_media(cls, user, file_type=None):
        """
        获取用户的媒体文件列表
        
        ⚠️  建议使用: MediaRepository.get_by_user(user, file_type)
        
        Args:
            user: 用户对象
            file_type: 文件类型过滤（可选）
            
        Returns:
            QuerySet: 媒体文件查询集
        """
        return MediaRepository.get_by_user(user, file_type)

    @classmethod
    def get_all_media(cls, file_type=None):
        """
        获取所有媒体文件列表
        
        ⚠️  建议使用: MediaRepository.get_all(file_type)
        
        Args:
            file_type: 文件类型过滤（可选）
            
        Returns:
            QuerySet: 媒体文件查询集
        """
        return MediaRepository.get_all(file_type)

    @classmethod
    def can_user_access(cls, media, user):
        """
        检查用户是否可以访问媒体文件
        
        Args:
            media: 媒体对象
            user: 用户对象
            
        Returns:
            bool: 是否可以访问
        """
        # is_admin 已包含 is_superuser 检查
        if user.is_admin:
            return True
        return media.uploader_id == user.id

    @classmethod
    def can_user_modify(cls, media, user):
        """
        检查用户是否可以修改媒体文件
        
        Args:
            media: 媒体对象
            user: 用户对象
            
        Returns:
            bool: 是否可以修改
        """
        # is_admin 已包含 is_superuser 检查
        if user.is_admin:
            return True
        return media.uploader_id == user.id

    @classmethod
    def delete_physical_files(cls, media):
        """
        删除媒体文件的物理文件
        
        Args:
            media: 媒体对象
            
        Returns:
            bool: 是否删除成功
        """
        success = True
        
        if media.file:
            try:
                file_path = media.file.path
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    logger.info(f"已删除文件: {file_path}")
            except Exception as e:
                logger.error(f"删除文件异常: {e}")
                success = False

        if media.thumbnails:
            try:
                thumbnails_dir = os.path.dirname(media.thumbnails.path)
                if os.path.isdir(thumbnails_dir):
                    shutil.rmtree(thumbnails_dir)
                    logger.info(f"已删除缩略图目录: {thumbnails_dir}")
            except Exception as e:
                logger.error(f"删除缩略图失败: {e}")
                success = False

        return success

    @classmethod
    def delete_media(cls, media):
        """
        删除媒体文件（包含引用计数逻辑）
        
        Args:
            media: 媒体对象
            
        Returns:
            bool: 是否删除成功
        """
        media_id = str(media.id)

        if media.reference:
            original = media.reference
            original.decrement_reference_count()
            logger.info(f"删除引用记录 {media_id}，原始文件 {original.id} 引用计数: {original.reference_count}")
        else:
            logger.info(f"删除原始文件 {media_id}，引用计数: {media.reference_count}，引用记录数: {media.references.count()}")

            if media.reference_count == 0 and not media.references.exists():
                cls.delete_physical_files(media)
            else:
                logger.info(f"保留物理文件（仍有引用）")

        media.delete()
        logger.info(f"已删除数据库记录: {media_id}")
        return True

    @classmethod
    def regenerate_thumbnails(cls, media):
        """
        重新生成视频缩略图
        
        Args:
            media: 媒体对象
            
        Returns:
            dict: 包含状态信息的字典
            
        Raises:
            ValueError: 如果不是视频文件
        """
        if not media.is_video:
            raise ValueError('只能为视频文件生成缩略图')

        media.thumbnail_status = 'pending'
        media.save(update_fields=['thumbnail_status'])
        media.generate_thumbnails_async()

        return {
            'message': '缩略图生成任务已启动',
            'thumbnail_status': 'pending'
        }

    @classmethod
    def get_media_statistics(cls, user=None):
        """
        获取媒体文件统计信息
        
        ⚠️  建议使用: MediaRepository.get_statistics(user)
        
        Args:
            user: 用户对象（可选，用于筛选用户的媒体）
            
        Returns:
            dict: 统计信息
        """
        return MediaRepository.get_statistics(user)
