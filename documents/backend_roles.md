# Roles 应用视图集详解

> 💡 **文档定位**: 本文档是 Roles 应用的完整实现指南，包含数据模型、序列化器、视图集的详细说明。
>
> **通用原理**: DRF 视图集的通用原理请查看 [`backend_viewsets_guide.md`](backend_viewsets_guide.md)
>
> **完整教程**: 从零开始的开发流程请查看 [`backend.md`](backend.md)

## 概述

Roles 应用是整个 CMS 系统的权限基础，提供角色和权限的管理功能。

**核心功能**：
- 权限的 CRUD
- 角色的 CRUD
- 为角色分配权限
- 权限验证

---

## 数据模型

### Permission 模型

```python
class Permission(models.Model):
    """权限表 - 定义系统中所有的权限"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=100, unique=True, verbose_name='权限代码')
    name = models.CharField(max_length=100, verbose_name='权限名称')
    description = models.TextField(blank=True, verbose_name='描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'permissions'
        verbose_name = '权限'
        ordering = ['code']
```

### Role 模型

```python
class Role(models.Model):
    """角色表 - 用户的角色"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=50, unique=True, verbose_name='角色代码')
    name = models.CharField(max_length=50, verbose_name='角色名称')
    description = models.TextField(blank=True, verbose_name='描述')
    permissions = models.ManyToManyField(Permission, blank=True, related_name='roles', verbose_name='权限')
    is_system = models.BooleanField(default=False, verbose_name='系统角色')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def has_permission(self, code):
        """检查角色是否有某个权限"""
        return self.permissions.filter(code=code).exists()
```

---

## 序列化器

### PermissionSerializer

```python
class PermissionSerializer(serializers.ModelSerializer):
    """权限序列化器 - 只读展示"""
    class Meta:
        model = Permission
        fields = ['id', 'code', 'name', 'description', 'created_at']
        read_only_fields = fields
```

### RoleSerializer

```python
class RoleSerializer(serializers.ModelSerializer):
    """角色序列化器 - 包含权限详情"""
    permissions = PermissionSerializer(many=True, read_only=True)
    permission_ids = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(),
        source='permissions',
        write_only=True,
        required=False
    )

    class Meta:
        model = Role
        fields = ['id', 'code', 'name', 'description', 'is_system', 
                  'permissions', 'permission_ids', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
```

### RoleCreateUpdateSerializer

```python
class RoleCreateUpdateSerializer(serializers.ModelSerializer):
    """角色创建/更新序列化器 - 简化版"""
    class Meta:
        model = Role
        fields = ['code', 'name', 'description', 'permissions', 'is_system']

    def create(self, validated_data):
        permissions_data = validated_data.pop('permissions', [])
        role = Role.objects.create(**validated_data)
        if permissions_data:
            role.permissions.set(permissions_data)
        return role

    def update(self, instance, validated_data):
        permissions_data = validated_data.pop('permissions', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if permissions_data is not None:
            instance.permissions.set(permissions_data)
        return instance
```

---

## 视图集实现

### PermissionViewSet

```python
from rest_framework import viewsets, permissions
from utils.response import api_response, api_error
from .models import Role, Permission
from .serializers import RoleSerializer, RoleCreateUpdateSerializer


class PermissionViewSet(viewsets.ModelViewSet):
    """
    权限视图集 - 提供权限的 CRUD 操作
    
    所有接口都使用统一响应格式（StandardResponse）
    """
    queryset = Permission.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PermissionSerializer

    def list(self, request, *args, **kwargs):
        """获取权限列表"""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return api_response(data=serializer.data, message='获取成功')

    def retrieve(self, request, *args, **kwargs):
        """获取权限详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_response(data=serializer.data, message='获取成功')

    def create(self, request, *args, **kwargs):
        """创建权限"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return api_response(
            data=serializer.data,
            message='创建成功',
            status=201
        )

    def update(self, request, *args, **kwargs):
        """更新权限"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return api_response(data=serializer.data, message='更新成功')

    def destroy(self, request, *args, **kwargs):
        """删除权限"""
        instance = self.get_object()
        instance.delete()
        return api_response(data=None, message='删除成功')
```

### RoleViewSet

```python
class RoleViewSet(viewsets.ModelViewSet):
    """
    角色视图集 - 提供角色的 CRUD 操作
    
    支持按权限过滤、分配权限等功能
    """
    queryset = Role.objects.all().prefetch_related('permissions')
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        """根据不同动作选择序列化器"""
        if self.action in ['create', 'update', 'partial_update']:
            return RoleCreateUpdateSerializer
        return RoleSerializer

    def list(self, request, *args, **kwargs):
        """获取角色列表（带分页）"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return api_response(data=serializer.data, message='获取成功')

    def retrieve(self, request, *args, **kwargs):
        """获取角色详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_response(data=serializer.data, message='获取成功')

    def create(self, request, *args, **kwargs):
        """创建角色"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return api_response(
            data=serializer.data,
            message='创建成功',
            status=201
        )

    def update(self, request, *args, **kwargs):
        """更新角色"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return api_response(data=serializer.data, message='更新成功')

    def destroy(self, request, *args, **kwargs):
        """删除角色"""
        instance = self.get_object()
        instance.delete()
        return api_response(data=None, message='删除成功')
    
    @action(detail=True, methods=['post'])
    def assign_permissions(self, request, pk=None):
        """
        为角色分配权限
        
        请求数据:
            permission_ids: 权限 ID 列表
        
        返回:
            更新后的角色信息
        """
        role = self.get_object()
        permission_ids = request.data.get('permission_ids', [])
        
        try:
            from django.db import transaction
            with transaction.atomic():
                role.permissions.set(permission_ids)
            
            return api_response(
                data=RoleSerializer(role).data,
                message='权限分配成功'
            )
        except Exception as e:
            return api_error(
                message=f'分配权限失败：{str(e)}',
                error_type='bad_request'
            )
```

---

## API 端点

### 权限接口

| 方法 | URL | 说明 |
|------|-----|------|
| GET | `/api/permissions/` | 获取权限列表 |
| POST | `/api/permissions/` | 创建权限 |
| GET | `/api/permissions/{id}/` | 获取权限详情 |
| PUT | `/api/permissions/{id}/` | 更新权限 |
| DELETE | `/api/permissions/{id}/` | 删除权限 |

### 角色接口

| 方法 | URL | 说明 |
|------|-----|------|
| GET | `/api/roles/` | 获取角色列表 |
| POST | `/api/roles/` | 创建角色 |
| GET | `/api/roles/{id}/` | 获取角色详情 |
| PUT | `/api/roles/{id}/` | 更新角色 |
| DELETE | `/api/roles/{id}/` | 删除角色 |
| POST | `/api/roles/{id}/assign_permissions/` | 分配权限 |

---

## 测试示例

### 使用 Postman 测试

1. 创建权限
   ```
   POST http://localhost:8000/api/permissions/
   Content-Type: application/json
   
   {
     "code": "content_create",
     "name": "创建内容",
     "description": "可以创建新内容"
   }
   ```

2. 创建角色并分配权限
   ```
   POST http://localhost:8000/api/roles/
   Content-Type: application/json
   
   {
     "code": "editor",
     "name": "编辑",
     "permissions": ["权限 ID"]
   }
   ```

3. 为已有角色分配权限
   ```
   POST http://localhost:8000/api/roles/{id}/assign_permissions/
   Content-Type: application/json
   
   {
     "permission_ids": ["权限 ID 1", "权限 ID 2"]
   }
   ```

---

## 关键知识点

### 1. UUID 主键

使用 UUID 而不是自增 ID：
- 更安全（不会暴露用户数量）
- 分布式友好
- 防止被猜测

### 2. ManyToManyField

角色和权限是多对多关系：
- 一个角色可以有多个权限
- 一个权限可以属于多个角色
- 使用 `set()` 方法设置关联

### 3. prefetch_related

预加载关联对象，避免 N+1 查询问题：
```python
queryset = Role.objects.all().prefetch_related('permissions')
```

### 4. 动态序列化器

根据不同动作使用不同的序列化器：
- 查询时使用完整序列化器
- 创建/更新时使用简化序列化器

### 5. 事务处理

使用数据库事务保证数据一致性：
```python
with transaction.atomic():
    role.permissions.set(permission_ids)
```

---

## 常见问题

### Q1: 为什么要用两个序列化器？

A: 分离读写逻辑：
- `RoleSerializer`: 用于查询，展示完整的权限信息
- `RoleCreateUpdateSerializer`: 用于创建/更新，允许写入权限 ID

### Q2: assign_permissions 为什么是自定义 action？

A: 因为这不是标准的 CRUD 操作，而是一个业务逻辑操作，需要特殊处理。

### Q3: 为什么要用 prefetch_related？

A: 避免 N+1 查询问题。如果不预加载，每次访问 `role.permissions` 都会执行一次数据库查询。

---

## 下一步

- [Users 应用视图集详解](backend_users.md)
- [Contents 应用视图集详解](backend_contents.md)
