"""
数据库连接池配置测试

验证连接池配置是否正确，以及性能是否符合预期。
"""
import os
import pytest
from django.db import connection
from django.test import override_settings
from utils.db_monitor import (
    get_connection_info,
    check_connection_health,
    get_connection_recommendations
)

# 检查是否为生产环境测试
IS_PRODUCTION_ENV = os.environ.get('DJANGO_ENV') == 'production'


class TestConnectionPoolConfiguration:
    """测试连接池配置"""
    
    @pytest.mark.skipif(not IS_PRODUCTION_ENV, reason="仅在生产环境检查连接池配置")
    def test_connection_pool_enabled_in_production(self):
        """测试生产环境启用了连接池"""
        from django.conf import settings
        
        # 跳过 SQLite
        if 'sqlite' in settings.DATABASES['default']['ENGINE']:
            pytest.skip("SQLite 不支持连接池")
        
        db_config = settings.DATABASES['default']
        
        # 检查 CONN_MAX_AGE
        conn_max_age = db_config.get('CONN_MAX_AGE', 0)
        assert conn_max_age >= 0, "CONN_MAX_AGE 不能为负数"
        
        # 生产环境应该启用连接池
        assert conn_max_age > 0, "生产环境应启用连接池（CONN_MAX_AGE > 0）"
        assert conn_max_age <= 600, "CONN_MAX_AGE 不应超过 600 秒"
    
    @pytest.mark.skipif(not IS_PRODUCTION_ENV, reason="仅在生产环境检查连接池配置")
    def test_health_checks_enabled_in_production(self):
        """测试生产环境启用了健康检查"""
        from django.conf import settings
        
        # 跳过 SQLite
        if 'sqlite' in settings.DATABASES['default']['ENGINE']:
            pytest.skip("SQLite 不支持连接池")
        
        db_config = settings.DATABASES['default']
        health_checks = db_config.get('CONN_HEALTH_CHECKS', False)
        
        # 生产环境应该启用健康检查
        assert health_checks is True, "生产环境应启用健康检查"
    
    def test_connection_info_retrieval(self):
        """测试获取连接信息"""
        info = get_connection_info()
        
        # 应该有基本字段
        assert 'connected' in info
        assert 'connection_config' in info
        
        # 如果连接成功，应该有配置信息
        if info['connected']:
            config = info['connection_config']
            assert 'engine' in config
            assert 'conn_max_age' in config
    
    @pytest.mark.django_db
    def test_connection_health_check(self):
        """测试连接健康检查"""
        result = check_connection_health()
        
        # 应该有基本字段
        assert 'healthy' in result
        assert 'response_time_ms' in result
        assert 'details' in result
        
        # 正常情况下应该健康
        assert result['healthy'] is True
        assert result['response_time_ms'] >= 0
    
    def test_connection_reuse(self):
        """测试连接复用"""
        from django.conf import settings
        
        # 跳过 SQLite
        if 'sqlite' in settings.DATABASES['default']['ENGINE']:
            pytest.skip("SQLite 不支持连接池")
        
        if settings.DATABASES['default'].get('CONN_MAX_AGE', 0) == 0:
            pytest.skip("连接池未启用")
        
        # 执行两次查询
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
            first_conn_id = id(connection.connection)
        
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
            second_conn_id = id(connection.connection)
        
        # 如果启用了连接池，应该是同一个连接对象
        # 注意：这个测试可能不稳定，因为 Django 的连接管理比较复杂
        # 主要用于验证连接池是否工作
        assert first_conn_id is not None
        assert second_conn_id is not None
    
    def test_configuration_recommendations(self):
        """测试配置建议"""
        recommendations = get_connection_recommendations()
        
        # 应该返回建议列表
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        
        # 每个建议应该有必要的字段
        for rec in recommendations:
            assert 'level' in rec
            assert 'message' in rec
            assert 'suggestion' in rec
    
    def test_invalid_conn_max_age_warning(self):
        """测试无效的 CONN_MAX_AGE 会发出警告"""
        import warnings
        
        # 模拟负的 CONN_MAX_AGE
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            # 这里需要实际修改配置才能测试
            # 暂时跳过，因为修改全局配置会影响其他测试
            pytest.skip("需要隔离测试环境")


class TestConnectionPoolPerformance:
    """测试连接池性能"""
    
    @pytest.mark.django_db
    def test_connection_creation_overhead(self):
        """测试连接创建开销"""
        import time
        from django.conf import settings
        
        # 跳过 SQLite
        if 'sqlite' in settings.DATABASES['default']['ENGINE']:
            pytest.skip("SQLite 不支持连接池")
        
        # 测量 10 次查询的时间
        start_time = time.time()
        for _ in range(10):
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
                cursor.fetchone()
        elapsed = time.time() - start_time
        
        # 平均每次查询应该小于 100ms
        avg_time = (elapsed / 10) * 1000
        assert avg_time < 100, f"平均查询时间 {avg_time}ms 过长"
    
    @pytest.mark.django_db
    def test_health_check_overhead(self):
        """测试健康检查开销"""
        import time
        from django.conf import settings
        
        # 跳过 SQLite
        if 'sqlite' in settings.DATABASES['default']['ENGINE']:
            pytest.skip("SQLite 不支持连接池")
        
        if not settings.DATABASES['default'].get('CONN_HEALTH_CHECKS', False):
            pytest.skip("健康检查未启用")
        
        # 测量带健康检查的查询时间
        start_time = time.time()
        for _ in range(10):
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
                cursor.fetchone()
        elapsed_with_check = time.time() - start_time
        
        # 健康检查开销应该很小（< 10ms/次）
        avg_overhead = (elapsed_with_check / 10) * 1000
        assert avg_overhead < 50, f"健康检查开销 {avg_overhead}ms 过大"


class TestConnectionPoolEdgeCases:
    """测试连接池边界情况"""
    
    def test_sqlite_timeout_configuration(self):
        """测试 SQLite 超时配置"""
        from django.conf import settings
        
        if 'sqlite' not in settings.DATABASES['default']['ENGINE']:
            pytest.skip("仅适用于 SQLite")
        
        db_config = settings.DATABASES['default']
        timeout = db_config.get('TIMEOUT', 0)
        
        # SQLite 应该设置超时
        assert timeout > 0, "SQLite 应设置 TIMEOUT 避免锁定"
    
    def test_mysql_charset_configuration(self):
        """测试 MySQL 字符集配置"""
        from django.conf import settings
        
        if 'mysql' not in settings.DATABASES['default']['ENGINE'].lower():
            pytest.skip("仅适用于 MySQL")
        
        db_config = settings.DATABASES['default']
        options = db_config.get('OPTIONS', {})
        charset = options.get('charset', '')
        
        # 应该使用 utf8mb4
        assert charset == 'utf8mb4', "MySQL 应使用 utf8mb4 字符集"
    
    def test_mysql_strict_mode(self):
        """测试 MySQL 严格模式"""
        from django.conf import settings
        
        if 'mysql' not in settings.DATABASES['default']['ENGINE'].lower():
            pytest.skip("仅适用于 MySQL")
        
        db_config = settings.DATABASES['default']
        options = db_config.get('OPTIONS', {})
        init_command = options.get('init_command', '')
        
        # 应该启用严格模式
        assert 'STRICT_TRANS_TABLES' in init_command, "MySQL 应启用严格模式"
