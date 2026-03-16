from django.apps import AppConfig

class TagsConfig(AppConfig):
    """
    标签管理应用配置
    
    功能：
    - 定义应用的默认自增字段类型
    - 定义应用的名称和可读名称
    """
    # 默认自增字段类型
    default_auto_field = 'django.db.models.BigAutoField'
    # 应用名称（用于 INSTALLED_APPS）
    name = 'apps.tags'
    # 应用的可读名称（用于 Django 管理后台）
    verbose_name = '标签管理'
