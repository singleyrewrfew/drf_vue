"""
Core models and utilities

提供项目中通用的模型引用和工具

注意：User 模型请使用 Django 标准方式获取：
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
或在模型字段中使用：
    from django.conf import settings
    ForeignKey(settings.AUTH_USER_MODEL, ...)
"""
