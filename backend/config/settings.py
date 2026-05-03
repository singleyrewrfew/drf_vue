"""
Django Settings for CMS Project

Configuration is loaded from environment-specific .env files:
- Development: .env.development
- Production: .env.production
"""

import os
import sys
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

# ==================== 基础路径配置 ====================

BASE_DIR = Path(__file__).resolve().parent.parent

ENV = os.getenv('DJANGO_ENV', 'development')

env_file = BASE_DIR / f'.env.{ENV}'
if env_file.exists():
    load_dotenv(env_file)

# ==================== 安全配置 ====================

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'

# 开发环境 fallback
if not SECRET_KEY and DEBUG:
    SECRET_KEY = 'dev-only-insecure-key-change-in-production'

# 生产环境强制要求 SECRET_KEY
if not SECRET_KEY and not DEBUG:
    from django.core.exceptions import ImproperlyConfigured
    raise ImproperlyConfigured(
        "生产环境必须设置 DJANGO_SECRET_KEY 环境变量。"
    )

# DEBUG 警告
def _warn_if_debug(message: str):
    """
    仅在 DEBUG 模式下发出警告
    
    注意：Django 开发服务器会启动两个进程（主进程和工作进程），
    通过检查 RUN_MAIN 环境变量避免重复警告。
    """
    if DEBUG and os.environ.get('RUN_MAIN') != 'true':
        import warnings
        warnings.warn(f"⚠️  WARNING: {message}", RuntimeWarning, stacklevel=2)

if not os.getenv('DJANGO_SECRET_KEY') and DEBUG:
    _warn_if_debug("正在使用开发环境的 SECRET_KEY。生产环境请设置 DJANGO_SECRET_KEY！")

_warn_if_debug("DEBUG 模式已启用！切勿在生产环境中使用。")

# 允许的主机
if DEBUG:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1'] + \
                   os.getenv('DJANGO_DEBUG_ALLOWED_HOSTS', '').split(',')
else:
    ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',')

# ==================== 应用配置 ====================
INSTALLED_APPS = [
    # Django 内置应用
    'django.contrib.admin',
    'apps.core',                                         # 必须在 auth 之前
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # 第三方应用
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'drf_spectacular',
    'django_celery_beat',
    'django_celery_results',
    
    # 自定义应用
    'apps.users',
    'apps.roles',
    'apps.contents',
    'apps.categories',
    'apps.tags',
    'apps.media',
    'apps.comments',
]

# ==================== 中间件配置 ====================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.ApiResultInterceptorMiddleware.ResponseLogMiddleware',
]

# ==================== 核心配置 ====================

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
AUTH_USER_MODEL = 'users.User'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==================== 模板配置 ====================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ==================== 数据库配置 ====================
DB_ENGINE = os.getenv('DB_ENGINE', 'django.db.backends.sqlite3')

if DB_ENGINE == 'django.db.backends.sqlite3':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.getenv('SQLITE_DB_NAME', BASE_DIR / 'db.sqlite3'),
            # SQLite 不支持连接池，但设置超时避免锁定
            'TIMEOUT': 20,  # 等待锁释放的超时时间（秒）
        }
    }
else:
    # MySQL/MariaDB 数据库配置
    # 从环境变量读取连接池配置，提供合理的默认值
    conn_max_age_default = '0' if DEBUG else '300'
    health_checks_default = 'False' if DEBUG else 'True'
    
    CONN_MAX_AGE = int(os.getenv('DB_CONN_MAX_AGE', conn_max_age_default))
    CONN_HEALTH_CHECKS = os.getenv('DB_CONN_HEALTH_CHECKS', health_checks_default) == 'True'
    
    # 验证配置合理性
    if CONN_MAX_AGE < 0:
        import warnings
        warnings.warn(
            f"⚠️  DB_CONN_MAX_AGE 设置为 {CONN_MAX_AGE}（负值），已重置为 0",
            RuntimeWarning
        )
        CONN_MAX_AGE = 0
    
    if CONN_MAX_AGE > 600 and not DEBUG:
        import warnings
        warnings.warn(
            f"⚠️  DB_CONN_MAX_AGE 设置为 {CONN_MAX_AGE} 秒（>600），"
            f"可能导致连接泄漏。建议设置为 300-600 秒。",
            RuntimeWarning
        )
    
    DATABASES = {
        'default': {
            'ENGINE': DB_ENGINE,
            'NAME': os.getenv('DB_NAME', 'cms_db'),
            'USER': os.getenv('DB_USER', 'root'),
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '3306'),
            
            # MySQL 特定选项
            'OPTIONS': {
                'charset': 'utf8mb4',                    # 支持 emoji 等 Unicode 字符
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",  # 严格模式
                'connect_timeout': 10,                   # 连接超时（秒）
                'autocommit': True,                      # 自动提交事务
            },
            
            # 连接池配置
            'CONN_MAX_AGE': CONN_MAX_AGE,               # 连接持久化时间（秒）
            'CONN_HEALTH_CHECKS': CONN_HEALTH_CHECKS,   # 健康检查开关
        }
    }
    
    # 打印连接池配置信息（仅在启动时）
    if os.environ.get('RUN_MAIN') != 'true' or 'gunicorn' in sys.argv:
        print(f"\n📊 数据库连接池配置:")
        print(f"   - CONN_MAX_AGE: {CONN_MAX_AGE}秒 {'(禁用)' if CONN_MAX_AGE == 0 else ''}")
        print(f"   - CONN_HEALTH_CHECKS: {'✅ 启用' if CONN_HEALTH_CHECKS else '❌ 禁用'}")
        if CONN_MAX_AGE > 0:
            print(f"   - 预计最大连接数: Gunicorn workers 数量")
            print(f"   - 连接复用率: 高（减少连接创建开销）")
        print()

# ==================== 国际化配置 ====================
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==================== 静态文件配置 ====================
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'

# 测试环境使用独立目录
if 'pytest' in sys.modules:
    MEDIA_ROOT = BASE_DIR / 'media_test'
else:
    MEDIA_ROOT = BASE_DIR / 'media'

UPLOAD_TEMP_DIR = os.getenv('UPLOAD_TEMP_DIR', MEDIA_ROOT / 'upload_temp')

# ==================== DRF 配置 ====================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'DATE_FORMAT': '%Y-%m-%d',
}

# ==================== JWT 配置 ====================
SIMPLE_JWT = {
    # Token 有效期
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),      # Access Token: 2小时
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),       # Refresh Token: 7天
    
    # Token 轮换与黑名单
    'ROTATE_REFRESH_TOKENS': True,                     # 启用 Refresh Token 轮换
    'BLACKLIST_AFTER_ROTATION': True,                  # 轮换后将旧 token 加入黑名单
    
    # 认证头配置
    'AUTH_HEADER_TYPES': ('Bearer',),                  # 使用 Bearer 认证
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',          # 请求头名称
    
    # 安全增强
    'USER_ID_FIELD': 'id',                             # 用户 ID 字段
    'USER_ID_CLAIM': 'user_id',                        # JWT claim 中的用户 ID 键名
    'TOKEN_TYPE_CLAIM': 'token_type',                  # Token 类型声明
    
    # 算法配置（使用 HS256，对称加密）
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': os.getenv('JWT_SECRET_KEY', SECRET_KEY),  # 签名密钥
    'VERIFYING_KEY': None,                             # 验证密钥（对称加密时不需要）
    
    # 其他配置
    'AUDIENCE': None,                                  # 受众（可选）
    'ISSUER': None,                                    # 发行者（可选）
    'JWK_URL': None,                                   # JWK URL（可选）
    'LEEWAY': 0,                                       # 时间容差（秒）
}

# ==================== CORS 配置 ====================
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')
    if origin.strip()
]

if DEBUG and os.getenv('CORS_ALLOW_ALL_FOR_DEV', 'False') == 'True':
    CORS_ALLOW_ALL_ORIGINS = True
    print("⚠️  警告：开发环境下 CORS 允许所有来源访问！")

CORS_ALLOW_CREDENTIALS = True

# ==================== 安全配置 ====================
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# ==================== API 文档配置 ====================
SPECTACULAR_SETTINGS = {
    'TITLE': 'CMS API',
    'DESCRIPTION': '内容管理系统 API 文档',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# ==================== 文件上传配置 ====================
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
FILE_UPLOAD_PERMISSIONS = 0o644
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB

ALLOWED_IMAGE_TYPES = [
    'image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml'
]
ALLOWED_VIDEO_TYPES = [
    'video/mp4', 'video/webm', 'video/ogg', 'video/quicktime'
]
ALLOWED_DOCUMENT_TYPES = [
    'application/pdf', 'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
]
ALLOWED_FILE_TYPES = ALLOWED_IMAGE_TYPES + ALLOWED_VIDEO_TYPES + ALLOWED_DOCUMENT_TYPES

FFMPEG_PATH = os.getenv('FFMPEG_PATH', '')
FFMPEG_ADDITIONAL_PATHS = [
    p.strip() for p in os.getenv('FFMPEG_ADDITIONAL_PATHS', '').split(',') if p.strip()
]

# ==================== 日志配置 ====================

# 确保日志目录存在并具备写入权限
LOG_DIR = BASE_DIR / 'logs'
if not LOG_DIR.exists():
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"警告: 无法创建日志目录 {LOG_DIR}: {e}")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    
    'filters': {
        # 敏感数据过滤器：自动脱敏密码、Token 等敏感信息
        'sensitive_data': {
            '()': 'utils.log_utils.SensitiveDataFilter',
        },
    },
    
    'formatters': {
        'simple': {
            'format': '{asctime} [{levelname}] {message}',
            'style': '{',
            'datefmt': '%H:%M:%S'
        },
        'verbose': {
            'format': '{asctime} [{levelname}] [PID:{process}] [TID:{thread}] {filename}:{funcName}:{lineno} - {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'filters': ['sensitive_data'],  # 添加敏感数据过滤
        },
        'file': {
            'level': 'DEBUG',
            'class': 'utils.log_handlers.SafeRotatingFileHandler',
            'filename': LOG_DIR / 'django.log',
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 5,
            'formatter': 'verbose',
            'encoding': 'utf-8',
            'filters': ['sensitive_data'],  # 添加敏感数据过滤
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'utils.log_handlers.SafeRotatingFileHandler',
            'filename': LOG_DIR / 'error.log',
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose',
            'encoding': 'utf-8',
            'filters': ['sensitive_data'],  # 添加敏感数据过滤
        },
    },
    
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',  # 改为 WARNING，避免记录所有 200 OK 请求
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': [],  # 关闭 SQL 日志输出，避免控制台混乱
            'level': 'WARNING',  # 仅记录警告和错误
            'propagate': False,
        },
        'apps': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'apps.media': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# ==================== DRF 异常处理 ====================
REST_FRAMEWORK["EXCEPTION_HANDLER"] = 'utils.exceptions.custom_exception_handler'

# ==================== 缓存配置 ====================
REDIS_URL = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/1')
CACHE_KEY_PREFIX = 'cms'

CACHE_TTL = {
    'DEFAULT': 300,
    'STATS': 120,
    'POPULAR': 300,
    'CONTENT_LIST': 120,
    'CATEGORY_LIST': 300,
    'TAG_LIST': 300,
    'ROLE_LIST': 600,
    'PERMISSION_LIST': 600,
}

# ==================== Celery 配置 ====================
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/0'))
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'django-db')
CELERY_RESULT_EXTENDED = True
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = True
CELERY_TASK_TRACK_STARTED = True

# 任务超时配置（根据任务类型设置合理的超时时间）
# 视频缩略图生成通常需要 30秒-5分钟，设置为 10 分钟足够
CELERY_TASK_TIME_LIMIT = 10 * 60  # 硬超时：10 分钟
# Note: soft_time_limit not supported on Windows (no SIGUSR1 signal)

# Worker 并发和预取配置
# prefetch_multiplier=4 表示每个 worker 预取 4 个任务，提高吞吐量
# 对于 CPU 密集型任务（视频处理），建议设置为 1-2
CELERY_WORKER_PREFETCH_MULTIPLIER = 2
CELERY_WORKER_CONCURRENCY = 2  # 默认并发数（可根据服务器 CPU 核心数调整）
CELERY_WORKER_MAX_TASKS_PER_CHILD = 100  # 每执行 100 个任务重启 worker，防止内存泄漏

# Broker 连接配置
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BROKER_POOL_LIMIT = 10  # 连接池大小

# 任务重试配置
CELERY_TASK_DEFAULT_RETRY_DELAY = 60  # 默认重试延迟 60 秒
CELERY_TASK_MAX_RETRIES = 3  # 最大重试次数

# 任务结果过期时间（秒）
CELERY_RESULT_EXPIRES = 60 * 60 * 24  # 24 小时后过期

# Beat 定时任务配置
CELERY_BEAT_SCHEDULE = {
    'cleanup-old-thumbnails': {
        'task': 'apps.media.tasks.cleanup_old_thumbnails',
        'schedule': 60 * 60 * 24,  # 每天执行一次
        'args': (30,),  # 清理 30 天前的文件
    },
}

# ==================== 媒体文件传输配置 ====================

# 是否使用 Nginx X-Accel-Redirect 传输媒体文件
# - 开发环境：False（使用 Django FileResponse，已足够高效）
# - 生产环境：True（使用 Nginx 直接传输，零 Python 资源占用）
USE_NGINX_ACCEL_REDIRECT = os.getenv('USE_NGINX_ACCEL_REDIRECT', 'False') == 'True'

if USE_NGINX_ACCEL_REDIRECT and not DEBUG:
    print(f"\n✅ 已启用 Nginx X-Accel-Redirect 用于媒体文件传输")
elif DEBUG:
    print(f"\nℹ️  开发环境：使用 Django FileResponse 传输媒体文件")
