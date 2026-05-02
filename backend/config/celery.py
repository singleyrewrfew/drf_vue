"""
Celery 配置模块

初始化 Celery 应用实例，配置任务队列、序列化和结果后端。

使用方式：
    from config.celery import app
    
    @app.task
    def my_task():
        pass
"""

import os
from pathlib import Path
from celery import Celery
from dotenv import load_dotenv

os.environ.setdefault('DJANGO_ENV', 'development')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

BASE_DIR = Path(__file__).resolve().parent.parent
env_file = BASE_DIR / f".env.{os.getenv('DJANGO_ENV', 'development')}"
if env_file.exists():
    load_dotenv(env_file)

app = Celery('cms')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """
    调试任务，用于验证 Celery 配置是否正确
    
    运行方式：
        celery -A config.celery worker -l info
    """
    print(f'Request: {self.request!r}')
