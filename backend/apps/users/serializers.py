from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name', read_only=True)
    role_code = serializers.CharField(source='role.code', read_only=True)
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'avatar', 'avatar_url', 'role', 'role_name', 'role_code', 'is_staff', 'is_active', 'is_superuser', 'created_at', 'updated_at']
        read_only_fields = ['id', 'is_staff', 'is_superuser', 'created_at', 'updated_at']
    
    def get_avatar_url(self, obj):
        """返回完整的头像 URL"""
        if obj.avatar:
            return obj.avatar.url
        return None


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True)
    role = serializers.PrimaryKeyRelatedField(queryset=User._meta.get_field('role').related_model.objects.all(), required=False, allow_null=True)
    is_active = serializers.BooleanField(required=False, default=True)
    is_staff = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'role', 'is_active', 'is_staff']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password_confirm': '两次密码不一致'})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        role = validated_data.pop('role', None)
        is_active = validated_data.pop('is_active', True)
        is_staff = validated_data.pop('is_staff', False)
        
        from apps.roles.models import Role
        user = User.objects.create_user(**validated_data)
        user.is_active = is_active
        user.is_staff = is_staff
        
        if role:
            user.role = role
        else:
            default_role = Role.objects.filter(code='user').first()
            if default_role:
                user.role = default_role
        
        # 根据角色设置 is_staff
        if user.role and user.role.code in ['admin', 'editor']:
            user.is_staff = True
        
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False, allow_null=True)
    avatar_url = serializers.CharField(required=False, write_only=True)
    is_staff = serializers.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['email', 'avatar', 'avatar_url', 'role', 'is_staff']

    def update(self, instance, validated_data):
        import logging
        logger = logging.getLogger(__name__)
        
        logger.info(f"UserUpdateSerializer.update called with validated_data: {validated_data}")
        
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
                if role.code in ['admin', 'editor']:
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
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=6)
    new_password_confirm = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('原密码错误')
        return value

    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError({'new_password_confirm': '两次密码不一致'})
        return data

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
