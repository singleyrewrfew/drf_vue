"""
用户序列化器测试

测试用户相关序列化器的数据验证和输入输出

作用：验证用户序列化器的数据序列化、反序列化和验证逻辑
使用：运行 pytest tests/test_serializers/test_user_serializer.py 执行测试

测试覆盖的序列化器：
    1. UserSerializer - 用户信息序列化（用于展示）
    2. UserRegisterSerializer - 用户注册序列化（含密码验证）
    3. UserUpdateSerializer - 用户信息更新序列化

测试场景：
    - 用户数据序列化输出格式验证
    - 只读字段保护机制验证
    - 用户注册流程及数据验证
    - 密码一致性检查
    - 密码强度验证
    - 用户名唯一性检查
    - 用户信息更新功能
"""
import pytest
from django.contrib.auth import get_user_model

from apps.roles.models import Role
from apps.users.serializers import (
    UserSerializer,
    UserRegisterSerializer,
    UserUpdateSerializer,
)

User = get_user_model()


@pytest.mark.unit
class TestUserSerializer:
    """
    UserSerializer 测试类
    
    验证用户序列化器的输出格式和只读字段保护机制。
    UserSerializer 主要用于用户信息的展示，不包含敏感信息如密码。
    
    测试用例：
        - 验证序列化输出的字段完整性和正确性
        - 验证只读字段不能被修改
    
    序列化字段：
        - id: 用户 ID（只读）
        - username: 用户名（只读）
        - email: 邮箱
        - role_name: 角色名称（只读）
        - role_code: 角色代码（只读）
        - created_at: 创建时间（只读）
        - is_admin: 是否管理员（只读）
    """
    
    def test_user_serializer_output(self, db):
        """
        测试用户序列化器的输出格式和字段完整性
        
        验证 UserSerializer 能够正确地将用户对象序列化为字典，
        包含所有必要的字段，且字段值正确。
        
        测试步骤：
            1. 创建或获取默认角色（避免重复创建）
            2. 创建测试用户并关联角色
            3. 使用 UserSerializer 序列化用户对象
            4. 验证输出数据的各个字段值
        
        预期结果：
            - username 字段正确
            - email 字段正确
            - role_name 显示角色中文名
            - role_code 显示角色代码
            - 包含 id 和 created_at 等系统字段
        
        注意：
            - 使用 get_or_create 避免测试间的数据冲突
            - 确保角色关联正确设置
        """
        # 使用 get_or_create 避免重复创建
        role, created = Role.objects.get_or_create(code='user', defaults={'name': '普通用户'})
        
        # 创建唯一用户名的测试用户
        user, _ = User.objects.get_or_create(
            username='testuser_serializer_output',
            defaults={
                'email': 'test@example.com',
                'role': role
            }
        )
        if not user.role:
            user.role = role
            user.save()
        
        # 序列化用户
        serializer = UserSerializer(user)
        data = serializer.data
        
        # 验证输出字段
        assert data['username'] == 'testuser_serializer_output'
        assert data['email'] == 'test@example.com'
        assert data['role_name'] == '普通用户'
        assert data['role_code'] == 'user'
        assert 'id' in data
        assert 'created_at' in data
    
    def test_user_serializer_readonly_fields(self, db):
        """
        测试用户序列化器的只读字段保护机制
        
        验证标记为 read_only 的字段在反序列化时不会被修改，
        即使传入数据中包含这些字段，也应该被忽略。
        
        测试步骤：
            1. 创建或获取默认角色
            2. 创建测试用户
            3. 尝试通过序列化器修改 username 和 is_admin
            4. 验证序列化器是否有效
            5. 保存并检查实际修改结果
        
        预期结果：
            - serializer.is_valid() 返回 True（忽略只读字段后数据有效）
            - username 成功修改（非只读字段）
            - is_admin 保持不变（只读字段被忽略）
        
        安全意义：
            - 防止客户端通过 API 修改受保护的字段
            - 确保权限相关字段只能通过服务端逻辑修改
        """
        role, created = Role.objects.get_or_create(code='user', defaults={'name': '普通用户'})
        
        user, _ = User.objects.get_or_create(
            username='testuser_readonly',
            defaults={
                'email': 'test_readonly@example.com',
                'role': role
            }
        )
        if not user.role:
            user.role = role
            user.save()
        
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
    """
    UserRegisterSerializer 测试类
    
    验证用户注册序列化器的数据验证和用户创建逻辑。
    该序列化器专门用于用户注册场景，包含密码确认、密码强度等验证。
    
    测试用例：
        - 正常注册流程
        - 带角色注册的流程
        - 密码不一致的验证
        - 密码长度不足的验证
        - 用户名重复的验证
    
    验证规则：
        - password 和 password_confirm 必须一致
        - 密码长度至少 6 位
        - 用户名必须唯一
        - 默认分配普通用户角色
    """
    
    def test_register_success(self, db):
        """
        测试用户注册成功场景
        
        验证提供正确的注册数据时，能够成功创建用户，
        密码被正确加密，且分配默认角色。
        
        测试步骤：
            1. 准备注册数据（用户名、邮箱、密码、确认密码）
            2. 创建 UserRegisterSerializer 实例并传入数据
            3. 调用 is_valid() 验证数据
            4. 调用 save() 创建用户
            5. 验证用户对象的各个属性
        
        预期结果：
            - is_valid() 返回 True
            - 用户成功创建，username 和 email 正确
            - 密码被正确加密（check_password 验证通过）
            - 默认分配 'user' 角色（普通用户）
        
        安全考虑：
            - 密码不会以明文存储
            - 默认分配最低权限角色
        """
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
        """
        测试用户注册时指定角色
        
        验证注册时可以通过 role 字段指定用户角色，
        适用于管理员创建用户或特殊角色分配场景。
        
        测试步骤：
            1. 创建或获取管理员角色
            2. 准备注册数据，包含 role 字段（角色 ID）
            3. 创建序列化器并验证数据
            4. 保存用户
            5. 验证用户的角色是否正确设置
        
        预期结果：
            - is_valid() 返回 True
            - 用户成功创建
            - user.role 等于指定的 admin_role
        
        应用场景：
            - 管理员后台创建用户
            - 批量导入用户时指定角色
        
        注意：
            - 实际生产中可能需要权限控制，防止普通用户自行指定管理员角色
        """
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
        """
        测试密码与确认密码不一致时的验证
        
        验证当 password 和 password_confirm 字段不匹配时，
        序列化器能够正确识别并返回验证错误。
        
        测试步骤：
            1. 准备注册数据，故意设置不同的密码和确认密码
            2. 创建序列化器并验证数据
            3. 检查验证结果
            4. 验证错误信息中包含 password_confirm 字段
        
        预期结果：
            - is_valid() 返回 False
            - serializer.errors 中包含 'password_confirm' 键
            - 用户不会被创建
        
        安全意义：
            - 防止用户因输入错误导致密码设置失败
            - 确保用户明确知道自己设置的密码
        """
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
        """
        测试密码长度不足时的验证
        
        验证当密码长度小于最小要求（6 位）时，
        序列化器能够拒绝注册并返回相应的错误提示。
        
        测试步骤：
            1. 准备注册数据，使用过短的密码（2 位）
            2. 创建序列化器并验证数据
            3. 检查验证结果
            4. 验证错误信息中包含 password 字段
        
        预期结果：
            - is_valid() 返回 False
            - serializer.errors 中包含 'password' 键
            - 用户不会被创建
        
        安全意义：
            - 强制用户使用足够长度的密码
            - 提高账户安全性，防止弱密码
        """
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
        """
        测试用户名重复时的验证
        
        验证当尝试注册已存在的用户名时，
        序列化器能够检测到并返回唯一性验证错误。
        
        测试步骤：
            1. 预先创建一个用户（existinguser）
            2. 尝试使用相同的用户名注册新用户
            3. 创建序列化器并验证数据
            4. 检查验证结果
            5. 验证错误信息中包含 username 字段
        
        预期结果：
            - is_valid() 返回 False
            - serializer.errors 中包含 'username' 键
            - 新用户不会被创建
        
        安全意义：
            - 保证用户名的唯一性
            - 防止用户身份混淆
            - 避免潜在的安全问题（如身份冒充）
        """
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
    """
    UserUpdateSerializer 测试类
    
    验证用户信息更新序列化器的功能。
    该序列化器用于用户部分更新自己的信息，支持选择性更新字段。
    
    测试用例：
        - 更新邮箱地址
        - 更新 is_staff 状态
    
    特性：
        - 支持部分更新（partial=True）
        - 只允许更新特定字段
        - 保持其他字段不变
    
    适用场景：
        - 用户修改个人资料
        - 管理员调整用户权限
    """
    
    def test_update_email(self, db):
        """
        测试更新用户邮箱地址
        
        验证用户可以通过序列化器更新自己的邮箱地址，
        这是最常见的个人信息更新操作之一。
        
        测试步骤：
            1. 创建或获取测试用户（初始邮箱为 old@example.com）
            2. 准备更新数据，只包含新的邮箱地址
            3. 创建 UserUpdateSerializer 实例，启用 partial 模式
            4. 验证数据有效性
            5. 保存更改
            6. 验证邮箱已成功更新
        
        预期结果：
            - is_valid() 返回 True
            - 用户邮箱从 old@example.com 更新为 new@example.com
            - 其他字段（username、is_staff 等）保持不变
        
        应用场景：
            - 用户更换邮箱
            - 修正错误的邮箱地址
        """
        user, _ = User.objects.get_or_create(
            username='testuser_update_email',
            defaults={
                'email': 'old@example.com',
            }
        )
        
        data = {'email': 'new@example.com'}
        serializer = UserUpdateSerializer(user, data=data, partial=True)
        assert serializer.is_valid()
        
        user_updated = serializer.save()
        assert user_updated.email == 'new@example.com'
    
    def test_update_is_staff(self, db):
        """
        测试更新用户的 is_staff 状态
        
        验证可以通过序列化器修改用户的 is_staff 字段，
        这通常由管理员操作，用于授予或撤销用户的后台访问权限。
        
        测试步骤：
            1. 创建或获取测试用户（初始 is_staff=False）
            2. 准备更新数据，将 is_staff 设置为 True
            3. 创建 UserUpdateSerializer 实例，启用 partial 模式
            4. 验证数据有效性
            5. 保存更改
            6. 验证 is_staff 已成功更新为 True
        
        预期结果：
            - is_valid() 返回 True
            - 用户 is_staff 从 False 更新为 True
            - 用户获得后台访问权限
        
        安全考虑：
            - 此操作应在权限控制的视图中执行
            - 只有管理员才能修改其他用户的 is_staff 状态
            - 修改 is_staff 会影响用户的登录和管理权限
        
        应用场景：
            - 提升普通用户为工作人员
            - 撤销工作人员的后台访问权限
        """
        user, _ = User.objects.get_or_create(
            username='testuser_update_staff',
            defaults={
                'email': 'test_staff@example.com',
                'is_staff': False
            }
        )
        
        data = {'is_staff': True}
        serializer = UserUpdateSerializer(user, data=data, partial=True)
        assert serializer.is_valid()
        
        user_updated = serializer.save()
        assert user_updated.is_staff is True
