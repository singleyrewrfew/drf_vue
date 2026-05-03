"""
Django Settings - 简化版

所有配置已迁移到 config.environments 模块，
此文件仅用于加载和验证配置。
"""

from config.environments import ConfigClass, ENVIRONMENT

# ==================== 应用配置 ====================

# 动态应用配置类的所有大写属性
for attr in dir(ConfigClass):
    if attr.isupper():
        globals()[attr] = getattr(ConfigClass, attr)

# ==================== 配置验证 ====================

def validate_config():
    """验证关键配置是否正确设置"""
    import warnings
    
    # SECRET_KEY 验证
    if not ConfigClass.SECRET_KEY:
        raise ValueError("SECRET_KEY 未设置")
    
    # DEBUG 模式警告
    if ConfigClass.DEBUG and __name__ == '__main__':
        warnings.warn(
            "⚠️  WARNING: DEBUG 模式已启用！切勿在生产环境中使用。",
            RuntimeWarning,
            stacklevel=2
        )
    
    # 数据库配置验证
    if hasattr(ConfigClass, 'DATABASES'):
        db_config = ConfigClass.DATABASES.get('default', {})
        engine = db_config.get('ENGINE', '')
        
        if 'mysql' in engine.lower() or 'postgresql' in engine.lower():
            # 生产环境数据库必须有密码
            if not ConfigClass.DEBUG and not db_config.get('PASSWORD'):
                raise ValueError("生产环境数据库必须设置密码")

# 执行配置验证
validate_config()

# 打印环境信息（仅在启动时）
import os
import sys
if os.environ.get('RUN_MAIN') != 'true' or 'gunicorn' in sys.argv:
    print(f"\n📋 Django 环境配置:")
    print(f"   - 环境: {ENVIRONMENT}")
    print(f"   - DEBUG: {ConfigClass.DEBUG}")
    print(f"   - 数据库引擎: {ConfigClass.DATABASES['default']['ENGINE']}")
    if hasattr(ConfigClass, 'CACHES'):
        print(f"   - 缓存后端: {ConfigClass.CACHES['default']['BACKEND']}")
    print()
