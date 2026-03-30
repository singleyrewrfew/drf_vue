# Categories & Tags & Comments & Media 应用视图集详解

> 💡 **文档定位**: 本文档是辅助功能模块的精简版实现指南，包含树形结构、聚合查询、文件上传等实用技术。
>
> **通用原理**: DRF 视图集的通用原理请查看 [`backend_viewsets_guide.md`](backend_viewsets_guide.md)
>
> **完整教程**: 从零开始的开发流程请查看 [`backend.md`](backend.md)

## Categories 应用

### 核心功能
- 分类的 CRUD
- 树形结构支持（父子分类）
- 统计每个分类的文章数量

### 数据模型

```python
class Category(models.Model):
    """分类模型（支持树形结构）"""
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
```

### 视图集关键代码

```python
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def tree(self, request):
        """获取分类树形结构"""
        queryset = self.get_queryset().filter(parent__isnull=True)
        serializer = self.get_serializer(queryset, many=True)
        return api_response(data=serializer.data)
    
    @action(detail=True, methods=['get'])
    def children(self, request, pk=None):
        """获取某个分类的所有子分类"""
        parent = self.get_object()
        children = parent.children.all()
        serializer = self.get_serializer(children, many=True)
        return api_response(data=serializer.data)
```

### API 端点

| 方法 | URL | 说明 |
|------|-----|------|
| GET | `/api/categories/` | 获取分类列表 |
| POST | `/api/categories/` | 创建分类 |
| GET | `/api/categories/{id}/` | 获取分类详情 |
| GET | `/api/categories/tree/` | 获取分类树 |
| GET | `/api/categories/{id}/children/` | 获取子分类 |

---

## Tags 应用

### 核心功能
- 标签的 CRUD
- 按标签过滤内容
- 热门标签统计

### 视图集关键代码

```python
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        """获取标签列表（带使用统计）"""
        from django.db.models import Count
        queryset = self.get_queryset().annotate(
            usage_count=Count('contents')
        )
        ordering = request.query_params.get('ordering', '-usage_count')
        queryset = queryset.order_by(ordering)
        serializer = self.get_serializer(queryset, many=True)
        return api_response(data=serializer.data)
    
    @action(detail=True, methods=['get'])
    def contents(self, request, pk=None):
        """获取使用该标签的所有内容"""
        tag = self.get_object()
        contents = tag.contents.filter(status='published')
        serializer = ContentListSerializer(contents, many=True)
        return api_response(data=serializer.data)
```

### API 端点

| 方法 | URL | 说明 |
|------|-----|------|
| GET | `/api/tags/` | 获取标签列表 |
| POST | `/api/tags/` | 创建标签 |
| GET | `/api/tags/{id}/` | 获取标签详情 |
| GET | `/api/tags/{id}/contents/` | 获取相关内容 |

---

## Comments 应用

### 核心功能
- 评论的 CRUD
- 嵌套评论（回复功能）
- 评论审核
- 点赞/点踩

### 数据模型

```python
class Comment(models.Model):
    """评论模型（支持嵌套）"""
    content = models.ForeignKey('contents.Content', on_delete=models.CASCADE)
    author = models.ForeignKey('core.User', on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    body = models.TextField()
    likes = models.ManyToManyField('core.User', related_name='liked_comments')
    dislikes = models.ManyToManyField('core.User', related_name='disliked_comments')
    status = models.CharField(
        max_length=10,
        choices=[('pending', '待审核'), ('approved', '已通过'), ('rejected', '已拒绝')],
        default='pending'
    )
```

### 视图集关键代码

```python
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('author', 'content').all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        """创建评论时自动设置作者和内容"""
        content_id = self.request.data.get('content')
        parent_id = self.request.data.get('parent')
        
        from apps.contents.models import Content
        content = Content.objects.get(id=content_id)
        
        parent = None
        if parent_id:
            parent = Comment.objects.get(id=parent_id)
        
        serializer.save(author=self.request.user, content=content, parent=parent)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """审核通过评论"""
        comment = self.get_object()
        comment.status = 'approved'
        comment.save()
        return api_response(data=CommentSerializer(comment).data)
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """点赞评论"""
        comment = self.get_object()
        user = request.user
        
        if user in comment.likes.all():
            comment.likes.remove(user)
        else:
            comment.likes.add(user)
        
        return api_response(data={
            'likes_count': comment.likes.count(),
            'is_liked': user in comment.likes.all()
        })
```

### API 端点

| 方法 | URL | 说明 |
|------|-----|------|
| GET | `/api/comments/` | 获取评论列表 |
| POST | `/api/comments/` | 创建评论 |
| POST | `/api/comments/{id}/approve/` | 审核评论 |
| POST | `/api/comments/{id}/like/` | 点赞评论 |
| POST | `/api/comments/{id}/dislike/` | 点踩评论 |

---

## Media 应用

### 核心功能
- 文件上传（图片、视频、文档）
- 文件管理（列表、删除）
- 流媒体播放
- 文件类型识别

### 数据模型

```python
class Media(models.Model):
    """媒体文件模型"""
    FILE_TYPE_CHOICES = (
        ('image', '图片'),
        ('video', '视频'),
        ('audio', '音频'),
        ('document', '文档'),
        ('other', '其他'),
    )
    
    file = models.FileField(upload_to='uploads/')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES)
    file_size = models.PositiveIntegerField()
    uploaded_by = models.ForeignKey('core.User', on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
```

### 视图集关键代码

```python
class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def create(self, request, *args, **kwargs):
        """上传文件"""
        uploaded_file = request.FILES.get('file')
        
        if not uploaded_file:
            return api_error(message='未选择文件', error_type='bad_request')
        
        # 生成唯一文件名
        import uuid
        file_extension = os.path.splitext(uploaded_file.name)[1]
        unique_filename = f"{uuid.uuid4().hex}{file_extension}"
        upload_path = os.path.join('uploads', unique_filename)
        
        # 保存文件
        file_path = default_storage.save(upload_path, uploaded_file)
        
        # 创建数据库记录
        media = Media.objects.create(
            file=file_path,
            title=request.data.get('title', uploaded_file.name),
            file_type=self._detect_file_type(uploaded_file),
            file_size=uploaded_file.size,
            uploaded_by=request.user
        )
        
        serializer = self.get_serializer(media)
        return api_response(data=serializer.data, status=201)
    
    @action(detail=True, methods=['get'])
    def stream(self, request, pk=None):
        """流媒体播放"""
        media = self.get_object()
        file_path = media.file.path
        
        if not os.path.exists(file_path):
            return api_error(message='文件不存在', error_type='not_found')
        
        response = FileResponse(open(file_path, 'rb'))
        return response
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """下载文件"""
        media = self.get_object()
        response = FileResponse(
            open(media.file.path, 'rb'),
            as_attachment=True,
            filename=media.title
        )
        return response
```

### API 端点

| 方法 | URL | 说明 |
|------|-----|------|
| POST | `/api/media/` | 上传文件 |
| GET | `/api/media/` | 获取媒体列表 |
| GET | `/api/media/{id}/` | 获取媒体详情 |
| DELETE | `/api/media/{id}/` | 删除媒体 |
| GET | `/api/media/{id}/stream/` | 流媒体播放 |
| GET | `/api/media/{id}/download/` | 下载文件 |

---

## 关键知识点总结

### 1. 树形结构实现

使用自引用外键：
```python
parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children')
```

递归序列化：
```python
def get_children(self, obj):
    children = obj.children.all()
    if children.exists():
        return CategoryTreeSerializer(children, many=True).data
    return []
```

### 2. 聚合查询

统计使用次数：
```python
from django.db.models import Count
Tag.objects.annotate(usage_count=Count('contents'))
```

### 3. 嵌套评论

使用自引用外键实现回复功能：
```python
parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies')
```

### 4. 文件上传

使用 MultiPartParser 处理文件：
```python
parser_classes = [MultiPartParser, FormParser]
uploaded_file = request.FILES.get('file')
```

### 5. 流媒体播放

使用 FileResponse 并支持 Range 请求：
```python
response = FileResponse(open(file_path, 'rb'))
# Django 会自动处理 Range 头，实现拖动进度条
```

---

## 下一步

- [返回主文档](backend_viewsets_guide.md)
- [Roles 应用视图集详解](backend_roles.md)
- [Users 应用视图集详解](backend_users.md)
- [Contents 应用视图集详解](backend_contents.md)
