from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
    
    def ready(self):
        """
        应用准备就绪时注册事件处理器
        
        这是 Django 推荐的事件处理器注册方式
        """
        # 导入事件处理器模块，自动注册所有 @receiver 装饰的监听器
        import apps.core.event_handlers  # noqa: F401
