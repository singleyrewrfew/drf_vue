"""
用户序列化器测试

测试用户相关序列化器的数据验证和输入输出
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from apps.users.serializers import (
    UserSerializer,
    UserRegisterSerializer,
    UserUpdateSerializer,
)
from apps.roles.models import Role

User = get_user_model()


@pytest.mark.unit
class TestUserSerializer:
    """用户序列化器测试类"""
    
    def test_user_serializer_output(self, db):
        """测试用户序列化器输出"""
        # 使用 get_or_create 避免重复创建
        role, created = Role.objects.get_or_create(code='user', defaults={'name': '普通用户'})
        
        # 创建用户
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role=role
        )
        
        # 序列化用户
        serializer = UserSerializer(user)
        data = serializer.data
        
        # 验证输出字段
        assert data['username'] == 'testuser'
        assert data['email'] == 'test@example.com'
        assert data['role_name'] == '普通用户'
        assert data['role_code'] == 'user'
        assert 'id' in data
        assert 'created_at' in data
    
    def test_user_serializer_readonly_fields(self, db):
        """测试只读字段不能被修改"""
        role, created = Role.objects.get_or_create(code='user', defaults={'name': '普通用户'})
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role=role
        )
        
        # 尝试修改只读字段
        serializer = UserSerializer(user, data={
            'username': 'newusername',
            'is_admin': True  # 只读字段
        }, partial=True)
        
        # is_admin 是只读的，应该被忽略
        assert serializer.is_valid()
        user_updated = serializer.save()
        assert user_updated.username == 'newusername'
        # is_admin 不会被修改，因为它是只读的


@pytest.mark.unit
class TestUserRegisterSerializer:
    """用户注册序列化器测试类"""
    
    def test_register_success(self, db):
        """测试成功注册"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'securepass123',
            'password_confirm': 'securepass123'
        }
        
        serializer = UserRegisterSerializer(data=data)
        assert serializer.is_valid()
        
        user = serializer.save()
        assert user.username == 'newuser'
        assert user.email == 'newuser@example.com'
        assert user.check_password('securepass123')
        assert user.role.code == 'user'  # 默认角色
    
    def test_register_with_role(self, db):
        """测试带角色注册"""
        admin_role, created = Role.objects.get_or_create(code='admin', defaults={'name': '管理员'})
        
        data = {
            'username': 'adminuser',
            'email': 'admin@example.com',
            'password': 'adminpass123',
            'password_confirm': 'adminpass123',
            'role': admin_role.id
        }
        
        serializer = UserRegisterSerializer(data=data)
        assert serializer.is_valid()
        
        user = serializer.save()
        assert user.role == admin_role
    
    def test_register_password_mismatch(self, db):
        """测试密码不一致"""
        data = {
            'username': 'baduser',
            'email': 'bad@example.com',
            'password': 'pass123',
            'password_confirm': 'pass456'  # 不同的密码
        }
        
        serializer = UserRegisterSerializer(data=data)
        assert not serializer.is_valid()
        assert 'password_confirm' in serializer.errors
    
    def test_register_short_password(self, db):
        """测试密码太短"""
        data = {
            'username': 'shortpass',
            'email': 'short@example.com',
            'password': '12',  # 小于 6 位
            'password_confirm': '12'
        }
        
        serializer = UserRegisterSerializer(data=data)
        assert not serializer.is_valid()
        assert 'password' in serializer.errors
    
    def test_register_duplicate_username(self, db):
        """测试重复用户名"""
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='pass123'
        )
        
        data = {
            'username': 'existinguser',
            'email': 'new@example.com',
            'password': 'pass123',
            'password_confirm': 'pass123'
        }
        
        serializer = UserRegisterSerializer(data=data)
        assert not serializer.is_valid()
        assert 'username' in serializer.errors


@pytest.mark.unit
class TestUserUpdateSerializer:
    """用户更新序列化器测试类"""
    
    def test_update_email(self, db):
        """测试更新邮箱"""
        user = User.objects.create_user(
            username='testuser',
            email='old@example.com',
            password='pass123'
        )
        
        data = {'email': 'new@example.com'}
        serializer = UserUpdateSerializer(user, data=data, partial=True)
        assert serializer.is_valid()
        
        user_updated = serializer.save()
        assert user_updated.email == 'new@example.com'
    
    def test_update_is_staff(self, db):
        """测试更新 is_staff"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='pass123',
            is_staff=False
        )
        
        data = {'is_staff': True}
        serializer = UserUpdateSerializer(user, data=data, partial=True)
        assert serializer.is_valid()
        
        user_updated = serializer.save()
        assert user_updated.is_staff is True
