# Users 应用视图集详解

> 💡 **文档定位**: 本文档是 Users 应用的完整实现指南，包含认证、用户管理、JWT 等核心功能。
>
> **通用原理**: DRF 视图集的通用原理请查看 [`backend_viewsets_guide.md`](backend_viewsets_guide.md)
>
> **完整教程**: 从零开始的开发流程请查看 [`backend.md`](backend.md)

## 概述

Users 应用提供用户管理、认证、个人信息管理等功能。

**核心功能**：
- 用户注册
- 用户登录（JWT 认证）
- 获取/更新用户信息
- 修改密码
- 获取热门作者
- 仪表盘统计数据

---

## 数据模型

### User 模型（自定义用户模型）

```python
# apps/core/models.py

class User(AbstractUser):
    """
    自定义用户模型
    
    扩展 Django 内置的 AbstractUser
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    role = models.ForeignKey(
        'roles.Role',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )
    bio = models.TextField(blank=True, verbose_name='个人简介')
    is_editor = models.BooleanField(default=False, verbose_name='编辑权限')
    is_admin = models.BooleanField(default=False, verbose_name='管理员权限')
    
    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
```

---

## 序列化器

### UserRegisterSerializer

```python
class UserRegisterSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("两次密码不一致")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user
```

### UserSerializer

```python
class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    role = RoleSerializer(read_only=True)
    article_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'avatar', 'role',
            'bio', 'is_staff', 'is_editor', 'is_admin',
            'article_count', 'comment_count', 'date_joined'
        ]
        read_only_fields = fields

    def get_article_count(self, obj):
        return obj.contents.filter(status='published').count()

    def get_comment_count(self, obj):
        return obj.comments.count()
```

### UserUpdateSerializer

```python
class UserUpdateSerializer(serializers.ModelSerializer):
    """用户更新序列化器"""
    avatar_url = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['email', 'avatar', 'avatar_url', 'bio', 'role']

    def update(self, instance, validated_data):
        avatar_url = validated_data.pop('avatar_url', None)
        if avatar_url:
            instance.avatar = avatar_url
        return super().update(instance, validated_data)
```

### PasswordChangeSerializer

```python
class PasswordChangeSerializer(serializers.Serializer):
    """密码修改序列化器"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    confirm_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("原密码错误")
        return value

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("两次输入的新密码不一致")
        return data

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
```

---

## 视图集实现

### UserViewSet

```python
from django.db import models
from django.db.models import Count, Sum
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from apps.comments.models import Comment
from apps.contents.models import Content
from apps.core.models import User
from apps.media.models import Media
from .permissions import IsAdminUser
from .serializers import (
    PasswordChangeSerializer,
    UserRegisterSerializer,
    UserSerializer,
    UserUpdateSerializer,
)
from utils.response import StandardResponse


class UserViewSet(viewsets.ModelViewSet):
    """
    用户视图集
    
    提供用户相关的 API 端点：
    - 登录、登出
    - 获取用户信息
    - 更新用户信息
    - 修改密码
    - 获取热门作者
    - 获取仪表盘统计数据
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # 支持多种解析器：表单、JSON、多部分（文件上传）
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    
    def get_permissions(self):
        """
        根据不同的操作返回不同的权限类
        
        权限规则：
        - login: 允许任何人访问
        - create: 允许任何人注册
        - list: 仅管理员可查看所有用户
        - destroy: 仅管理员可删除用户
        - 其他：需要认证
        """
        if self.action == 'login':
            return [AllowAny()]
        elif self.action == 'create':
            return [AllowAny()]
        elif self.action in ['list', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        """
        根据不同的操作返回不同的序列化器
        
        序列化器映射：
        - create: UserRegisterSerializer（注册）
        - update/partial_update: UserUpdateSerializer（更新）
        - 其他：UserSerializer（读取）
        """
        if self.action == 'create':
            return UserRegisterSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """
        用户登录（JWT 认证）
        
        URL: POST /api/users/login/
        权限：AllowAny（任何人都可以访问）
        
        请求数据:
            {
                "username": "zhangsan",
                "password": "TestPass123!"
            }
        
        步骤：
        1. 获取用户名和密码
        2. 验证用户名和密码不为空
        3. 查询用户是否存在
        4. 验证密码是否正确
        5. 验证账户是否激活
        6. 生成访问令牌和刷新令牌
        7. 返回用户信息和令牌
        """
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return api_error(
                message='用户名和密码不能为空',
                error_type='bad_request',
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return api_error(
                message='用户不存在',
                error_type='unauthorized',
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.check_password(password):
            return api_error(
                message='密码错误',
                error_type='unauthorized',
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.is_active:
            return api_error(
                message='账户已被禁用',
                error_type='forbidden',
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 生成 JWT 令牌
        refresh = RefreshToken.for_user(user)
        return StandardResponse({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        })
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        """
        获取当前登录用户的个人信息
        
        URL: GET /api/users/profile/
        权限：IsAuthenticated
        
        返回完整的用户信息，包括计算属性
        """
        serializer = UserSerializer(request.user)
        return StandardResponse(serializer.data)
    
    @action(detail=False, methods=['put', 'patch', 'post'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        """
        更新用户个人信息
        
        URL: PUT/PATCH/POST /api/users/update_profile/
        权限：IsAuthenticated
        
        支持的字段：
        - email: 邮箱
        - avatar: 头像（支持文件对象或 URL）
        - role: 角色
        - is_staff: 是否为后台用户
        """
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return StandardResponse(UserSerializer(request.user).data)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """
        修改用户密码
        
        URL: POST /api/users/change_password/
        权限：IsAuthenticated
        
        步骤：
        1. 验证原密码
        2. 验证新密码和确认密码
        3. 更新密码
        """
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return StandardResponse({'message': '密码修改成功'})
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def logout(self, request):
        """
        用户登出
        
        URL: POST /api/users/logout/
        权限：AllowAny
        
        步骤：
        1. 获取刷新令牌
        2. 将令牌加入黑名单
        3. 返回成功消息
        """
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except Exception:
            pass
        return StandardResponse({'message': '退出成功'})
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def popular(self, request):
        """
        获取热门作者列表
        
        URL: GET /api/users/popular/
        权限：IsAuthenticated
        
        排序规则：
        - 按已发布的文章数量降序
        - 返回前 10 名
        """
        users = User.objects.annotate(
            article_count=Count(
                'contents',
                filter=models.Q(contents__status='published')
            )
        ).order_by('-article_count')[:10]
        
        serializer = UserSerializer(users, many=True)
        return StandardResponse(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def dashboard_stats(self, request):
        """
        获取仪表盘统计数据
        
        URL: GET /api/users/dashboard_stats/
        权限：IsAuthenticated
        
        返回：
        - 文章总数
        - 评论总数
        - 获得的点赞数
        - 浏览量总数
        """
        user = request.user
        
        stats = {
            'article_count': Content.objects.filter(author=user).count(),
            'comment_count': Comment.objects.filter(author=user).count(),
            'total_likes': Content.objects.filter(author=user).aggregate(
                total=Sum('likes_count')
            )['total'] or 0,
            'total_views': Content.objects.filter(author=user).aggregate(
                total=Sum('view_count')
            )['total'] or 0,
        }
        
        return StandardResponse(stats)
```

---

## API 端点

| 方法 | URL | 说明 | 权限 |
|------|-----|------|------|
| POST | `/api/users/login/` | 用户登录 | AllowAny |
| POST | `/api/users/logout/` | 用户登出 | AllowAny |
| POST | `/api/users/` | 用户注册 | AllowAny |
| GET | `/api/users/` | 获取用户列表 | IsAdminUser |
| GET | `/api/users/{id}/` | 获取用户详情 | IsAuthenticated |
| GET | `/api/users/profile/` | 获取当前用户信息 | IsAuthenticated |
| PUT/PATCH | `/api/users/update_profile/` | 更新用户信息 | IsAuthenticated |
| POST | `/api/users/change_password/` | 修改密码 | IsAuthenticated |
| GET | `/api/users/popular/` | 获取热门作者 | IsAuthenticated |
| GET | `/api/users/dashboard_stats/` | 获取仪表盘统计 | IsAuthenticated |

---

## 关键知识点

### 1. JWT 认证流程

```python
from rest_framework_simplejwt.tokens import RefreshToken

# 为用户生成令牌
refresh = RefreshToken.for_user(user)
access_token = str(refresh.access_token)
refresh_token = str(refresh)
```

**令牌的用途**：
- **Access Token**：短期有效，用于 API 请求认证
- **Refresh Token**：长期有效，用于刷新 Access Token

### 2. check_password()

Django 内置的密码验证方法，使用 PBKDF2 算法：
```python
user.check_password('plain_password')  # 返回 True/False
```

### 3. annotate() 聚合查询

```python
from django.db.models import Count

# 为每个用户添加文章数量统计
User.objects.annotate(
    article_count=Count(
        'contents',
        filter=models.Q(contents__status='published')
    )
)
```

### 4. 动态权限控制

```python
def get_permissions(self):
    """根据不同动作返回不同的权限类"""
    if self.action == 'login':
        return [AllowAny()]
    elif self.action == 'create':
        return [AllowAny()]
    elif self.action in ['list', 'destroy']:
        return [IsAdminUser()]
    return [IsAuthenticated()]
```

### 5. 多解析器支持

```python
parser_classes = [JSONParser, MultiPartParser, FormParser]
```

- **JSONParser**：处理 JSON 格式的请求体
- **MultiPartParser**：处理文件上传（multipart/form-data）
- **FormParser**：处理表单数据（application/x-www-form-urlencoded）

---

## 测试示例

### 1. 用户登录

```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "zhangsan",
    "password": "TestPass123!"
  }'
```

**响应示例**：
```json
{
  "code": 0,
  "message": "操作成功",
  "data": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user": {
      "id": "uuid...",
      "username": "zhangsan",
      "email": "test@example.com",
      "role": {...}
    }
  }
}
```

### 2. 获取当前用户信息

```bash
curl -X GET http://localhost:8000/api/users/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 3. 更新用户信息

```bash
# PATCH - 部分更新
curl -X PATCH http://localhost:8000/api/users/update_profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "bio": "这是我的个人简介"
  }'

# PUT - 全量更新
curl -X PUT http://localhost:8000/api/users/update_profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "new@example.com",
    "bio": "新的简介",
    "avatar": "..."
  }'
```

### 4. 修改密码

```bash
curl -X POST http://localhost:8000/api/users/change_password/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "OldPass123",
    "new_password": "NewPass456!",
    "confirm_password": "NewPass456!"
  }'
```

### 5. 获取热门作者

```bash
curl -X GET http://localhost:8000/api/users/popular/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 常见问题

### Q1: 为什么要用 JWT 而不是 Session？

A: 
- **JWT**：无状态，适合前后端分离和分布式系统
- **Session**：有状态，需要服务器存储 session 数据
- JWT 更适合 RESTful API

### Q2: Access Token 和 Refresh Token 有什么区别？

A:
- **Access Token**：有效期短（如 1 小时），用于 API 请求
- **Refresh Token**：有效期长（如 7 天），用于刷新 Access Token
- 这种设计提高了安全性

### Q3: 如何实现令牌刷新？

A:
```python
from rest_framework_simplejwt.tokens import RefreshToken

refresh = RefreshToken(refresh_token_from_client)
new_access_token = str(refresh.access_token)
```

### Q4: 为什么要用 parser_classes？

A:
- 支持多种请求格式
- 文件上传需要 MultiPartParser
- JSON 请求需要 JSONParser
- 表单提交需要 FormParser

---

## 下一步

- [Contents 应用视图集详解](backend_contents.md)
- [Categories 应用视图集详解](backend_categories.md)
