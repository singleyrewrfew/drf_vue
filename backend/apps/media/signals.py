"""
⚠️  DEPRECATED - 已迁移到 apps.core.events

此文件保留仅为向后兼容，建议使用:
from apps.core.events import media_uploaded, media_processed
"""
import django.dispatch

# 保留旧信号以兼容现有代码
video_uploaded = django.dispatch.Signal()
video_thumbnail_generated = django.dispatch.Signal()
