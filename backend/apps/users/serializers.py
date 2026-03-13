from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name', read_only=True)
    role_code = serializers.CharField(source='role.code', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'avatar', 'role', 'role_name', 'role_code', 'is_staff', 'is_active', 'is_superuser', 'created_at', 'updated_at']
        read_only_fields = ['id', 'is_staff', 'is_superuser', 'created_at', 'updated_at']


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
        avatar_url = validated_data.pop('avatar_url', None)
        if avatar_url:
            if avatar_url.startswith('/media/'):
                instance.avatar.name = avatar_url.replace('/media/', '')
            else:
                instance.avatar = avatar_url
        
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
        
        return super().update(instance, validated_data)


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
