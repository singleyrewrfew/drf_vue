from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.users.permissions import IsEditorUser, IsOwnerOrAdmin
from utils.mixins import SlugOrUUIDMixin
from utils.response import StandardResponse, api_error, api_response
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
    """内容视图集 - 提供内容的 CRUD 操作及发布、归档功能"""
    queryset = Content.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    
    # 默认序列化器（用于 retrieve 等未配置的操作）
    default_serializer_class = ContentSerializer
    
    def _get_serializer_mapping(self):
        """获取序列化器映射配置"""
        return {
            'list': ContentListSerializer,
            'create': ContentCreateUpdateSerializer,
            'update': ContentCreateUpdateSerializer,
            'partial_update': ContentCreateUpdateSerializer,
        }
    
    def perform_create(self, serializer):
        """创建内容时自动设置作者（管理员可指定其他作者）"""
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
        """检索单个内容并增加浏览次数"""
        instance = self.get_object()
        instance.increment_view_count()
        serializer = self.get_serializer(instance)
        return serializer.data  # 装饰器会自动包装
    
    @extend_schema(request=None, responses=ContentSerializer)
    @action(detail=True, methods=['post'])
    @auto_response
    def publish(self, request, pk=None):
        """发布内容（仅限未发布的内容）"""
        content = self.get_object()
        try:
            service = ContentService()
            published_content = service.publish_content(content)
            return ContentSerializer(published_content).data  # 装饰器会自动包装
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
        """归档内容"""
        content = self.get_object()
        service = ContentService()
        archived_content = service.archive_content(content)
        return ContentSerializer(archived_content).data  # 装饰器会自动包装

    def get_queryset(self):
        """
        获取动态过滤后的查询集
        
        根据请求参数和用户角色对内容数据进行多层过滤：
        - 按用户角色过滤：
          * 管理员/超级用户：可查看所有内容，可按状态过滤
          * 编辑：只能查看自己的内容，可按状态过滤
          * 普通用户/未认证：只能查看已发布的内容
        - category 参数：通过分类 ID、slug 或 UUID 过滤内容
        - tag 参数：通过标签 ID、slug 或 UUID 过滤内容
        - author 参数：通过作者 ID 过滤内容
        - search 参数：按标题搜索内容
        - 结果按置顶状态和创建时间降序排列
        
        Returns:
            QuerySet: 经过过滤的内容查询集
        
        Raises:
            无
        """
        queryset = super().get_queryset()
        status_filter = self.request.query_params.get('status')
        
        if self.action == 'list':
            if self.request.user.is_authenticated:
                if self.request.user.is_admin or self.request.user.is_superuser:
                    if status_filter:
                        queryset = queryset.filter(status=status_filter)
                elif self.request.user.is_editor:
                    queryset = queryset.filter(author=self.request.user)
                    if status_filter:
                        queryset = queryset.filter(status=status_filter)
                else:
                    queryset = queryset.filter(status='published')
            else:
                queryset = queryset.filter(status='published')
        
        category_id = self.request.query_params.get('category')
        if category_id:
            # 支持通过 slug 或 UUID 查找分类
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
        tag_id = self.request.query_params.get('tag')
        if tag_id:
            # 支持通过 slug 或 UUID 查找标签
            try:
                import uuid
                uuid.UUID(tag_id)
                queryset = queryset.filter(tags__id=tag_id)
            except (ValueError, AttributeError):
                from apps.tags.models import Tag
                try:
                    tag = Tag.objects.get(slug=tag_id)
                    queryset = queryset.filter(tags__id=tag.id)
                except Tag.DoesNotExist:
                    queryset = queryset.none()
        author_id = self.request.query_params.get('author')
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)
        
        # 确保置顶文章排在前面
        queryset = queryset.order_by('-is_top', '-created_at')
        
        return queryset

    def list(self, request, *args, **kwargs):
        """
        获取内容列表（统一响应格式）
        
        重写父类方法以使用统一的响应格式。
        
        Args:
            request: HTTP 请求对象
            *args: 位置参数
            **kwargs: 关键字参数
        
        Returns:
            Response: 包含分页数据的统一格式响应，HTTP 状态码为 200
        
        Raises:
            无
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
        上传封面图
        
        封面图会保存到 covers/ 目录，而不是 media/{uploader.id}/ 目录
        这样可以与 Content 模型的 upload_to='covers/' 配置保持一致。
        
        Args:
            request: HTTP 请求对象，包含上传的文件数据
            pk: 内容的主键或 UUID
        
        Returns:
            Response: 包含上传后封面图数据的响应对象，HTTP 状态码为 201
        
        Raises:
            无
        """
        if 'file' not in request.FILES:
            return api_error(
                message='请上传文件',
                error_type='bad_request',
                status=status.HTTP_400_BAD_REQUEST
            )
        
        file = request.FILES['file']
        
        # 验证文件类型
        allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
        if file.content_type not in allowed_types:
            return api_error(
                message='只支持 JPG/PNG/GIF/WEBP 格式的图片',
                error_type='unsupported_media_type',
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
            )
        
        # 验证文件大小（最大 10MB）
        if file.size > 10 * 1024 * 1024:
            return api_error(
                message='图片大小不能超过 10MB',
                error_type='payload_too_large',
                status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
            )
        
        # 保存文件到 covers/ 目录
        from django.core.files.storage import default_storage
        import uuid
        
        # 生成唯一文件名
        ext = file.name.split('.')[-1]
        filename = f'{uuid.uuid4().hex}.{ext}'
        
        # 保存文件
        file_path = default_storage.save(f'covers/{filename}', file)
        
        # 返回文件 URL
        file_url = f'/media/covers/{filename}'
        
        return api_response({
            'url': file_url,
            'filename': filename
        }, message='封面图上传成功', status=status.HTTP_201_CREATED)
