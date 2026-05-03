from rest_framework import serializers, status
from django.contrib.auth import get_user_model
from utils.response import StandardResponse, api_error

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    用户序列化器
    
    用于返回用户信息，包含计算属性和只读字段
    """
    # 角色名称：从关联的角色对象获取
    role_name = serializers.CharField(source='role.name', read_only=True)
    # 角色代码：从关联的角色对象获取
    role_code = serializers.CharField(source='role.code', read_only=True)
    # 头像 URL：使用方法字段动态生成
    avatar_url = serializers.SerializerMethodField()
    # 权限列表：使用方法字段动态获取
    permissions = serializers.SerializerMethodField()
    # 是否为管理员：只读属性，从 User 模型计算
    is_admin = serializers.BooleanField(read_only=True)
    # 是否为编辑者：只读属性，从 User 模型计算
    is_editor = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = User
        # 包含的字段：ID、用户名、邮箱、头像、角色信息、权限状态、时间戳等
        fields = ['id', 'username', 'email', 'avatar', 'avatar_url', 'role', 'role_name', 'role_code', 'is_staff', 'is_active', 'is_superuser', 'is_admin', 'is_editor', 'permissions', 'created_at', 'updated_at']
        # 只读字段：不允许通过 API 修改这些字段
        read_only_fields = ['id', 'is_staff', 'is_superuser', 'is_admin', 'is_editor', 'created_at', 'updated_at']
    
    def get_avatar_url(self, obj):
        """返回完整的头像 URL"""
        if obj.avatar:
            return obj.avatar.url
        return None
    
    def get_permissions(self, obj):
        """返回用户权限列表"""
        return obj.get_permission_codes()

class UserRegisterSerializer(serializers.ModelSerializer):
    """
    用户注册序列化器
    
    用于创建新用户，包含密码确认和角色分配
    """
    # 密码：只写字段，最小长度 6 位
    password = serializers.CharField(write_only=True, min_length=6)
    # 确认密码：只写字段，用于验证密码一致性
    password_confirm = serializers.CharField(write_only=True)
    # 角色：外键，允许为空，默认分配普通用户角色
    role = serializers.PrimaryKeyRelatedField(queryset=User._meta.get_field('role').related_model.objects.all(), required=False, allow_null=True)
    # 是否激活：默认为 True
    is_active = serializers.BooleanField(required=False, default=True)
    # 是否为后台用户：默认为 False
    is_staff = serializers.BooleanField(required=False, default=False)
    
    class Meta:
        model = User
        # 注册时需要的字段
        fields = ['username', 'email', 'password', 'password_confirm', 'role', 'is_active', 'is_staff']
    
    def validate(self, data):
        """
        验证密码一致性
        
        如果两次输入的密码不一致，抛出验证错误
        """
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password_confirm': '两次密码不一致'})
        return data
    
    def create(self, validated_data):
        """
        创建用户
        
        步骤：
        1. 移除确认密码字段
        2. 获取角色和激活状态
        3. 创建用户
        4. 分配角色（如果提供）
        5. 设置后台权限（根据角色权限）
        """
        # 移除确认密码，不需要保存到数据库
        validated_data.pop('password_confirm')
        # 获取角色和激活状态，使用 pop 避免后续处理
        role = validated_data.pop('role', None)
        is_active = validated_data.pop('is_active', True)
        is_staff = validated_data.pop('is_staff', False)

        # 创建用户（Django 的 create_user 会自动哈希密码）
        user = User.objects.create_user(**validated_data)
        # 设置激活状态
        user.is_active = is_active
        user.is_staff = is_staff

        # 分配角色（如果提供了角色）
        if role:
            user.role = role
        else:
            # 如果没有提供角色，分配默认的普通用户角色
            from apps.roles.models import Role
            default_role = Role.objects.filter(code='user').first()
            if default_role:
                user.role = default_role

        # 根据角色权限设置 is_staff（有后台管理权限的用户需要 is_staff=True）
        if user.role:
            # 管理员权限：可以管理角色
            admin_permissions = ['role_manage', 'user_view', 'user_create', 'user_update', 'user_delete']
            if user.role.permissions.filter(code__in=admin_permissions).exists():
                user.is_staff = True

        # 保存用户
        user.save()
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    """
    用户更新序列化器
    
    用于更新用户信息，主要处理头像和角色更新
    """
    # 头像：允许上传图片，可以为空
    avatar = serializers.ImageField(required=False, allow_null=True)
    # 头像 URL：只写字段，用于接收前端传递的 URL
    avatar_url = serializers.CharField(required=False, write_only=True)
    # 是否为后台用户：允许修改
    is_staff = serializers.BooleanField(required=False)
    
    class Meta:
        model = User
        # 更新时可以修改的字段
        fields = ['email', 'avatar', 'avatar_url', 'role', 'is_staff']
    
    def update(self, instance, validated_data):
        """
        更新用户信息
        
        主要处理：
        1. 头像更新（支持文件对象或 URL）
        2. 角色更新
        3. 后台权限更新（根据角色权限自动设置）
        """
        import logging
        logger = logging.getLogger(__name__)
        
        logger.info(f"UserUpdateSerializer.update called with validated_data: {validated_data}")
        
        # 获取并移除 avatar_url（这是前端传递的 URL，不是文件对象）
        avatar_url = validated_data.pop('avatar_url', None)
        logger.info(f"avatar_url from request: {avatar_url}")
        
        # 如果提供了 avatar_url，手动设置 avatar 字段
        if avatar_url:
            # 处理相对路径
            if avatar_url.startswith('/media/'):
                # 去掉 /media/ 前缀，只保存相对路径
                avatar_path = avatar_url.replace('/media/', '', 1)
                instance.avatar.name = avatar_path
                logger.info(f"Set avatar.name from avatar_url: {avatar_path}")
            elif avatar_url.startswith('media/'):
                # 已经是相对路径
                instance.avatar.name = avatar_url
                logger.info(f"Set avatar.name from avatar_url: {avatar_url}")
            else:
                # 其他情况直接赋值
                instance.avatar.name = avatar_url
                logger.info(f"Set avatar.name from avatar_url: {avatar_url}")
            # 从 validated_data 中移除 avatar，因为我们已经手动设置了
            validated_data.pop('avatar', None)
        # 否则，如果 validated_data 中有 avatar 文件对象，保持原样（ImageField 会自动处理）
        elif 'avatar' in validated_data:
            logger.info(f"Avatar file object provided: {validated_data['avatar']}")
        
        logger.info(f"Final validated_data before super().update: {validated_data}")
        
        # 更新角色时自动设置 is_staff
        role = validated_data.get('role')
        if role:
            instance.role = role
            # 如果手动设置了 is_staff，则使用手动设置的值
            if 'is_staff' not in validated_data:
                admin_permissions = ['role_manage', 'user_view', 'user_create', 'user_update', 'user_delete']
                if role.permissions.filter(code__in=admin_permissions).exists():
                    instance.is_staff = True
                else:
                    instance.is_staff = False
        # 如果显式传递了 is_staff，使用传递的值
        if 'is_staff' in validated_data:
            instance.is_staff = validated_data['is_staff']
        
        # 调用父类的 update 方法
        result = super().update(instance, validated_data)
        
        # 如果手动设置了 avatar.name，需要保存
        if avatar_url:
            result.save()
            logger.info(f"Saved instance with manually set avatar")
        
        logger.info(f"Updated user avatar: {result.avatar}, avatar.name: {result.avatar.name if result.avatar else None}")
        return result

class PasswordChangeSerializer(serializers.Serializer):
    """
    密码修改序列化器
    
    用于用户修改密码，需要验证原密码
    """
    # 原密码：只写字段
    old_password = serializers.CharField(write_only=True)
    # 新密码：只写字段，最小长度 6 位
    new_password = serializers.CharField(write_only=True, min_length=6)
    # 确认新密码：只写字段
    new_password_confirm = serializers.CharField(write_only=True)
    
    def validate_old_password(self, value):
        """
        验证原密码是否正确
        
        从请求上下文中获取当前用户，使用 check_password 方法验证
        """
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('原密码错误')
        return value
    
    def validate(self, data):
        """
        验证新密码一致性
        
        确保两次输入的新密码一致
        """
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError({'new_password_confirm': '两次密码不一致'})
        return data
    
    def save(self):
        """
        保存新密码
        
        使用 Django 的 set_password 方法自动哈希密码
        """
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
