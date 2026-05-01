"""
FFmpeg 工具函数模块

提供 FFmpeg/FFprobe 可执行文件查找功能
"""
import os
import platform
import shutil
import logging

from django.conf import settings

logger = logging.getLogger(__name__)


def get_ffmpeg_executable(name):
    """
    查找 FFmpeg/FFprobe 可执行文件路径

    搜索顺序：Django 配置 -> 系统 PATH -> 额外配置/常见目录

    Args:
        name: 可执行文件名称 ('ffmpeg' 或 'ffprobe')

    Returns:
        str: 可执行文件的完整路径

    Raises:
        FileNotFoundError: 当找不到可执行文件时抛出异常
    """
    exe_name = f'{name}.exe' if platform.system() == 'Windows' else name

    # 1. 优先使用 Django settings 中配置的 FFMPEG_PATH
    ffmpeg_config_path = getattr(settings, 'FFMPEG_PATH', None)
    if ffmpeg_config_path:
        exe_path = os.path.join(ffmpeg_config_path, exe_name)
        if os.path.exists(exe_path):
            return exe_path

    # 2. 尝试从系统环境变量 PATH 中查找
    system_path = shutil.which(name)
    if system_path:
        return system_path

    # 3. 最后尝试额外配置的路径和系统常见安装目录
    fallback_paths = list(getattr(settings, 'FFMPEG_ADDITIONAL_PATHS', []))

    if platform.system() == 'Windows':
        fallback_paths.extend([
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'ffmpeg', 'bin'),
            os.path.join(os.environ.get('PROGRAMFILES', ''), 'ffmpeg', 'bin'),
        ])
    else:
        fallback_paths.extend([
            '/usr/bin',
            '/usr/local/bin',
            '/opt/ffmpeg/bin',
        ])

    for path in fallback_paths:
        if path:
            exe_path = os.path.join(path, exe_name)
            if os.path.exists(exe_path):
                return exe_path

    # 如果所有路径都失败，返回原始名称，让 subprocess 尝试在系统 PATH 中查找
    logger.warning(f"未在配置的路径中找到 {name}，将尝试使用系统默认 PATH")
    return name


# 模块加载时初始化全局常量
FFMPEG = get_ffmpeg_executable('ffmpeg')
FFPROBE = get_ffmpeg_executable('ffprobe')
