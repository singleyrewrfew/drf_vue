"""
Django 环境配置管理

使用 django-environ 集中管理环境变量，提供类型安全和默认值验证。

使用方法:
    from config.environments import BaseConfig, DevelopmentConfig, ProductionConfig
"""

import os
from pathlib import Path

import environ

# ==================== 初始化环境变量解析器 ====================

env = environ.Env(
    # 定义变量及其类型和默认值
    DEBUG=(bool, False),
    DJANGO_SECRET_KEY=(str, None),
    DJANGO_ENV=(str, 'development'),
    
    # 数据库配置
    DB_ENGINE=(str, 'django.db.backends.sqlite3'),
    DB_NAME=(str, ''),
    DB_USER=(str, ''),
    DB_PASSWORD=(str, ''),
    DB_HOST=(str, '127.0.0.1'),
    DB_PORT=(str, '3306'),
    SQLITE_DB_NAME=(str, ''),
    DB_CONN_MAX_AGE=(int, 0),
    DB_CONN_HEALTH_CHECKS=(bool, False),
    
    # Redis 配置
    REDIS_URL=(str, 'redis://127.0.0.1:6379/0'),
    REDIS_CACHE_URL=(str, 'redis://127.0.0.1:6379/1'),
    CACHE_KEY_PREFIX=(str, 'cms'),
    
    # Celery 配置
    CELERY_BROKER_URL=(str, 'redis://127.0.0.1:6379/2'),
    CELERY_RESULT_BACKEND=(str, 'redis://127.0.0.1:6379/3'),
    
    # JWT 配置
    JWT_ACCESS_TOKEN_LIFETIME=(int, 60),
    JWT_REFRESH_TOKEN_LIFETIME=(int, 1440),
    
    # CORS 配置
    DJANGO_DEBUG_ALLOWED_HOSTS=(list, []),
    DJANGO_ALLOWED_HOSTS=(list, []),
    
    # 日志配置
    LOG_LEVEL=(str, 'INFO'),
    LOG_DIR=(str, ''),
    
    # FFmpeg 配置
    FFMPEG_PATH=(str, ''),
    FFMPEG_ADDITIONAL_PATHS=(list, []),
    
    # Nginx 配置
    USE_NGINX_ACCEL_REDIRECT=(bool, False),
)

# ==================== 基础路径 ====================

BASE_DIR = Path(__file__).resolve().parent.parent

# 读取 .env 文件
ENVIRONMENT = env('DJANGO_ENV', default='development')
env_file = BASE_DIR / f'.env.{ENVIRONMENT}'
if env_file.exists():
    environ.Env.read_env(env_file)


class BaseConfig:
    """基础配置类 - 包含所有环境的通用配置"""
    
    # 安全配置
    SECRET_KEY = env('DJANGO_SECRET_KEY')
    DEBUG = env('DEBUG')
    
    # 允许的主机
    if DEBUG:
        ALLOWED_HOSTS = ['localhost', '127.0.0.1'] + env.list('DJANGO_DEBUG_ALLOWED_HOSTS', default=[])
    else:
        ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=[])
    
    # 应用配置
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
    
    ROOT_URLCONF = 'config.urls'
    WSGI_APPLICATION = 'config.wsgi.application'
    AUTH_USER_MODEL = 'users.User'
    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
    
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
    
    # 密码验证
    AUTH_PASSWORD_VALIDATORS = [
        {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
        {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
        {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
        {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
    ]
    
    # 国际化
    LANGUAGE_CODE = 'zh-hans'
    TIME_ZONE = 'Asia/Shanghai'
    USE_I18N = True
    USE_TZ = True
    
    # 静态文件
    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    
    # 媒体文件
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'
    
    # REST Framework 配置
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        ),
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticatedOrReadOnly',
        ),
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
        'PAGE_SIZE': 20,  # 默认每页数量
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
        ),
        'EXCEPTION_HANDLER': 'utils.exceptions.custom_exception_handler',
        'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
        # 时间格式配置
        'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',  # 日期时间格式：2026-04-26 02:44:15
        'DATE_FORMAT': '%Y-%m-%d',  # 日期格式：2026-04-26
        'TIME_FORMAT': '%H:%M:%S',  # 时间格式：02:44:15
    }
    
    # JWT 配置
    from datetime import timedelta
    SIMPLE_JWT = {
        'ACCESS_TOKEN_LIFETIME': timedelta(minutes=env.int('JWT_ACCESS_TOKEN_LIFETIME', default=60)),
        'REFRESH_TOKEN_LIFETIME': timedelta(minutes=env.int('JWT_REFRESH_TOKEN_LIFETIME', default=1440)),
        'ROTATE_REFRESH_TOKENS': True,
        'BLACKLIST_AFTER_ROTATION': True,
        'ALGORITHM': 'HS256',
        'SIGNING_KEY': SECRET_KEY,
        'AUTH_HEADER_TYPES': ('Bearer',),
    }
    
    # drf-spectacular 配置
    SPECTACULAR_SETTINGS = {
        'TITLE': 'CMS API',
        'DESCRIPTION': '内容管理系统 API 文档',
        'VERSION': '1.0.0',
        'SERVE_INCLUDE_SCHEMA': False,
    }
    
    # Celery 配置
    CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='redis://127.0.0.1:6379/2')
    CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND', default='redis://127.0.0.1:6379/3')
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = TIME_ZONE
    CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
    
    # ==================== 缓存配置 ====================
    # ⚠️  重要说明：
    # - Django Cache API (django.core.cache) 仅用于 Session 存储
    # - 业务缓存统一使用 utils.cache_utils（基于 redis-py）
    # - 新代码禁止使用 django.core.cache，应使用 cache_utils
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': env('REDIS_CACHE_URL', default='redis://localhost:6379/1'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }
    
    CACHE_KEY_PREFIX = env('CACHE_KEY_PREFIX', default='cms')
    REDIS_URL = env('REDIS_URL', default='redis://127.0.0.1:6379/1')
    
    # Session 使用 Redis 存储（性能优于数据库）
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
    SESSION_CACHE_ALIAS = 'default'
    
    # 缓存 TTL 配置
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
    
    # 缓存 TTL 配置
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
    
    # 文件上传配置
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
    
    # FFmpeg 配置
    FFMPEG_PATH = env('FFMPEG_PATH', default='')
    FFMPEG_ADDITIONAL_PATHS = env.list('FFMPEG_ADDITIONAL_PATHS', default=[])
    
    # Nginx X-Accel-Redirect
    USE_NGINX_ACCEL_REDIRECT = env.bool('USE_NGINX_ACCEL_REDIRECT', default=False)
    
    # 日志配置
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
                'filters': ['sensitive_data'],
            },
        },
        
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': True,
            },
            'django.request': {
                'handlers': ['console'],
                'level': 'WARNING',
                'propagate': False,
            },
            'django.db.backends': {
                'handlers': [],
                'level': 'WARNING',
                'propagate': False,
            },
            'apps': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
        
        'root': {
            'handlers': ['console'],
            'level': env('LOG_LEVEL', default='INFO'),
        },
    }


class DevelopmentConfig(BaseConfig):
    """开发环境配置"""
    
    DEBUG = True
    
    # 开发环境 fallback SECRET_KEY
    if not BaseConfig.SECRET_KEY:
        SECRET_KEY = 'dev-only-insecure-key-change-in-production'
    
    # 更宽松的 CORS 配置
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = [
        'http://localhost:5173',
        'http://127.0.0.1:5173',
    ]
    
    # 开发环境数据库（SQLite）
    DB_ENGINE = env('DB_ENGINE', default='django.db.backends.sqlite3')
    
    if DB_ENGINE == 'django.db.backends.sqlite3':
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': env('SQLITE_DB_NAME', default=str(BASE_DIR / 'db.sqlite3')),
                'TIMEOUT': 20,
            }
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': DB_ENGINE,
                'NAME': env('DB_NAME', default='cms_db'),
                'USER': env('DB_USER', default='root'),
                'PASSWORD': env('DB_PASSWORD', default=''),
                'HOST': env('DB_HOST', default='127.0.0.1'),
                'PORT': env('DB_PORT', default='3306'),
                'OPTIONS': {
                    'charset': 'utf8mb4',
                    'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                    'connect_timeout': 10,
                    'autocommit': True,
                },
                'CONN_MAX_AGE': env.int('DB_CONN_MAX_AGE', default=0),
                'CONN_HEALTH_CHECKS': env.bool('DB_CONN_HEALTH_CHECKS', default=False),
            }
        }
    
    # 确保日志目录存在
    log_dir = BASE_DIR / 'logs'
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"警告: 无法创建日志目录 {log_dir}: {e}")
    
    # 开发环境日志级别
    LOGGING = {
        **BaseConfig.LOGGING,
        'handlers': {
            **BaseConfig.LOGGING['handlers'],
            'file': {
                'level': 'DEBUG',
                'class': 'utils.log_handlers.SafeRotatingFileHandler',
                'filename': str(log_dir / 'django.log'),
                'maxBytes': 10 * 1024 * 1024,
                'backupCount': 5,
                'formatter': 'verbose',
                'encoding': 'utf-8',
                'filters': ['sensitive_data'],
            },
        },
        'loggers': {
            **BaseConfig.LOGGING['loggers'],
            'django': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': True,
            },
            'apps.media': {
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': False,
            },
        },
    }


class ProductionConfig(BaseConfig):
    """生产环境配置"""
    
    DEBUG = False
    
    # 生产环境强制要求 SECRET_KEY
    if not BaseConfig.SECRET_KEY:
        from django.core.exceptions import ImproperlyConfigured
        raise ImproperlyConfigured(
            "生产环境必须设置 DJANGO_SECRET_KEY 环境变量。"
        )
    
    # 严格的安全配置
    SECURE_SSL_REDIRECT = False  # 强制跳转 HTTPS
    SESSION_COOKIE_SECURE = False  # Cookie 仅 HTTPS 传输
    CSRF_COOKIE_SECURE = False
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    
    # 生产环境 CORS 配置
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[])
    
    # 生产环境数据库（MySQL）
    DATABASES = {
        'default': {
            'ENGINE': env('DB_ENGINE', default='django.db.backends.mysql'),
            'NAME': env('DB_NAME'),
            'USER': env('DB_USER'),
            'PASSWORD': env('DB_PASSWORD'),
            'HOST': env('DB_HOST'),
            'PORT': env('DB_PORT', default='3306'),
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                'connect_timeout': 10,
                'autocommit': True,
            },
            'CONN_MAX_AGE': env.int('DB_CONN_MAX_AGE', default=300),
            'CONN_HEALTH_CHECKS': env.bool('DB_CONN_HEALTH_CHECKS', default=True),
        }
    }
    
    # 确保日志目录存在
    log_dir_str = env('LOG_DIR', default=str(BASE_DIR / 'logs'))
    log_dir = Path(log_dir_str)
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"警告: 无法创建日志目录 {log_dir}: {e}")
    
    # 生产环境日志
    LOGGING = {
        **BaseConfig.LOGGING,
        'handlers': {
            **BaseConfig.LOGGING['handlers'],
            'file': {
                'level': 'WARNING',
                'class': 'utils.log_handlers.SafeRotatingFileHandler',
                'filename': str(log_dir / 'error.log'),
                'maxBytes': 10 * 1024 * 1024,
                'backupCount': 10,
                'formatter': 'verbose',
                'encoding': 'utf-8',
                'filters': ['sensitive_data'],
            },
            'django_file': {
                'level': 'INFO',
                'class': 'utils.log_handlers.SafeRotatingFileHandler',
                'filename': str(log_dir / 'django.log'),
                'maxBytes': 10 * 1024 * 1024,
                'backupCount': 5,
                'formatter': 'verbose',
                'encoding': 'utf-8',
                'filters': ['sensitive_data'],
            },
        },
        'loggers': {
            **BaseConfig.LOGGING['loggers'],
            'django': {
                'handlers': ['file', 'django_file'],
                'level': 'INFO',
                'propagate': True,
            },
            'apps.media': {
                'handlers': ['file', 'django_file'],
                'level': 'DEBUG',
                'propagate': False,
            },
        },
    }


# ==================== 配置映射 ====================

CONFIG_MAP = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}

# 根据环境变量选择配置
ConfigClass = CONFIG_MAP.get(ENVIRONMENT, DevelopmentConfig)
