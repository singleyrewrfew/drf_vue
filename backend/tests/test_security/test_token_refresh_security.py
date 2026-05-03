"""
JWT Token 刷新安全测试

测试 Token 刷新机制的安全性，包括：
1. Refresh Token 轮换机制
2. 旧 Token 黑名单验证
3. 用户状态检查
4. 刷新频率限制
5. 重放攻击防护
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
from utils.error_codes import ErrorTypes

User = get_user_model()


class TestTokenRefreshSecurity:
    """Token 刷新安全测试"""
    
    @pytest.fixture
    def api_client(self):
        """创建 API 客户端"""
        return APIClient()
    
    @pytest.fixture
    def user(self, db):
        """创建测试用户"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
        return user
    
    @pytest.fixture
    def refresh_token(self, user):
        """创建 Refresh Token"""
        return RefreshToken.for_user(user)
    
    def test_refresh_token_rotation(self, api_client, refresh_token):
        """测试 Refresh Token 轮换机制"""
        response = api_client.post('/api/auth/refresh/', {
            'refresh': str(refresh_token)
        })
        
        assert response.status_code == 200
        response_data = response.json()
        
        # StandardResponse 格式：{'message': '...', 'data': {...}}
        data = response_data.get('data', response_data)
        
        # 应该返回新的 access token
        assert 'access' in data
        assert data['access'] != str(refresh_token.access_token)
        
        # 如果启用了轮换，应该返回新的 refresh token
        if 'refresh' in data:
            assert data['refresh'] != str(refresh_token)
    
    def test_old_refresh_token_blacklisted(self, api_client, refresh_token):
        """测试旧 Refresh Token 被加入黑名单（防止重放攻击）"""
        # 第一次刷新 - 应该成功
        response1 = api_client.post('/api/auth/refresh/', {
            'refresh': str(refresh_token)
        })
        assert response1.status_code == 200
        
        # 第二次使用同一个 refresh token - 应该失败（已被加入黑名单）
        response2 = api_client.post('/api/auth/refresh/', {
            'refresh': str(refresh_token)
        })
        
        # 401 表示 token 无效（已被加入黑名单）
        assert response2.status_code == 401
    
    def test_inactive_user_cannot_refresh(self, api_client, user, refresh_token):
        """测试禁用的用户不能刷新 Token"""
        # 禁用用户
        user.is_active = False
        user.save()
        
        # 尝试刷新
        response = api_client.post('/api/auth/refresh/', {
            'refresh': str(refresh_token)
        })
        
        # 应该返回 403 Forbidden
        assert response.status_code == 403
        response_data = response.json()
        # 响应格式：{'message': '...', 'error': 'forbidden', 'data': null}
        assert response_data.get('error') == 'forbidden'
    
    def test_refresh_rate_limiting(self, api_client, refresh_token, user):
        """测试刷新频率限制"""
        # 清除之前的缓存
        cache.clear()
        
        # 快速连续刷新 6 次（超过限制的 5 次/分钟）
        responses = []
        current_refresh = str(refresh_token)
        
        for i in range(6):
            response = api_client.post('/api/auth/refresh/', {
                'refresh': current_refresh
            })
            responses.append(response)
            
            # 每次刷新后获取新的 refresh token（如果返回了）
            if response.status_code == 200:
                response_data = response.json()
                data = response_data.get('data', response_data)
                if 'refresh' in data:
                    current_refresh = data['refresh']
        
        # 前 5 次应该成功，第 6 次应该被限流
        success_count = sum(1 for r in responses if r.status_code == 200)
        rate_limited_count = sum(1 for r in responses if r.status_code == 429)
        
        assert success_count <= 5, f"成功次数 {success_count} 超过了限制 5"
        assert rate_limited_count >= 1, "应该至少有一次被限流"
    
    def test_invalid_refresh_token(self, api_client):
        """测试无效的 Refresh Token"""
        # 使用伪造的 token
        response = api_client.post('/api/auth/refresh/', {
            'refresh': 'invalid.token.here'
        })
        
        assert response.status_code == 401
        # 注意：由于 DRF 默认异常处理，返回的格式可能不同
        data = response.json()
        # 检查是否包含认证相关的错误信息
        assert 'error' in data or 'detail' in data
    
    def test_missing_refresh_token(self, api_client):
        """测试缺少 Refresh Token"""
        response = api_client.post('/api/auth/refresh/', {})
        
        # 由于我们的实现会先检查 refresh 字段，应该返回 400
        # 但如果被 DRF 拦截，可能返回 401
        assert response.status_code in [400, 401]
        data = response.json()
        # 检查是否有错误信息
        assert 'message' in data or 'detail' in data or 'error' in data
    
    def test_expired_refresh_token(self, api_client, user):
        """测试过期的 Refresh Token"""
        from datetime import timedelta
        from django.utils import timezone
        
        # 创建一个已过期的 token
        refresh = RefreshToken.for_user(user)
        refresh.set_exp(lifetime=timedelta(seconds=-1))  # 设置为已过期
        
        response = api_client.post('/api/auth/refresh/', {
            'refresh': str(refresh)
        })
        
        assert response.status_code == 401
    
    def test_deleted_user_cannot_refresh(self, api_client, user, refresh_token):
        """测试已删除用户的 Token 不能刷新"""
        # 删除用户
        user_id = user.id
        user.delete()
        
        # 尝试使用已删除用户的 token 刷新
        response = api_client.post('/api/auth/refresh/', {
            'refresh': str(refresh_token)
        })
        
        # 应该返回 401（用户不存在）
        assert response.status_code == 401
    
    def test_refresh_logging(self, api_client, refresh_token, caplog):
        """测试刷新操作有日志记录"""
        import logging
        
        with caplog.at_level(logging.INFO):
            response = api_client.post('/api/auth/refresh/', {
                'refresh': str(refresh_token)
            })
        
        assert response.status_code == 200
        
        # 检查是否有成功刷新的日志
        log_messages = [record.message for record in caplog.records]
        assert any('Token 刷新成功' in msg for msg in log_messages), \
            "应该记录 Token 刷新成功的日志"
    
    def test_concurrent_refresh_requests(self, api_client, user):
        """测试并发刷新请求的处理"""
        import concurrent.futures
        
        refresh = RefreshToken.for_user(user)
        
        def refresh_token_task(token_str):
            response = api_client.post('/api/auth/refresh/', {
                'refresh': token_str
            })
            return response.status_code
        
        # 模拟 3 个并发请求
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [
                executor.submit(refresh_token_task, str(refresh))
                for _ in range(3)
            ]
            results = [f.result() for f in futures]
        
        # 只有第一个请求应该成功，其他的应该失败（token 已被轮换）
        success_count = results.count(200)
        assert success_count <= 1, f"并发刷新中成功次数 {success_count} 应该 <= 1"


class TestTokenRefreshIntegration:
    """Token 刷新集成测试"""
    
    @pytest.fixture
    def api_client(self):
        """创建 API 客户端"""
        return APIClient()
    
    @pytest.fixture
    def authenticated_client(self, api_client, db):
        """创建已认证的客户端"""
        from apps.roles.models import Role
        
        # 确保存在 editor 角色
        role, _ = Role.objects.get_or_create(
            code='editor',
            defaults={'name': '编辑者'}
        )
        
        user = User.objects.create_user(
            username='integration_test_user',
            email='integration@test.com',
            password='TestPass123!'
        )
        user.roles.add(role)
        
        refresh = RefreshToken.for_user(user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        return api_client, user, refresh
    
    def test_full_refresh_workflow(self, api_client, db):
        """测试完整的 Token 刷新工作流程"""
        from apps.roles.models import Role
        
        # 确保存在 editor 角色
        role, _ = Role.objects.get_or_create(
            code='editor',
            defaults={'name': '编辑者'}
        )
        
        # 1. 创建用户并登录
        user = User.objects.create_user(
            username='workflow_user',
            email='workflow@test.com',
            password='TestPass123!'
        )
        user.role = role  # 使用 role 而不是 roles
        user.save()
        
        # 2. 获取初始 token
        refresh = RefreshToken.for_user(user)
        old_access = str(refresh.access_token)
        old_refresh = str(refresh)
        
        # 3. 刷新 token
        response = api_client.post('/api/auth/refresh/', {
            'refresh': old_refresh
        })
        
        assert response.status_code == 200
        response_data = response.json()
        data = response_data.get('data', response_data)
        
        new_access = data['access']
        new_refresh = data.get('refresh')
        
        # 4. 验证新 token 不同
        assert new_access != old_access
        if new_refresh:
            assert new_refresh != old_refresh
        
        # 5. 使用新 access token 访问受保护的资源
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {new_access}')
        response = api_client.get('/api/auth/profile/')
        
        # 应该成功（200）而不是未授权（401）
        assert response.status_code == 200
