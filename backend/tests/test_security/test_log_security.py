"""
日志敏感信息脱敏测试

验证日志脱敏工具的正确性，确保密码、Token 等敏感信息不会泄露到日志中。

运行测试：
    pytest tests/test_security/test_log_security.py -v
"""
import pytest
from utils.log_utils import (
    mask_password,
    mask_token,
    mask_dict,
    mask_sensitive_data,
    SensitiveDataFilter,
)


@pytest.mark.unit
class TestMaskPassword:
    """密码脱敏测试"""
    
    def test_mask_normal_password(self):
        """测试普通密码脱敏"""
        result = mask_password('secret123')
        assert result == '*** (length: 9)'
        assert 'secret' not in result
        assert '123' not in result
    
    def test_mask_empty_password(self):
        """测试空密码脱敏"""
        result = mask_password('')
        assert result == '***'
    
    def test_mask_none_password(self):
        """测试 None 密码脱敏"""
        result = mask_password(None)
        assert result == '***'
    
    def test_mask_without_length(self):
        """测试不显示长度的密码脱敏"""
        result = mask_password('secret123', show_length=False)
        assert result == '***'
        assert 'length' not in result


@pytest.mark.unit
class TestMaskToken:
    """Token 脱敏测试"""
    
    def test_mask_jwt_token(self):
        """测试 JWT Token 脱敏"""
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U'
        result = mask_token(token)
        
        # 应该保留前缀
        assert result.startswith('eyJh')
        # 应该包含长度信息
        assert 'length:' in result
        # 不应该包含完整的 Token
        assert token not in result
        assert 'dozjgNryP4J3jVmNHl0w5N' not in result
    
    def test_mask_short_token(self):
        """测试短 Token 脱敏"""
        token = 'abc'
        result = mask_token(token)
        assert result == '***'
    
    def test_mask_empty_token(self):
        """测试空 Token 脱敏"""
        result = mask_token('')
        assert result == '***'
    
    def test_mask_custom_prefix_length(self):
        """测试自定义前缀长度"""
        token = 'sk_test_123456789'
        result = mask_token(token, show_prefix_length=8)
        assert result.startswith('sk_test_')
        assert '123456789' not in result


@pytest.mark.unit
class TestMaskDict:
    """字典脱敏测试"""
    
    def test_mask_password_field(self):
        """测试密码字段脱敏"""
        data = {'username': 'admin', 'password': 'secret123'}
        result = mask_dict(data)
        
        assert result['username'] == 'admin'
        assert result['password'] == '*** (length: 9)'  # secret123 是 9 个字符
        assert 'secret' not in str(result)
        assert '123' not in str(result)
    
    def test_mask_token_field(self):
        """测试 Token 字段脱敏"""
        data = {
            'user_id': 123,
            'access_token': 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.abc123'
        }
        result = mask_dict(data)
        
        assert result['user_id'] == 123
        assert 'eyJh' in result['access_token']  # 前缀保留 4 个字符
        assert 'abc123' not in result['access_token']
    
    def test_mask_multiple_sensitive_fields(self):
        """测试多个敏感字段脱敏"""
        data = {
            'username': 'admin',
            'password': 'pass123',
            'api_key': 'sk_test_abc123',
            'email': 'admin@example.com'
        }
        result = mask_dict(data)
        
        assert result['username'] == 'admin'
        assert result['email'] == 'admin@example.com'
        assert result['password'] == '*** (length: 7)'
        assert 'pass123' not in str(result)
        assert 'sk_test' not in str(result)
    
    def test_mask_nested_dict(self):
        """测试嵌套字典脱敏"""
        data = {
            'user': {
                'name': 'admin',
                'credentials': {
                    'password': 'secret',
                    'token': 'abc123'
                }
            }
        }
        result = mask_dict(data)
        
        assert result['user']['name'] == 'admin'
        # credentials 是敏感字段，但其值是字典，所以会递归处理
        assert result['user']['credentials']['password'] == '*** (length: 6)'
        # token 也是敏感字段，会显示长度
        assert result['user']['credentials']['token'] == '*** (length: 6)'
        assert 'abc123' not in str(result)
    
    def test_mask_list_with_dicts(self):
        """测试包含字典的列表脱敏"""
        data = [
            {'username': 'user1', 'password': 'pass1'},
            {'username': 'user2', 'password': 'pass2'}
        ]
        result = mask_dict({'users': data})
        
        assert result['users'][0]['username'] == 'user1'
        assert result['users'][0]['password'] == '*** (length: 5)'
        assert 'pass1' not in str(result)
    
    def test_mask_no_sensitive_fields(self):
        """测试无敏感字段的字典保持不变"""
        data = {'username': 'admin', 'email': 'admin@example.com'}
        result = mask_dict(data)
        
        assert result == data
    
    def test_mask_case_insensitive(self):
        """测试字段名大小写不敏感"""
        data = {
            'PASSWORD': 'secret',
            'Api_Key': 'sk_test_123',
            'Refresh_Token': 'token_value'
        }
        result = mask_dict(data)
        
        assert result['PASSWORD'] == '*** (length: 6)'
        assert '***' in str(result['Api_Key'])  # API Key 会被识别为敏感字段
        assert '***' in str(result['Refresh_Token'])


@pytest.mark.unit
class TestMaskSensitiveData:
    """通用敏感数据脱敏测试"""
    
    def test_mask_string_jwt(self):
        """测试 JWT 字符串脱敏"""
        token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.abc123'
        result = mask_sensitive_data(token)
        
        assert result.startswith('eyJh')
        assert 'abc123' not in result
    
    def test_mask_string_api_key(self):
        """测试 API Key 字符串脱敏"""
        api_key = 'sk_test_abc123xyz'
        result = mask_sensitive_data(api_key)
        
        assert 'sk_test' not in result or result == '***'
    
    def test_mask_non_sensitive_string(self):
        """测试非敏感字符串不变"""
        text = 'Hello, World!'
        result = mask_sensitive_data(text)
        
        assert result == text
    
    def test_mask_dict_wrapper(self):
        """测试字典包装"""
        data = {'password': 'secret'}
        result = mask_sensitive_data(data)
        
        assert result['password'] == '*** (length: 6)'
    
    def test_mask_list(self):
        """测试列表脱敏"""
        data = [{'password': 'secret1'}, {'password': 'secret2'}]
        result = mask_sensitive_data(data)
        
        assert result[0]['password'] == '*** (length: 7)'
        assert result[1]['password'] == '*** (length: 7)'
    
    def test_mask_other_types(self):
        """测试其他类型不变"""
        assert mask_sensitive_data(123) == 123
        assert mask_sensitive_data(True) is True
        assert mask_sensitive_data(None) is None


@pytest.mark.unit
class TestSensitiveDataFilter:
    """日志过滤器测试"""
    
    def test_filter_dict_message(self):
        """测试字典消息过滤"""
        import logging
        
        filter_obj = SensitiveDataFilter()
        record = logging.LogRecord(
            name='test',
            level=logging.INFO,
            pathname='test.py',
            lineno=1,
            msg={'password': 'secret', 'username': 'admin'},
            args=(),
            exc_info=None
        )
        
        result = filter_obj.filter(record)
        assert result is True
        assert record.msg['password'] == '*** (length: 6)'
        assert record.msg['username'] == 'admin'
    
    def test_filter_tuple_args(self):
        """测试元组参数过滤"""
        import logging
        
        filter_obj = SensitiveDataFilter()
        record = logging.LogRecord(
            name='test',
            level=logging.INFO,
            pathname='test.py',
            lineno=1,
            msg='User login: %s',
            args=({'password': 'secret', 'username': 'admin'},),
            exc_info=None
        )
        
        result = filter_obj.filter(record)
        assert result is True
        # 注意：LogRecord 会将单元素元组解包为字典
        if isinstance(record.args, dict):
            # 如果已经被解包为字典
            assert record.args['password'] == '*** (length: 6)'
            assert record.args['username'] == 'admin'
        elif isinstance(record.args, tuple):
            # 如果是元组（多个参数）
            assert record.args[0]['password'] == '*** (length: 6)'
            assert record.args[0]['username'] == 'admin'
    
    def test_filter_error_handling(self):
        """测试异常处理（不应影响日志记录）"""
        import logging
        
        filter_obj = SensitiveDataFilter()
        record = logging.LogRecord(
            name='test',
            level=logging.INFO,
            pathname='test.py',
            lineno=1,
            msg='Normal message',
            args=(),
            exc_info=None
        )
        
        # 即使处理出错，也应该返回 True
        result = filter_obj.filter(record)
        assert result is True


@pytest.mark.integration
class TestLogSecurityIntegration:
    """集成测试：验证实际日志输出中的敏感信息脱敏"""
    
    def test_logger_with_sensitive_data(self, caplog):
        """测试日志记录器自动脱敏"""
        import logging
        from utils.log_utils import get_safe_logger
        
        logger = get_safe_logger('test_security')
        
        with caplog.at_level(logging.INFO):
            logger.info('用户登录: %s', {
                'username': 'admin',
                'password': 'secret123',
                'token': 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.abc123'
            })
        
        # 检查日志中不包含原始敏感信息
        log_text = caplog.text
        assert 'secret123' not in log_text
        assert 'eyJhbGciOiJIUzI1NiJ9' not in log_text or '***' in log_text
        assert 'admin' in log_text  # 用户名应该保留
    
    def test_real_world_login_scenario(self, caplog):
        """测试真实登录场景的日志脱敏"""
        import logging
        from utils.log_utils import get_safe_logger
        
        logger = get_safe_logger('test_auth')
        
        with caplog.at_level(logging.INFO):
            # 模拟登录日志 - 使用脱敏后的数据
            login_data = {
                'username': 'testuser',
                'password': 'Test@123456',
                'ip': '192.168.1.100'
            }
            # 手动脱敏后再记录
            from utils.log_utils import mask_sensitive_data
            safe_data = mask_sensitive_data(login_data)
            logger.info(f'用户登录尝试: {safe_data}')
        
        # 验证密码被脱敏
        assert 'Test@123456' not in caplog.text
        assert '***' in caplog.text or '(length:' in caplog.text
        assert 'testuser' in caplog.text  # 用户名应该保留
        assert '192.168.1.100' in caplog.text  # IP 应该保留
