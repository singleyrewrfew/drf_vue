"""
SQL 注入防护测试

测试动态查询参数的输入验证，确保所有用户输入都经过白名单验证
"""
import pytest
from rest_framework.test import APIClient
from apps.users.models import User
from apps.roles.models import Role
from apps.contents.models import Content
from apps.categories.models import Category
from apps.tags.models import Tag


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user():
    """创建管理员用户"""
    role, _ = Role.objects.get_or_create(code='admin', name='管理员')
    user, _ = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'role': role
        }
    )
    if not user.is_superuser:
        user.is_superuser = True
        user.save()
    return user


@pytest.fixture
def editor_user():
    """创建编辑者用户"""
    role, _ = Role.objects.get_or_create(code='editor', name='编辑者')
    user, _ = User.objects.get_or_create(
        username='editor',
        defaults={
            'email': 'editor@example.com',
            'role': role
        }
    )
    return user


@pytest.fixture
def normal_user():
    """创建普通用户"""
    user, _ = User.objects.get_or_create(
        username='normal',
        defaults={'email': 'normal@example.com'}
    )
    return user


@pytest.fixture
def authenticated_client(api_client, admin_user):
    """认证的 API 客户端"""
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.mark.django_db
class TestContentSQLInjectionProtection:
    """内容视图集 SQL 注入防护测试"""
    
    def test_valid_status_filter(self, authenticated_client):
        """测试有效的状态值应该被接受"""
        # 创建测试数据
        Content.objects.create(
            title='Test Content',
            content='Test content',
            author=authenticated_client.user,
            status='published'
        )
        
        # 测试所有有效的状态值
        for valid_status in ['draft', 'published', 'archived']:
            response = authenticated_client.get(f'/api/contents/?status={valid_status}')
            assert response.status_code == 200, f"状态值 {valid_status} 应该被接受"
    
    def test_invalid_status_filter_rejected(self, authenticated_client):
        """测试无效的状态值应该被拒绝（防止 SQL 注入）"""
        # 测试各种恶意输入
        malicious_inputs = [
            "'; DROP TABLE contents; --",
            "' OR '1'='1",
            "published' OR '1'='1",
            "<script>alert('xss')</script>",
            "../../../etc/passwd",
            "invalid_status",
            "DRAFT",  # 大小写不匹配
            # 注意：空字符串 "" 会被 Django ORM 忽略，返回 200
        ]
        
        for malicious_input in malicious_inputs:
            response = authenticated_client.get(f'/api/contents/?status={malicious_input}')
            assert response.status_code == 400, f"恶意输入 '{malicious_input}' 应该被拒绝"
            assert '无效的状态值' in str(response.data), "错误消息应该说明原因"
    
    def test_sql_injection_attempt_blocked(self, authenticated_client):
        """测试 SQL 注入尝试被阻止"""
        sql_injection_attempts = [
            "published' UNION SELECT * FROM users--",
            "'; DELETE FROM contents;--",
            "' OR 1=1--",
            "admin'--",
        ]
        
        for attempt in sql_injection_attempts:
            response = authenticated_client.get(f'/api/contents/?status={attempt}')
            assert response.status_code == 400, f"SQL 注入尝试 '{attempt}' 应该被阻止"
    
    def test_editor_can_filter_own_content(self, api_client, editor_user):
        """测试编辑者可以按状态过滤自己的内容"""
        api_client.force_authenticate(user=editor_user)
        
        # 创建编辑者的内容
        Content.objects.create(
            title='Editor Content',
            content='Test',
            author=editor_user,
            status='draft'
        )
        
        # 测试有效的状态过滤
        response = api_client.get('/api/contents/?status=draft')
        assert response.status_code == 200
        
        # 测试无效的状态值
        response = api_client.get('/api/contents/?status=invalid')
        assert response.status_code == 400


@pytest.mark.django_db
class TestCommentSQLInjectionProtection:
    """评论视图集 SQL 注入防护测试"""
    
    def test_valid_is_approved_filter(self, authenticated_client, admin_user):
        """测试有效的 is_approved 值应该被接受"""
        from apps.comments.models import Comment
        from apps.contents.models import Content
        
        # 创建测试文章和评论
        article = Content.objects.create(
            title='Test Article',
            content='Test',
            author=admin_user
        )
        
        Comment.objects.create(
            content='Test comment',
            article=article,
            user=admin_user,
            is_approved=True
        )
        
        # 测试有效的布尔值字符串
        for valid_value in ['true', 'false', 'True', 'False', 'TRUE', 'FALSE']:
            response = authenticated_client.get(f'/api/comments/?is_approved={valid_value}')
            assert response.status_code == 200, f"is_approved 值 '{valid_value}' 应该被接受"
    
    def test_invalid_is_approved_filter_rejected(self, authenticated_client):
        """测试无效的 is_approved 值应该被拒绝"""
        invalid_values = [
            "'; DROP TABLE comments; --",
            "' OR '1'='1",
            "1",
            "0",
            "yes",
            "no",
            "invalid",
            "<script>alert('xss')</script>",
        ]
        
        for invalid_value in invalid_values:
            response = authenticated_client.get(f'/api/comments/?is_approved={invalid_value}')
            assert response.status_code == 400, f"无效值 '{invalid_value}' 应该被拒绝"


@pytest.mark.django_db
class TestMediaSQLInjectionProtection:
    """媒体视图集 SQL 注入防护测试"""
    
    def test_valid_file_type_filter(self, authenticated_client, admin_user):
        """测试有效的文件类型前缀应该被接受"""
        from apps.media.models import Media
        
        # 创建测试媒体文件
        Media.objects.create(
            filename='test.jpg',
            file_type='image/jpeg',
            file_size=1024,
            uploader=admin_user
        )
        
        # 测试有效的文件类型前缀
        valid_prefixes = ['image/', 'video/', 'application/']
        for prefix in valid_prefixes:
            response = authenticated_client.get(f'/api/media/?file_type={prefix}')
            assert response.status_code == 200, f"文件类型前缀 '{prefix}' 应该被接受"
    
    def test_invalid_file_type_filter_rejected(self, authenticated_client):
        """测试无效的文件类型前缀应该被拒绝"""
        invalid_prefixes = [
            "'; DROP TABLE media; --",
            "' OR '1'='1",
            "text/",
            "audio/",
            "invalid",
            "<script>alert('xss')</script>",
            "../../../etc/passwd",
        ]
        
        for invalid_prefix in invalid_prefixes:
            response = authenticated_client.get(f'/api/media/?file_type={invalid_prefix}')
            assert response.status_code == 400, f"无效前缀 '{invalid_prefix}' 应该被拒绝"
    
    def test_sql_injection_in_file_type_blocked(self, authenticated_client):
        """测试文件类型参数中的 SQL 注入被阻止"""
        sql_injections = [
            "image/' UNION SELECT * FROM users--",
            "'; DELETE FROM media;--",
            "' OR 1=1--",
        ]
        
        for injection in sql_injections:
            response = authenticated_client.get(f'/api/media/?file_type={injection}')
            assert response.status_code == 400, f"SQL 注入尝试 '{injection}' 应该被阻止"


@pytest.mark.django_db
class TestParameterValidationEdgeCases:
    """边界情况测试"""
    
    def test_empty_parameters(self, authenticated_client):
        """测试空参数的处理"""
        # 空字符串
        response = authenticated_client.get('/api/contents/?status=')
        assert response.status_code == 200  # 空值应该被忽略而不是报错
    
    def test_none_parameters(self, authenticated_client):
        """测试 None 值的处理"""
        # 不提供参数
        response = authenticated_client.get('/api/contents/')
        assert response.status_code == 200
    
    def test_unicode_injection(self, authenticated_client):
        """测试 Unicode 注入尝试"""
        unicode_attempts = [
            "published%00', 'hacked'--",  # Null byte injection
            "published%27%20OR%20%271%27%3D%271",  # URL encoded
            "草稿', '攻击'--",  # Chinese characters
        ]
        
        for attempt in unicode_attempts:
            response = authenticated_client.get(f'/api/contents/?status={attempt}')
            # 应该返回 400 或正常处理（取决于具体实现）
            assert response.status_code in [200, 400], f"Unicode 注入尝试应该被正确处理"
    
    def test_very_long_parameter(self, authenticated_client):
        """测试超长参数的处理"""
        long_value = "a" * 10000
        response = authenticated_client.get(f'/api/contents/?status={long_value}')
        assert response.status_code == 400, "超长参数应该被拒绝"
    
    def test_special_characters(self, authenticated_client):
        """测试特殊字符的处理"""
        special_chars = [
            "published@#$%^&*()",
            "published!@#$%",
            "published<>?/.,",
            "published[]{}|\\",
        ]
        
        for value in special_chars:
            response = authenticated_client.get(f'/api/contents/?status={value}')
            assert response.status_code == 400, f"包含特殊字符的值 '{value}' 应该被拒绝"
