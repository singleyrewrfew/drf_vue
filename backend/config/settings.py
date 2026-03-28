"""
Django settings for config project.
"""

import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

# 项目根目录（backend/）
BASE_DIR = Path(__file__).resolve().parent.parent

# 当前环境：development 或 production
ENV = 'development'

# 加载对应环境的 .env 文件
env_file = BASE_DIR / f'.env.{ENV}'
if env_file.exists():
    load_dotenv(env_file)

# Django 安全密钥，用于加密签名
# 生产环境必须通过 DJANGO_SECRET_KEY 环境变量设置
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# 如果未设置 SECRET_KEY，根据环境决定行为
if not SECRET_KEY:
    if DEBUG:
        # 开发环境 fallback（仅本地开发使用）
        SECRET_KEY = 'dev-only-insecure-key-change-in-production'
        import warnings
        warnings.warn(
            "⚠️  WARNING: Using development SECRET_KEY. Set DJANGO_SECRET_KEY for production!",
            RuntimeWarning,
            stacklevel=2
        )
    else:
        # 生产环境未设置则启动失败
        from django.core.exceptions import ImproperlyConfigured
        raise ImproperlyConfigured(
            "DJANGO_SECRET_KEY environment variable is required for production deployment. "
            "Please set it in your .env file or environment variables."
        )

# 调试模式：默认关闭，开发环境需显式开启
DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'

# 如果开启 DEBUG 模式，添加安全警告
if DEBUG:
    import warnings
    warnings.warn(
        "⚠️  WARNING: DEBUG mode is enabled! This should never be used in production.",
        RuntimeWarning,
        stacklevel=2
    )
    # 限制允许的主机（开发环境可额外配置）
    ALLOWED_HOSTS = ['localhost', '127.0.0.1'] + \
                   os.getenv('DJANGO_DEBUG_ALLOWED_HOSTS', '').split(',')
else:
    # 生产环境使用环境变量配置
    ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',')

# 已安装的应用列表
INSTALLED_APPS = [
    'django.contrib.admin',              # Django 管理后台
    'apps.core',                        # 核心应用（必须在 django.contrib.auth 之前）
    'django.contrib.auth',               # Django 认证系统
    'django.contrib.contenttypes',        # 内容类型框架
    'django.contrib.sessions',             # 会话框架
    'django.contrib.messages',            # 消息框架
    'django.contrib.staticfiles',         # 静态文件管理
    'rest_framework',                   # Django REST Framework
    'rest_framework_simplejwt',          # JWT 认证
    'rest_framework_simplejwt.token_blacklist',  # JWT Token 黑名单
    'corsheaders',                      # CORS 跨域支持
    'drf_spectacular',                  # API 文档生成
    'apps.users',                       # 用户管理应用
    'apps.roles',                       # 角色管理应用
    'apps.contents',                     # 内容管理应用
    'apps.categories',                   # 分类管理应用
    'apps.tags',                        # 标签管理应用
    'apps.media',                       # 媒体管理应用
    'apps.comments',                     # 评论管理应用
]

# 中间件列表
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',        # 安全中间件
    'corsheaders.middleware.CorsMiddleware',             # CORS 中间件
    'django.contrib.sessions.middleware.SessionMiddleware',     # 会话中间件
    'django.middleware.common.CommonMiddleware',           # 通用中间件
    'django.middleware.csrf.CsrfViewMiddleware',         # CSRF 保护
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # 认证中间件
    'django.contrib.messages.middleware.MessageMiddleware',    # 消息中间件
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # 点击劫持保护
    'middleware.BackendAccessMiddleware.BackendAccessMiddleware',  # 自定义后台访问中间件
    'middleware.exception_handler.ExceptionHandlerMiddleware',  # 统一异常处理中间件（必须在最后）
]

# 根 URL 配置文件
ROOT_URLCONF = 'config.urls'

# 模板配置
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

# WSGI 应用配置
WSGI_APPLICATION = 'config.wsgi.application'

# 数据库配置
# 支持 SQLite/MySQL 动态切换，通过 DB_ENGINE 环境变量控制
DB_ENGINE = os.getenv('DB_ENGINE', 'django.db.backends.sqlite3')

if DB_ENGINE == 'django.db.backends.sqlite3':
    # SQLite 配置（开发环境默认）
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.getenv('SQLITE_DB_NAME', BASE_DIR / 'db.sqlite3'),
        }
    }
else:
    # MySQL/MariaDB 配置（生产环境推荐）
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

# 密码验证器
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 语言代码
LANGUAGE_CODE = 'zh-hans'

# 时区设置
TIME_ZONE = 'Asia/Shanghai'

# 启用国际化
USE_I18N = True

# 启用时区
USE_TZ = True

# 静态文件 URL 前缀
STATIC_URL = 'static/'

# 静态文件收集目录
STATIC_ROOT = BASE_DIR / 'staticfiles'

# 媒体文件 URL 前缀
MEDIA_URL = 'media/'

# 媒体文件存储目录
# 测试环境使用独立目录，避免与生产数据冲突
import sys
if 'pytest' in sys.modules:
    MEDIA_ROOT = BASE_DIR / 'media_test'
else:
    MEDIA_ROOT = BASE_DIR / 'media'

# 文件上传临时目录
UPLOAD_TEMP_DIR = os.getenv('UPLOAD_TEMP_DIR', MEDIA_ROOT / 'upload_temp')

# 默认自增主键类型
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 自定义用户模型（格式：app_label.ModelName）
# app_label 是应用的短标识，从 apps/ 目录名自动提取（去掉 apps 前缀）
# ModelName 是模型类名
AUTH_USER_MODEL = 'users.User'

# Django REST Framework 配置
REST_FRAMEWORK = {
    # 默认认证类
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    # 默认权限类
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    # 默认分页类
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 默认每页数量
    'PAGE_SIZE': 20,
    # 默认过滤后端
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter',
    ],
    # API 文档生成类
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    # 日期时间格式
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'DATE_FORMAT': '%Y-%m-%d',
}

# JWT 认证配置
SIMPLE_JWT = {
    # 访问令牌有效期
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
    # 刷新令牌有效期
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    # 刷新时轮换令牌
    'ROTATE_REFRESH_TOKENS': True,
    # 轮换后加入黑名单
    'BLACKLIST_AFTER_ROTATION': True,
    # 认证头类型
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# CORS 配置：始终使用白名单策略（不再使用 CORS_ALLOW_ALL_ORIGINS）
CORS_ALLOWED_ORIGINS = [
    origin.strip() 
    for origin in os.getenv('CORS_ALLOWED_ORIGINS', '').split(',') 
    if origin.strip()
]

# 开发环境可临时放宽（需显式配置）
if DEBUG and os.getenv('CORS_ALLOW_ALL_FOR_DEV', 'False') == 'True':
    CORS_ALLOW_ALL_ORIGINS = True
    print("⚠️  WARNING: CORS allows all origins for development!")

# CORS 配置：允许携带凭证
CORS_ALLOW_CREDENTIALS = True

# 额外的安全响应头
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# API 文档配置
SPECTACULAR_SETTINGS = {
    'TITLE': 'CMS API',
    'DESCRIPTION': '内容管理系统 API 文档',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# 文件上传配置
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
# FILE_UPLOAD_PERMISSIONS = 0o644 是 Django 为 Unix/Linux 系统设置上传文件默认权限的配置，含义为「所有者可读写，其他用户只读」，是安全的默认值。
FILE_UPLOAD_PERMISSIONS = 0o644
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB

# 允许的图片类型
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml']

# 允许的视频类型
ALLOWED_VIDEO_TYPES = ['video/mp4', 'video/webm', 'video/ogg', 'video/quicktime']

# 允许的文档类型
ALLOWED_DOCUMENT_TYPES = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']

# 所有允许的文件类型
ALLOWED_FILE_TYPES = ALLOWED_IMAGE_TYPES + ALLOWED_VIDEO_TYPES + ALLOWED_DOCUMENT_TYPES

# FFmpeg 配置：从环境变量读取路径
FFMPEG_PATH = os.getenv('FFMPEG_PATH', '')
FFMPEG_ADDITIONAL_PATHS = [
    p.strip() for p in os.getenv('FFMPEG_ADDITIONAL_PATHS', '').split(',') if p.strip()
]
