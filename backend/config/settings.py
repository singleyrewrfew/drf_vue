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
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': DB_ENGINE,
            'NAME': os.getenv('DB_NAME', 'cms_db'),
            'USER': os.getenv('DB_USER', 'root'),
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '3306'),
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
            'CONN_MAX_AGE': int(os.getenv('DB_CONN_MAX_AGE', '0')),
            'CONN_HEALTH_CHECKS': os.getenv('DB_CONN_HEALTH_CHECKS', 'True') == 'True',
        }
    }

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
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
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

# 确保日志目录存在
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    
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
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'django.log',
            'maxBytes': 10 * 1024 * 1024,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
            'encoding': 'utf-8'
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'error.log',
            'maxBytes': 10 * 1024 * 1024,  # 10MB
            'backupCount': 10,
            'formatter': 'verbose',
            'encoding': 'utf-8'
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
            'handlers': ['console'] if DEBUG else [],
            'level': 'DEBUG' if DEBUG else 'WARNING',  # 仅开发环境打印 SQL
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
