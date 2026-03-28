"""
诊断视频缩略图问题
"""

import os
import subprocess

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from apps.media.models import Media, FFMPEG, FFPROBE
from django.conf import settings

print("=" * 80)
print("视频缩略图诊断报告")
print("=" * 80)

# 1. 检查视频文件
videos = Media.objects.filter(file_type__startswith='video/')
print(f"\n1. 视频文件总数: {videos.count()}")

if videos.count() == 0:
    print("   ❌ 没有找到视频文件")
else:
    print(f"   ✅ 找到 {videos.count()} 个视频文件")
    
    # 2. 检查缩略图状态分布
    print("\n2. 缩略图状态分布:")
    status_counts = {}
    for video in videos:
        status = video.thumbnail_status
        status_counts[status] = status_counts.get(status, 0) + 1
    
    for status, count in status_counts.items():
        print(f"   - {status}: {count} 个")
    
    # 3. 检查已完成的缩略图
    completed = videos.filter(thumbnail_status='completed')
    print(f"\n3. 已完成缩略图生成: {completed.count()} 个")
    
    if completed.count() > 0:
        print("\n   详细信息:")
        for video in completed[:5]:
            print(f"   - ID: {video.id}")
            print(f"     文件名: {video.filename}")
            print(f"     缩略图字段: {video.thumbnails}")
            print(f"     缩略图数量: {video.thumbnails_count}")
            if video.thumbnails:
                try:
                    print(f"     缩略图URL: {video.thumbnails.url}")
                    if video.thumbnails.path:
                        exists = os.path.exists(video.thumbnails.path)
                        print(f"     文件存在: {'✅ 是' if exists else '❌ 否'}")
                except Exception as e:
                    print(f"     ❌ 获取缩略图信息失败: {e}")
            else:
                print(f"     缩略图字段为空")
            print()
    
    # 4. 检查失败的缩略图
    failed = videos.filter(thumbnail_status='failed')
    print(f"\n4. 缩略图生成失败: {failed.count()} 个")
    
    if failed.count() > 0:
        print("\n   失败的视频:")
        for video in failed[:5]:
            print(f"   - {video.filename} (ID: {video.id})")
    
    # 5. 检查待处理的缩略图
    pending = videos.filter(thumbnail_status__in=['pending', 'processing'])
    print(f"\n5. 待处理/处理中: {pending.count()} 个")
    
    if pending.count() > 0:
        print("\n   待处理的视频:")
        for video in pending[:5]:
            print(f"   - {video.filename} (ID: {video.id}, 状态: {video.thumbnail_status})")

# 6. 检查 FFmpeg
print("\n6. FFmpeg 检查:")
print(f"   FFmpeg 路径: {FFMPEG}")
print(f"   FFprobe 路径: {FFPROBE}")

try:
    result = subprocess.run([FFMPEG, '-version'], capture_output=True, timeout=5)
    if result.returncode == 0:
        print("   ✅ FFmpeg 可用")
    else:
        print("   ❌ FFmpeg 不可用")
except Exception as e:
    print(f"   ❌ FFmpeg 检查失败: {e}")

try:
    result = subprocess.run([FFPROBE, '-version'], capture_output=True, timeout=5)
    if result.returncode == 0:
        print("   ✅ FFprobe 可用")
    else:
        print("   ❌ FFprobe 不可用")
except Exception as e:
    print(f"   ❌ FFprobe 检查失败: {e}")

# 7. 检查媒体目录
print("\n7. 媒体目录检查:")
media_root = settings.MEDIA_ROOT
thumbnails_dir = os.path.join(media_root, 'thumbnails')

print(f"   MEDIA_ROOT: {media_root}")
print(f"   缩略图目录: {thumbnails_dir}")

if os.path.exists(thumbnails_dir):
    print("   ✅ 缩略图目录存在")
    thumbnail_files = []
    for root, dirs, files in os.walk(thumbnails_dir):
        for file in files:
            if file.endswith('.jpg'):
                thumbnail_files.append(os.path.join(root, file))
    print(f"   缩略图文件数量: {len(thumbnail_files)}")
    if len(thumbnail_files) > 0:
        print(f"   示例文件: {thumbnail_files[0]}")
else:
    print("   ❌ 缩略图目录不存在")

print("\n" + "=" * 80)
print("诊断完成")
print("=" * 80)
