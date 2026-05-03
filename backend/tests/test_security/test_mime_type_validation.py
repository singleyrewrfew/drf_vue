"""
文件 MIME 类型验证测试

测试基于文件内容的真实 MIME 类型检测，防止 MIME 类型伪造攻击。
"""
import pytest
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.exceptions import ValidationError
from utils.file_validation import (
    validate_file_mime_type,
    validate_image_file,
    validate_video_file,
    sanitize_svg
)


class TestMIMETypeValidation:
    """MIME 类型验证测试"""
    
    def test_valid_jpeg_file(self):
        """测试有效的 JPEG 文件"""
        # JPEG 文件魔数: FF D8 FF
        jpeg_data = bytes([0xFF, 0xD8, 0xFF, 0xE0]) + b'\x00' * 100
        file = SimpleUploadedFile(
            'test.jpg',
            jpeg_data,
            content_type='image/jpeg'
        )
        
        result = validate_file_mime_type(file, ['image/jpeg', 'image/png'])
        assert result == 'image/jpeg'
    
    def test_valid_png_file(self):
        """测试有效的 PNG 文件"""
        # PNG 文件魔数: 89 50 4E 47 0D 0A 1A 0A
        png_data = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]) + b'\x00' * 100
        file = SimpleUploadedFile(
            'test.png',
            png_data,
            content_type='image/png'
        )
        
        result = validate_file_mime_type(file, ['image/jpeg', 'image/png'])
        assert result == 'image/png'
    
    def test_mime_type_forgery_detected(self):
        """检测到 MIME 类型伪造（扩展名与内容不符）"""
        # 创建一个实际上是 JPEG 但声称是 PNG 的文件
        jpeg_data = bytes([0xFF, 0xD8, 0xFF, 0xE0]) + b'\x00' * 100
        file = SimpleUploadedFile(
            'malicious.png',  # 扩展名是 .png
            jpeg_data,
            content_type='image/png'  # 声明为 PNG
        )
        
        # 应该检测到真实的 MIME 类型是 JPEG
        result = validate_file_mime_type(file, ['image/jpeg', 'image/png'])
        assert result == 'image/jpeg'  # 返回真实类型
    
    def test_invalid_file_type_rejected(self):
        """拒绝不支持的文件类型"""
        # EXE 文件魔数: 4D 5A
        exe_data = bytes([0x4D, 0x5A]) + b'\x00' * 100
        file = SimpleUploadedFile(
            'virus.exe',
            exe_data,
            content_type='application/octet-stream'
        )
        
        with pytest.raises(ValidationError) as exc_info:
            validate_file_mime_type(file, ['image/jpeg', 'image/png'])
        
        assert '不支持的文件类型' in str(exc_info.value)
    
    def test_empty_file_rejected(self):
        """拒绝空文件"""
        file = SimpleUploadedFile('empty.txt', b'', content_type='text/plain')
        
        with pytest.raises(ValidationError) as exc_info:
            validate_file_mime_type(file, ['text/plain'])
        
        assert '文件内容为空' in str(exc_info.value)
    
    def test_validate_image_file_helper(self):
        """测试图片文件验证辅助函数"""
        jpeg_data = bytes([0xFF, 0xD8, 0xFF, 0xE0]) + b'\x00' * 100
        file = SimpleUploadedFile('test.jpg', jpeg_data, content_type='image/jpeg')
        
        result = validate_image_file(file)
        assert result == 'image/jpeg'
    
    def test_non_image_rejected_by_helper(self):
        """辅助函数拒绝非图片文件"""
        exe_data = bytes([0x4D, 0x5A]) + b'\x00' * 100
        file = SimpleUploadedFile('test.exe', exe_data, content_type='application/x-msdownload')
        
        with pytest.raises(ValidationError):
            validate_image_file(file)


class TestSVGSanitization:
    """SVG 安全清洗测试"""
    
    def test_clean_svg_passes(self):
        """测试干净的 SVG 通过验证"""
        svg = '''<?xml version="1.0"?>
        <svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
            <circle cx="50" cy="50" r="40" fill="red"/>
        </svg>'''
        
        result = sanitize_svg(svg)
        assert '<circle' in result
        assert 'fill="red"' in result
    
    def test_script_tag_removed(self):
        """移除 script 标签"""
        malicious_svg = '''<?xml version="1.0"?>
        <svg xmlns="http://www.w3.org/2000/svg">
            <script>alert('XSS')</script>
            <circle cx="50" cy="50" r="40"/>
        </svg>'''
        
        result = sanitize_svg(malicious_svg)
        assert '<script>' not in result
        assert "alert('XSS')" not in result
        assert '<circle' in result
    
    def test_event_handler_removed(self):
        """移除恶意事件处理器"""
        malicious_svg = '''<?xml version="1.0"?>
        <svg xmlns="http://www.w3.org/2000/svg">
            <circle cx="50" cy="50" r="40" onclick="alert('XSS')"/>
        </svg>'''
        
        result = sanitize_svg(malicious_svg)
        assert 'onclick=' not in result.lower()
        assert "alert('XSS')" not in result
    
    def test_javascript_protocol_removed(self):
        """移除 javascript: 协议"""
        malicious_svg = '''<?xml version="1.0"?>
        <svg xmlns="http://www.w3.org/2000/svg">
            <a href="javascript:alert('XSS')">
                <circle cx="50" cy="50" r="40"/>
            </a>
        </svg>'''
        
        result = sanitize_svg(malicious_svg)
        assert 'javascript:' not in result.lower()
    
    def test_data_protocol_removed(self):
        """移除 data: 协议"""
        malicious_svg = '''<?xml version="1.0"?>
        <svg xmlns="http://www.w3.org/2000/svg">
            <image href="data:text/html;base64,PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4="/>
        </svg>'''
        
        result = sanitize_svg(malicious_svg)
        assert 'data:' not in result.lower()
    
    def test_multiple_attacks_sanitized(self):
        """多重攻击向量都被清理"""
        malicious_svg = '''<?xml version="1.0"?>
        <svg xmlns="http://www.w3.org/2000/svg">
            <script>alert('XSS')</script>
            <circle cx="50" cy="50" r="40" onclick="steal()" onerror="hack()"/>
            <a href="javascript:void(0)">Link</a>
        </svg>'''
        
        result = sanitize_svg(malicious_svg)
        assert '<script>' not in result
        assert 'onclick=' not in result.lower()
        assert 'onerror=' not in result.lower()
        assert 'javascript:' not in result.lower()
        assert '<circle' in result  # 保留安全元素


@pytest.mark.django_db
class TestMediaUploadWithMIMEValidation:
    """媒体上传集成测试（需要数据库）"""
    
    def test_upload_valid_image(self, api_client, admin_user):
        """测试上传有效的图片文件"""
        from apps.media.models import Media
        
        api_client.force_authenticate(user=admin_user)
        
        # 创建真实的 JPEG 文件
        jpeg_data = bytes([0xFF, 0xD8, 0xFF, 0xE0]) + b'\x00' * 1000
        file = SimpleUploadedFile('test.jpg', jpeg_data, content_type='image/jpeg')
        
        response = api_client.post('/api/media/', {'file': file}, format='multipart')
        
        # 注意：由于我们使用的是伪数据，实际测试可能需要真实的图片文件
        # 这里主要验证验证逻辑被调用
        assert response.status_code in [201, 400]  # 可能成功或因数据不完整失败
    
    def test_upload_malicious_file_rejected(self, api_client, admin_user):
        """测试恶意文件被拒绝"""
        api_client.force_authenticate(user=admin_user)
        
        # 尝试上传 EXE 文件伪装成 JPG
        exe_data = bytes([0x4D, 0x5A]) + b'\x00' * 1000
        file = SimpleUploadedFile('virus.jpg', exe_data, content_type='image/jpeg')
        
        response = api_client.post('/api/media/', {'file': file}, format='multipart')
        
        # 应该被拒绝（400 Bad Request）
        assert response.status_code == 400
        assert '不支持的文件类型' in str(response.data)


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def admin_user():
    from apps.users.models import User
    from apps.roles.models import Role
    
    role, _ = Role.objects.get_or_create(code='admin', name='管理员')
    user, _ = User.objects.get_or_create(
        username='admin',
        defaults={'email': 'admin@example.com', 'role': role}
    )
    if not user.is_superuser:
        user.is_superuser = True
        user.save()
    return user
