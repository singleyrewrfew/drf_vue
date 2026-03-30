# Contents 应用视图集详解

> 💡 **文档定位**: 本文档是 CMS 核心内容管理模块的完整实现指南，包含 Mixin 设计、Service 层等高级用法。
>
> **通用原理**: DRF 视图集的通用原理请查看 [`backend_viewsets_guide.md`](backend_viewsets_guide.md)
>
> **完整教程**: 从零开始的开发流程请查看 [`backend.md`](backend.md)

## 概述

Contents 应用是 CMS 系统的核心，提供内容管理功能。

**核心功能**：
- 内容的 CRUD
- 内容发布/归档
- 封面上传
- 多级过滤（分类、标签、作者）
- 搜索
- 浏览量统计
- 置顶功能

---

## 数据模型

### Content 模型

```python
# apps/contents/models.py

class Content(models.Model):
    """
    内容模型
    
    支持草稿、发布、归档等状态
    """
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('published', '已发布'),
        ('archived', '已归档'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, verbose_name='标题')
    slug = models.SlugField(unique=True, blank=True, verbose_name='URL 标识')
    content = models.TextField(verbose_name='内容')
    excerpt = models.TextField(blank=True, verbose_name='摘要')
    cover = models.ImageField(upload_to='covers/', null=True, blank=True, verbose_name='封面')
    
    # 状态
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='发布时间')
    archived_at = models.DateTimeField(null=True, blank=True, verbose_name='归档时间')
    
    # 关联
    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contents'
    )
    author = models.ForeignKey(
        'core.User',
        on_delete=models.CASCADE,
        related_name='contents'
    )
    tags = models.ManyToManyField(
        'tags.Tag',
        blank=True,
        related_name='contents'
    )
    
    # 统计
    view_count = models.PositiveIntegerField(default=0, verbose_name='浏览量')
    likes_count = models.PositiveIntegerField(default=0, verbose_name='点赞数')
    
    # 功能
    is_top = models.BooleanField(default=False, verbose_name='置顶')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'contents'
        verbose_name = '内容'
        ordering = ['-is_top', '-created_at']
    
    def increment_view_count(self):
        """增加浏览量"""
        from django.db.models import F
        self.view_count = F('view_count') + 1
        self.save(update_fields=['view_count'])
    
    def __str__(self):
        return self.title
```

---

## 序列化器

### ContentSerializer

```python
class ContentSerializer(serializers.ModelSerializer):
    """内容序列化器 - 用于详情展示"""
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        source='tags',
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Content
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt', 'cover',
            'status', 'published_at', 'archived_at',
            'category', 'author', 'tags', 'tag_ids',
            'view_count', 'likes_count', 'is_top',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
```

### ContentListSerializer

```python
class ContentListSerializer(serializers.ModelSerializer):
    """内容列表序列化器 - 简化版"""
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Content
        fields = [
            'id', 'title', 'slug', 'excerpt', 'cover',
            'status', 'published_at',
            'category', 'author', 'tags',
            'view_count', 'is_top',
            'created_at'
        ]
```

### ContentCreateUpdateSerializer

```python
class ContentCreateUpdateSerializer(serializers.ModelSerializer):
    """内容创建/更新序列化器"""
    
    class Meta:
        model = Content
        fields = [
            'title', 'content', 'excerpt', 'cover',
            'category', 'tags', 'is_top'
        ]
    
    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        content = Content.objects.create(**validated_data)
        if tags_data:
            content.tags.set(tags_data)
        return content
    
    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tags_data is not None:
            instance.tags.set(tags_data)
        return instance
```

---

## Mixin 设计

### ContentQuerySetMixin

```python
class ContentQuerySetMixin:
    """查询集混入类"""
    
    def get_queryset(self):
        """
        获取动态过滤后的查询集
        
        根据请求参数和用户角色对内容数据进行多层过滤
        """
        queryset = super().get_queryset()
        status_filter = self.request.query_params.get('status')
        
        if self.action == 'list':
            if self.request.user.is_authenticated:
                if self.request.user.is_admin or self.request.user.is_superuser:
                    # 管理员：可查看所有内容，可按状态过滤
                    if status_filter:
                        queryset = queryset.filter(status=status_filter)
                elif self.request.user.is_editor:
                    # 编辑：只能查看自己的内容，可按状态过滤
                    queryset = queryset.filter(author=self.request.user)
                    if status_filter:
                        queryset = queryset.filter(status=status_filter)
                else:
                    # 普通用户：只能查看已发布的内容
                    queryset = queryset.filter(status='published')
            else:
                # 未认证：只能查看已发布的内容
                queryset = queryset.filter(status='published')
        
        # 按分类过滤
        category_id = self.request.query_params.get('category')
        if category_id:
            try:
                import uuid
                uuid.UUID(category_id)
                queryset = queryset.filter(category_id=category_id)
            except (ValueError, AttributeError):
                from apps.categories.models import Category
                try:
                    category = Category.objects.get(slug=category_id)
                    queryset = queryset.filter(category_id=category.id)
                except Category.DoesNotExist:
                    queryset = queryset.none()
        
        # 按标签过滤
        tag_id = self.request.query_params.get('tag')
        if tag_id:
            try:
                uuid.UUID(tag_id)
                queryset = queryset.filter(tags__id=tag_id)
            except (ValueError, AttributeError):
                from apps.tags.models import Tag
                try:
                    tag = Tag.objects.get(slug=tag_id)
                    queryset = queryset.filter(tags__id=tag.id)
                except Tag.DoesNotExist:
                    queryset = queryset.none()
        
        # 按作者过滤
        author_id = self.request.query_params.get('author')
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        
        # 搜索
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)
        
        # 排序：置顶优先，然后按创建时间降序
        queryset = queryset.order_by('-is_top', '-created_at')
        
        return queryset
```

### ContentPermissionMixin

```python
class ContentPermissionMixin:
    """权限混入类"""
    
    def get_permissions(self):
        """
        根据不同动作返回不同的权限类
        
        权限规则：
        - list/retrieve: 允许任何人查看（只读）
        - create: 需要认证
        - update/delete: 需要是作者或管理员
        """
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticatedOrReadOnly]
        elif self.action in ['create']:
            return [permissions.IsAuthenticated]
        return [IsOwnerOrAdmin()]
```

### ContentSerializerMixin

```python
class ContentSerializerMixin:
    """序列化器混入类"""
    
    default_serializer_class = ContentSerializer
    
    def _get_serializer_mapping(self):
        """获取序列化器映射配置"""
        return {
            'list': ContentListSerializer,
            'create': ContentCreateUpdateSerializer,
            'update': ContentCreateUpdateSerializer,
            'partial_update': ContentCreateUpdateSerializer,
        }
    
    def get_serializer_class(self):
        """
        获取序列化器类
        
        优先使用 _get_serializer_mapping() 中的配置
        如果没有配置，使用 default_serializer_class
        """
        mapping = self._get_serializer_mapping()
        return mapping.get(self.action, self.default_serializer_class)
```

---

## 视图集实现

### ContentViewSet

```python
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.users.permissions import IsEditorUser, IsOwnerOrAdmin
from utils.mixins import SlugOrUUIDMixin
from utils.response import StandardResponse, api_error
from utils.response_decorator import auto_response
from services.content_service import ContentService
from .models import Content
from .serializers import ContentCreateUpdateSerializer, ContentListSerializer, ContentSerializer
from .mixins import ContentPermissionMixin, ContentSerializerMixin, ContentQuerySetMixin


class ContentViewSet(
    ContentQuerySetMixin,
    ContentPermissionMixin,
    ContentSerializerMixin,
    SlugOrUUIDMixin,
    viewsets.ModelViewSet
):
    """
    内容视图集 - 提供内容的 CRUD 操作及发布、归档功能
    
    使用 Mixin 模式的好处:
    1. 代码组织清晰，每个 Mixin 负责一块功能
    2. 易于测试和维护
    3. 可以复用到其他 ViewSet
    """
    queryset = Content.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    
    # 默认序列化器（用于 retrieve 等未配置的操作）
    default_serializer_class = ContentSerializer
    
    def perform_create(self, serializer):
        """
        创建内容时自动设置作者
        
        业务逻辑:
        1. 检查请求数据中是否有 author 字段
        2. 如果有 author：
           - 检查当前用户是否是管理员
           - 如果是，查找指定的作者并保存
           - 如果不是，忽略 author 字段
        3. 如果没有 author：
           - 自动设置当前用户为作者
        """
        author_id = self.request.data.get('author')
        if author_id and (self.request.user.is_admin or self.request.user.is_superuser):
            from apps.core.models import User
            try:
                author = User.objects.get(id=author_id)
                serializer.save(author=author)
                return
            except User.DoesNotExist:
                pass
        serializer.save(author=self.request.user)
    
    @auto_response
    def retrieve(self, request, *args, **kwargs):
        """
        检索单个内容并增加浏览次数
        
        URL: GET /api/contents/{pk}/
        权限：IsAuthenticatedOrReadOnly
        
        特性:
        - 使用 @auto_response 装饰器自动包装响应
        - 每次查看自动增加浏览计数
        """
        instance = self.get_object()
        instance.increment_view_count()
        serializer = self.get_serializer(instance)
        return serializer.data  # 装饰器会自动包装
    
    @extend_schema(request=None, responses=ContentSerializer)
    @action(detail=True, methods=['post'])
    @auto_response
    def publish(self, request, pk=None):
        """
        发布内容（仅限未发布的内容）
        
        URL: POST /api/contents/{pk}/publish/
        权限：IsEditorUser（来自 ContentPermissionMixin）
        
        业务逻辑:
        1. 检查内容状态（必须是 draft）
        2. 设置发布时间
        3. 更改状态为 published
        4. 保存到数据库
        """
        content = self.get_object()
        
        try:
            # 使用 Service 层处理业务逻辑
            service = ContentService()
            published_content = service.publish_content(content)
            return ContentSerializer(published_content).data
        except ValueError as e:
            return api_error(
                message=str(e),
                error_type='bad_request',
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @extend_schema(request=None, responses=ContentSerializer)
    @action(detail=True, methods=['post'])
    @auto_response
    def archive(self, request, pk=None):
        """
        归档内容
        
        URL: POST /api/contents/{pk}/archive/
        权限：IsAdminUser 或 IsAuthor
        """
        content = self.get_object()
        service = ContentService()
        archived_content = service.archive_content(content)
        return ContentSerializer(archived_content).data
    
    def list(self, request, *args, **kwargs):
        """
        获取内容列表（统一响应格式）
        
        URL: GET /api/contents/
        
        查询优化:
        - select_related('author', 'category'): 预加载关联对象
        - prefetch_related('tags'): 预加载多对多关系
        - paginate: 分页处理
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data).data
            return StandardResponse(paginated_data)
        
        serializer = self.get_serializer(queryset, many=True)
        return StandardResponse(serializer.data)
    
    @extend_schema(request=None, responses=ContentSerializer)
    @action(detail=True, methods=['post'])
    def upload_cover(self, request, pk=None):
        """
        上传封面图片
        
        URL: POST /api/contents/{pk}/upload_cover/
        权限：IsOwnerOrAdmin
        
        请求数据:
        - cover: 文件对象
        """
        content = self.get_object()
        cover = request.FILES.get('cover')
        
        if not cover:
            return api_error(
                message='请上传封面图片',
                error_type='bad_request',
                status=status.HTTP_400_BAD_REQUEST
            )
        
        content.cover = cover
        content.save(update_fields=['cover'])
        
        return StandardResponse(
            data=ContentSerializer(content).data,
            message='封面上传成功'
        )
```

---

## Service 层

### ContentService

```python
# services/content_service.py

from django.utils import timezone


class ContentService:
    """
    内容服务层
    
    职责:
    - 封装复杂的业务逻辑
    - 保持 ViewSet 简洁
    - 便于单元测试
    """
    
    def publish_content(self, content):
        """
        发布内容
        
        参数:
            content: Content 实例
        
        返回:
            发布后的 Content 实例
        
        异常:
            ValueError: 如果内容不是草稿状态
        """
        if content.status != 'draft':
            raise ValueError('只有草稿可以发布')
        
        content.status = 'published'
        content.published_at = timezone.now()
        content.save(update_fields=['status', 'published_at'])
        
        return content
    
    def archive_content(self, content):
        """
        归档内容
        
        参数:
            content: Content 实例
        
        返回:
            归档后的 Content 实例
        
        异常:
            ValueError: 如果内容已经是归档状态
        """
        if content.status == 'draft':
            raise ValueError('草稿不能归档')
        
        content.status = 'archived'
        content.archived_at = timezone.now()
        content.save(update_fields=['status', 'archived_at'])
        
        return content
```

---

## API 端点

| 方法 | URL | 说明 | 权限 |
|------|-----|------|------|
| GET | `/api/contents/` | 获取内容列表 | 公开 |
| POST | `/api/contents/` | 创建内容 | IsAuthenticated |
| GET | `/api/contents/{pk}/` | 获取内容详情 | 公开 |
| PUT | `/api/contents/{pk}/` | 更新内容 | IsOwnerOrAdmin |
| DELETE | `/api/contents/{pk}/` | 删除内容 | IsOwnerOrAdmin |
| POST | `/api/contents/{pk}/publish/` | 发布内容 | IsEditorUser |
| POST | `/api/contents/{pk}/archive/` | 归档内容 | IsAdmin/Author |
| POST | `/api/contents/{pk}/upload_cover/` | 上传封面 | IsOwnerOrAdmin |

---

## 关键知识点

### 1. Mixin 模式

将复杂的功能拆分成多个独立的 Mixin 类：
- **ContentQuerySetMixin**: 查询集相关
- **ContentPermissionMixin**: 权限相关
- **ContentSerializerMixin**: 序列化器相关

### 2. 动态查询集

根据用户角色和 URL 参数动态过滤：
```python
def get_queryset(self):
    queryset = super().get_queryset()
    
    # 按用户角色过滤
    if self.request.user.is_admin:
        pass  # 查看全部
    elif self.request.user.is_editor:
        queryset = queryset.filter(author=self.request.user)
    else:
        queryset = queryset.filter(status='published')
    
    # 按 URL 参数过滤
    category = self.request.query_params.get('category')
    if category:
        queryset = queryset.filter(category_id=category)
    
    return queryset
```

### 3. @auto_response 装饰器

自动包装响应，减少样板代码：
```python
@auto_response
def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)
    return serializer.data  # 自动包装为 StandardResponse
```

### 4. Service 层封装

将业务逻辑从 ViewSet 中分离：
```python
# ViewSet 中
service = ContentService()
published_content = service.publish_content(content)

# Service 中
def publish_content(self, content):
    if content.status != 'draft':
        raise ValueError('只有草稿可以发布')
    content.status = 'published'
    content.save()
    return content
```

### 5. F() 表达式

原子性更新字段值：
```python
from django.db.models import F

def increment_view_count(self):
    self.view_count = F('view_count') + 1
    self.save(update_fields=['view_count'])
```

---

## 测试示例

### 1. 创建并发布内容

```bash
# 创建内容
curl -X POST http://localhost:8000/api/contents/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "测试文章",
    "content": "这是测试内容",
    "category": "category-uuid"
  }'

# 发布内容
curl -X POST http://localhost:8000/api/contents/{id}/publish/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 2. 获取列表（带过滤）

```bash
# 按分类过滤
curl "http://localhost:8000/api/contents/?category=tech"

# 按标签过滤
curl "http://localhost:8000/api/contents/?tag=python"

# 搜索
curl "http://localhost:8000/api/contents/?search=Django"

# 组合过滤
curl "http://localhost:8000/api/contents/?category=tech&author=user-uuid&search=Vue"
```

---

## 常见问题

### Q1: 为什么要用 Mixin 模式？

A: 
- 代码组织更清晰
- 每个 Mixin 职责单一
- 易于测试和维护
- 可以复用到其他 ViewSet

### Q2: Service 层的作用是什么？

A:
- 封装业务逻辑
- 保持 ViewSet 简洁
- 便于单元测试
- 可以在多个地方复用

### Q3: 如何实现浏览量统计？

A:
- 使用 F() 表达式原子性增加
- 避免并发问题
- 只更新 view_count 字段提高效率

---

## 下一步

- [Categories 应用视图集详解](backend_categories.md)
- [Tags 应用视
