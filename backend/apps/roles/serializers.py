from rest_framework import serializers
from .models import Permission, Role


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'code', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class RoleSerializer(serializers.ModelSerializer):
    """普通的角色序列化"""
    # 1. 读：返回完整权限列表（嵌套序列化）
    permissions = PermissionSerializer(many=True, read_only=True)
    # 2. 写：接收权限ID列表（只写、不传也可以）
    permission_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,    # 只用于创建/更新，不返回给前端
        required=False
    )

    class Meta:
        model = Role
        fields = ['id', 'name', 'code', 'description', 'permissions', 'permission_ids', 'is_system', 'created_at', 'updated_at']
        read_only_fields = ['id', 'is_system', 'created_at', 'updated_at']

    def create(self, validated_data):
        """
        新增的时候触发

        调用了 serializer.save()
        创建序列化器时，没有传 instance=（也就是没有要更新的对象）
        :param validated_data:
        :return:
        """
        # 1. 从验证后的数据中提取 'permission_ids' 字段，默认值为空列表
        permission_ids = validated_data.pop('permission_ids', [])
        # 2. 使用剩余的验证数据，创建并保存一个新的 Role 对象到数据库
        role = Role.objects.create(**validated_data)
        # 3. 如果存在权限ID列表，则为角色分配权限
        if permission_ids:
            # Django 多对多（ManyToManyField）关系的 set() 方法。
            role.permissions.set(Permission.objects.filter(id__in=permission_ids))
        return role

    def update(self, instance, validated_data):
        """
        更新的时候触发

        调用了 serializer.save()
        创建序列化器时，必须传入 instance=（要修改的模型对象）
        :param instance:
        :param validated_data:
        :return:
        """
        permission_ids = validated_data.pop('permission_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if permission_ids is not None:
            instance.permissions.set(Permission.objects.filter(id__in=permission_ids))
        return instance


class RoleListSerializer(serializers.ModelSerializer):
    """列表操作的序列化类"""
    # SerializerMethodField 是 Django REST Framework 中用于在序列化器里动态添加只读字段的核心工具，
    # 通过自定义方法生成字段值，常用于数据加工、关联对象展示、计算字段等场景。
    # 必须对应一个 get_<字段名> 的方法，方法接收当前序列化对象 obj，返回值即为字段内容。
    permission_count = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = ['id', 'name', 'code', 'description', 'is_system', 'permission_count', 'created_at']

    def get_permission_count(self, obj):
        return obj.permissions.count()
