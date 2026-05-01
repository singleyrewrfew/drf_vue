"""
视频处理工具函数模块

提供基于 FFmpeg 的视频元数据获取和缩略图生成功能
"""
import os
import subprocess
import logging

from utils.ffmpeg_utils import FFMPEG, FFPROBE

logger = logging.getLogger(__name__)


def get_video_duration(video_path):
    """
    获取视频时长（秒）

    Args:
        video_path: 视频文件路径

    Returns:
        float: 视频时长，失败返回 None
    """
    try:
        result = subprocess.run(
            [FFPROBE, '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', video_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode != 0:
            logger.error(f"[视频工具] FFPROBE 执行失败: {result.stderr}")
            return None
        return float(result.stdout.strip())
    except Exception as e:
        logger.error(f"[视频工具] 获取视频时长出错: {e}")
        return None


def generate_video_thumbnails(video_path, output_dir, interval=5):
    """
    生成视频缩略图雪碧图（Artplayer 格式）

    Args:
        video_path: 视频文件路径
        output_dir: 输出目录
        interval: 截帧间隔（秒）

    Returns:
        tuple: (缩略图图片路径, 截帧数量)，失败返回 (None, 0)
    """
    os.makedirs(output_dir, exist_ok=True)
    thumbnails_image = os.path.join(output_dir, 'thumbnails.jpg')

    duration = get_video_duration(video_path)
    if duration is None:
        return None, 0

    num_thumbnails = max(1, int(duration / interval))
    cols = min(num_thumbnails, 10)
    rows = (num_thumbnails + cols - 1) // cols
    filter_complex = f"fps=1/{interval},scale=160:90,tile={cols}x{rows}"

    try:
        result = subprocess.run(
            [FFMPEG, '-y', '-i', video_path, '-vf', filter_complex,
             '-frames:v', '1', thumbnails_image],
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode != 0:
            logger.error(f"[视频工具] FFMPEG 执行失败 (退出码 {result.returncode}): {result.stderr}")
            return None, 0
    except subprocess.TimeoutExpired:
        logger.error(f"[视频工具] FFMPEG 处理超时: {video_path}")
        return None, 0
    except Exception as e:
        logger.error(f"[视频工具] 生成缩略图出错: {e}")
        return None, 0

    if not os.path.exists(thumbnails_image):
        logger.error(f"[视频工具] 输出文件未生成: {thumbnails_image}")
        return None, 0

    return thumbnails_image, num_thumbnails
