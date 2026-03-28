"""
文件上传管理器

提供安全的文件上传临时存储、验证和迁移功能
"""
import os
import shutil
import logging
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Tuple
from django.conf import settings

logger = logging.getLogger(__name__)


class UploadFileManager:
    """
    文件上传管理器
    
    功能：
    1. 临时目录管理（按日期分离子目录）
    2. 文件完整性检查
    3. 自动清理过期临时文件
    4. 原子性文件移动操作
    """
    
    def __init__(self):
        self.temp_root = getattr(settings, 'UPLOAD_TEMP_DIR', settings.MEDIA_ROOT / 'upload_temp')
        self.max_age_days = 7  # 临时文件保留天数
        self._ensure_temp_dir()
    
    def _ensure_temp_dir(self):
        """确保临时目录存在"""
        try:
            self.temp_root.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Upload temp directory ensured: {self.temp_root}")
        except Exception as e:
            logger.error(f"Failed to create temp directory: {e}")
            raise
    
    def get_temp_path(self, filename: str) -> Path:
        """
        获取临时文件路径（带日期子目录）
        
        Args:
            filename: 原始文件名
            
        Returns:
            临时文件路径
        """
        date_subdir = datetime.now().strftime('%Y-%m-%d')
        temp_dir = self.temp_root / date_subdir
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成唯一文件名避免冲突
        unique_filename = f"{datetime.now().timestamp()}_{filename}"
        return temp_dir / unique_filename
    
    def save_temp_file(self, uploaded_file) -> Tuple[Path, int]:
        """
        保存上传的文件到临时目录
        
        Args:
            uploaded_file: Django UploadedFile 对象
            
        Returns:
            (临时文件路径，文件大小)
        """
        temp_path = self.get_temp_path(uploaded_file.name)
        
        try:
            # 分块写入文件（节省内存）
            total_size = 0
            with open(temp_path, 'wb') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)
                    total_size += len(chunk)
            
            logger.info(f"File saved to temp: {temp_path} ({total_size} bytes)")
            return temp_path, total_size
            
        except Exception as e:
            logger.error(f"Failed to save temp file: {e}")
            # 清理失败的文件
            if temp_path.exists():
                try:
                    temp_path.unlink()
                except Exception:
                    pass
            raise
    
    def verify_temp_file(self, temp_path: Path, expected_hash: str = None) -> bool:
        """
        验证临时文件
        
        Args:
            temp_path: 临时文件路径
            expected_hash: 期望的 MD5 哈希值（可选）
            
        Returns:
            验证是否通过
        """
        if not temp_path.exists():
            logger.error(f"Temp file does not exist: {temp_path}")
            return False
        
        if not temp_path.is_file():
            logger.error(f"Temp path is not a file: {temp_path}")
            return False
        
        # 验证文件大小（不能为 0）
        file_size = temp_path.stat().st_size
        if file_size == 0:
            logger.error(f"Temp file is empty: {temp_path}")
            return False
        
        # 验证文件哈希
        if expected_hash:
            import hashlib
            md5 = hashlib.md5()
            with open(temp_path, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b''):
                    md5.update(chunk)
            
            actual_hash = md5.hexdigest()
            if actual_hash != expected_hash:
                logger.error(f"Hash mismatch: expected={expected_hash}, actual={actual_hash}")
                return False
        
        logger.debug(f"Temp file verified: {temp_path}")
        return True
    
    def move_to_final_location(
        self,
        temp_path: Path,
        final_path: Path,
        overwrite: bool = False
    ) -> bool:
        """
        将临时文件移动到最终位置（原子操作）
        
        Args:
            temp_path: 临时文件路径
            final_path: 最终文件路径
            overwrite: 是否覆盖已存在的文件
            
        Returns:
            移动是否成功
        """
        try:
            # 确保目标目录存在
            final_path.parent.mkdir(parents=True, exist_ok=True)
            
            if final_path.exists() and not overwrite:
                logger.error(f"Final file already exists: {final_path}")
                return False
            
            # 使用 shutil.move 进行原子移动
            shutil.move(str(temp_path), str(final_path))
            logger.info(f"File moved from {temp_path} to {final_path}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to move file: {e}")
            return False
    
    def cleanup_old_temp_files(self) -> int:
        """
        清理过期的临时文件
        
        Returns:
            清理的文件数量
        """
        cleaned_count = 0
        cutoff_date = datetime.now() - timedelta(days=self.max_age_days)
        
        try:
            if not self.temp_root.exists():
                return 0
            
            # 遍历所有日期子目录
            for date_dir in self.temp_root.iterdir():
                if not date_dir.is_dir():
                    continue
                
                try:
                    # 解析目录名中的日期
                    dir_date = datetime.strptime(date_dir.name, '%Y-%m-%d')
                    
                    if dir_date < cutoff_date:
                        # 删除整个目录
                        shutil.rmtree(date_dir)
                        cleaned_count += 1
                        logger.info(f"Cleaned old temp directory: {date_dir}")
                        
                except ValueError:
                    # 不是日期格式的目录，跳过
                    continue
                    
        except Exception as e:
            logger.error(f"Error during temp file cleanup: {e}")
        
        return cleaned_count
    
    def delete_temp_file(self, temp_path: Path) -> bool:
        """
        删除临时文件
        
        Args:
            temp_path: 临时文件路径
            
        Returns:
            删除是否成功
        """
        try:
            if temp_path.exists():
                temp_path.unlink()
                logger.debug(f"Deleted temp file: {temp_path}")
                return True
            else:
                logger.warning(f"Temp file does not exist: {temp_path}")
                return False
        except Exception as e:
            logger.error(f"Failed to delete temp file: {e}")
            return False
    
    def get_temp_stats(self) -> dict:
        """
        获取临时目录统计信息
        
        Returns:
            统计信息字典
        """
        stats = {
            'total_size': 0,
            'file_count': 0,
            'directory_count': 0
        }
        
        try:
            if not self.temp_root.exists():
                return stats
            
            for item in self.temp_root.rglob('*'):
                if item.is_file():
                    stats['file_count'] += 1
                    stats['total_size'] += item.stat().st_size
                elif item.is_dir():
                    stats['directory_count'] += 1
                    
        except Exception as e:
            logger.error(f"Error getting temp stats: {e}")
        
        return stats


# 全局上传管理器实例
upload_manager = UploadFileManager()


def cleanup_upload_temp_files():
    """
    清理上传临时文件的便捷函数
    
    可定期调用（如每天凌晨执行）
    """
    cleaned = upload_manager.cleanup_old_temp_files()
    stats = upload_manager.get_temp_stats()
    
    logger.info(
        f"Temp file cleanup completed: "
        f"cleaned_dirs={cleaned}, "
        f"current_files={stats['file_count']}, "
        f"current_size={stats['total_size'] / 1024 / 1024:.2f}MB"
    )
    
    return stats
