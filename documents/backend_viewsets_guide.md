# Django REST Framework 视图集开发指南

## 适用对象
- Python Web 开发初学者至中级开发者
- 正在学习 DRF 的后端开发人员

## 技术栈
- Django 4.2 + DRF 3.14 + JWT 认证
- 项目类型：内容管理系统 (CMS)

> 💡 **说明**: 本文档是视图集开发的通用指南，讲解 DRF 的核心原理和最佳实践。
> 
> **实战教程**: 请查看 [`backend.md`](backend.md) 获取从零开始的完整开发流程。
> 
> **应用详解**: 各个应用的具体实现请查看对应的应用文档（Roles、Users、Contents 等）。

---

## 目录

1. [统一响应格式设计](#统一响应格式设计)
2. [视图集核心原理](#视图集核心原理)
3. [Roles 应用视图集详解](#roles-应用视图集详解)
4. [Users 应用视图集详解](#users-应用视图集详解)
5. [Contents 应用视图集详解](#contents-应用视图集详解)
6. [Categories 应用视图集详解](#categories-应用视图集详解)
7. [Tags 应用视图集详解](#tags-应用视图集详解)
8. [Comments 应用视图集详解](#comments-应用视图集详解)
9. [Media 应用视图集详解](#media-应用视图集详解)

---

## 统一响应格式设计

### 设计理念

**分层架构**：
```
┌─────────────────────────────────┐
│   ViewSet 层（业务代码）          │
│   使用 @auto_response 装饰器     │
├─────────────────────────────────┤
│   装饰器层（@auto_response）      │
│   自动包装返回值                  │
├─────────────────────────────────┤
│   工具函数层（api_response）      │
│   简化调用                        │
├─────────────────────────────────┤
│   基础类层（StandardResponse）    │
│   继承自 DRF Response             │
├─────────────────────────────────┤
│   中间件层（ErrorHandlerMiddleware）│
│   全局异常捕获                    │
└─────────────────────────────────┘
```

### 核心组件

#### 1. StandardResponse - 基础响应类

文件：`utils/response.py`

```python
from rest_framework.response import Response


class StandardResponse(Response):
    """
    统一 API 响应格式
    
    设计原则：
    1. 所有数据统一放在 data 字段中
    2. 成功和错误都使用统一的包装格式
    3. 分页时：保留 DRF 的分页格式在 data 中
    """
    
    def __init__(self, data=None, message='操作成功', code=0, status=200, error_type=None):
        response_data = {
            'code': code,
            'message': message,
            'data': data,
        }
        
        if error_type:
            response_data['error'] = error_type
        
        super().__init__(response_data, status=status)
```

**关键设计点**：
- ✅ **继承 DRF Response** - 保持兼容性
- ✅ **code 字段** - 业务状态码（0 表示成功）
- ✅ **message 字段** - 友好的提示信息
- ✅ **data 字段** - 实际返回的数据
- ✅ **error 字段** - 仅在错误时出现

#### 2. api_response / api_error - 便捷工具函数

```python
def api_response(data=None, message='操作成功', status=200):
    """简化版成功响应函数"""
    return StandardResponse(data=data, message=message, status=status)


def api_error(message, error_type='bad_request', code=None, status=400, data=None):
    """统一的错误响应函数"""
    return StandardResponse(
        data=data,
        message=message,
        code=code if code is not None else status,
        status=status,
        error_type=error_type
    )
```

#### 3. @auto_response - 自动化装饰器

文件：`utils/response_decorator.py`

```python
import functools
from utils.response import StandardResponse


def auto_response(func):
    """
    自动包装响应装饰器
    
    如果函数返回的不是 Response 对象，则自动使用 StandardResponse 包装
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        
        from rest_framework.response import Response
        if isinstance(result, Response):
            return result
        
        return StandardResponse(result)
    
    return wrapper
```

---

## 视图集核心原理

### ModelViewSet 提供的 5 个默认动作

```
list()      → GET /api/roles/          → 获取列表
create()    → POST /api/roles/         → 创建对象
retrieve()  → GET /api/roles/{id}/     → 获取详情
update()    → PUT /api/roles/{id}/     → 全量更新
partial_update() → PATCH /api/roles/{id}/ → 部分更新
destroy()   → DELETE /api/roles/{id}/  → 删除对象
```

### list() - 获取列表方法详解

```python
def list(self, request, *args, **kwargs):
    """
    获取角色列表（带分页）
    
    执行流程：
    1. 获取查询集 → get_queryset()
    2. 应用过滤器 → filter_queryset()
    3. 应用分页 → paginate_queryset()
    4. 序列化数据 → get_serializer()
    5. 返回响应 → api_response()
    """
    # 步骤 1: 获取基础查询集
    queryset = self.filter_queryset(self.get_queryset())
    
    # 步骤 2: 尝试应用分页
    page = self.paginate_queryset(queryset)
    
    if page is not None:
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
    
    serializer = self.get_serializer(queryset, many=True)
    return api_response(data=serializer.data, message='获取成功')
```

**关键方法解析**：

1. **get_queryset()** - 获取查询集
2. **filter_queryset()** - 应用过滤后端
3. **paginate_queryset()** - 应用分页
4. **get_serializer()** - 获取序列化器

### retrieve() - 获取详情方法详解

```python
def retrieve(self, request, *args, **kwargs):
    """获取单个对象详情"""
    instance = self.get_object()
    serializer = self.get_serializer(instance)
    return api_response(data=serializer.data, message='获取成功')
```

**get_object() 执行流程**：
1. 从 URL 中获取 pk 参数
2. 执行 queryset.get(pk=pk)
3. 检查对象权限
4. 返回找到的对象

### create() - 创建对象方法详解

```python
def create(self, request, *args, **kwargs):
    """创建新对象"""
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)
    return api_response(
        data=serializer.data,
        message='创建成功',
        status=201
    )
```

**关键步骤**：
1. 使用请求数据初始化序列化器
2. 验证数据（失败自动抛出 400 错误）
3. 保存到数据库（钩子方法）
4. 返回创建的对象

### update() - 更新对象方法详解

```python
def update(self, request, *args, **kwargs):
    """全量更新对象（PUT）"""
    partial = kwargs.pop('partial', False)
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=partial)
    serializer.is_valid(raise_exception=True)
    self.perform_update(serializer)
    return api_response(data=serializer.data, message='更新成功')
```

**PUT vs PATCH 的区别**：
- PUT - 全量更新（partial=False）
- PATCH - 部分更新（partial=True）

### destroy() - 删除对象方法详解

```python
def destroy(self, request, *args, **kwargs):
    """删除对象"""
    instance = self.get_object()
    self.perform_destroy(instance)
    return api_response(data=None, message='删除成功')
```

---

## 高级功能

### get_serializer_class() - 动态序列化器选择

```python
def get_serializer_class(self):
    """根据不同动作返回不同的序列化器类"""
    if self.action in ['create', 'update', 'partial_update']:
        return RoleCreateUpdateSerializer
    return RoleSerializer
```

**为什么需要这个？**
- 列表展示：只需要基本信息
- 创建/更新：需要所有可写字段
- 详情展示：需要完整信息包括关联对象

### @action 装饰器 - 自定义端点

```python
from rest_framework.decorators import action

@action(detail=True, methods=['post'])
def assign_permissions(self, request, pk=None):
    """
    为角色分配权限
    
    detail=True: 需要 pk
    methods=['post']: 只接受 POST 请求
    
    生成的 URL:
    POST /api/roles/{pk}/assign_permissions/
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

### 权限检查机制

```python
def get_permissions(self):
    """根据不同动作返回不同的权限类"""
    if self.action == 'login':
        return [AllowAny()]  # 任何人都可以登录
    elif self.action == 'create':
        return [AllowAny()]  # 任何人都可以注册
    elif self.action in ['list', 'destroy']:
        return [IsAdminUser()]  # 只有管理员可以查看/删除用户
    return [IsAuthenticated()]  # 其他操作需要登录
```

---

## 完整模板

可以直接套用的视图集模板：

```python
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from utils.response import api_response, api_error
from .models import MyModel
from .serializers import (
    MyModelSerializer,
    MyModelCreateSerializer,
    MyModelListSerializer
)


class MyModelViewSet(viewsets.ModelViewSet):
    """我的模型视图集"""
    queryset = MyModel.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    
    def get_serializer_class(self):
        if self.action == 'list':
            return MyModelListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return MyModelCreateSerializer
        return MyModelSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_admin:
            queryset = queryset.filter(author=self.request.user)
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return api_response(data=serializer.data, message='获取成功')
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return api_response(
            data=serializer.data,
            message='创建成功',
            status=201
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_response(data=serializer.data, message='获取成功')
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return api_response(data=serializer.data, message='更新成功')
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return api_response(data=None, message='删除成功')
    
    @action(detail=True, methods=['post'])
    def custom_action(self, request, pk=None):
        instance = self.get_object()
        try:
            # 执行业务逻辑
            return api_response(
                data=MyModelSerializer(instance).data,
                message='操作成功'
            )
        except ValueError as e:
            return api_error(message=str(e), error_type='bad_request')
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
```

---

## 下一步

查看各个应用的详细实现：

- [Roles 应用视图集详解](backend_roles.md)
- [Users 应用视图集详解](backend_users.md)
- [Contents 应用视图集详解](backend_contents.md)
- [Categories 应用视图集详解](backend_categories.md)
- [Tags 应用视图集详解](backend_tags.md)
- [Comments 应用视图集详解](backend_comments.md)
- [Media 应用视图集详解](backend_media.md)
