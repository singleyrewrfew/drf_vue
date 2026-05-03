from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django.conf import settings
from services.content_service import ContentService
from utils.cache_utils import get_cache_key, invalidate_pattern
from utils.query_utils import get_object_by_slug_or_id
from utils.response import StandardResponse, api_error
from utils.viewset_mixins import CachedListMixin, SlugOrUUIDMixin
from .mixins import ContentPermissionMixin, ContentSerializerMixin, ContentQuerySetMixin
from .models import Content
from .serializers import ContentCreateUpdateSerializer, ContentListSerializer, ContentSerializer


class ContentViewSet(
    CachedListMixin,
    SlugOrUUIDMixin,
    ContentQuerySetMixin,
    ContentPermissionMixin,
    ContentSerializerMixin,
    viewsets.ModelViewSet
):
    """内容视图集 - 提供内容的 CRUD 操作及发布、归档功能"""
    queryset = Content.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    cache_key_prefix = 'contents:list'
    cache_timeout = settings.CACHE_TTL['CONTENT_LIST']

    default_serializer_class = ContentSerializer
    
    # 有效的状态值白名单（防止 SQL 注入）
    VALID_STATUSES = dict(Content.STATUS_CHOICES).keys()

    def _invalidate_cache(self):
        """内容变更时，同时清除列表、统计和热门作者缓存"""
        super()._invalidate_cache()
        invalidate_pattern('stats')
        invalidate_pattern('popular_authors')

    def get_cache_scope(self, request):
        """
        内容列表按数据范围隔离缓存

        - admin/superuser: 看全部内容 → scope='all'
        - editor: 只看自己的内容 → scope='own:{user_id}'（必须按 user_id 隔离，否则不同编辑会看到彼此的数据）
        - 普通用户/匿名: 只看已发布 → scope='published'
        """
        if request.user.is_authenticated:
            if request.user.is_admin or request.user.is_superuser:
                return 'all'
            elif request.user.is_editor:
                return f'own:{request.user.id}'
        return 'published'

    def _get_cache_key(self, request):
        """
        内容列表额外受查询参数影响（category/tag/search/status 等），
        需要将查询参数拼入缓存 key，否则不同筛选条件会命中同一份缓存
        """
        scope = self.get_cache_scope(request)
        query_params = '&'.join(
            f'{k}={v}' for k, v in sorted(request.query_params.items())
        )
        return get_cache_key(self.cache_key_prefix, scope, query_params)

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
                self._invalidate_cache()
                return
            except User.DoesNotExist:
                pass
        serializer.save(author=self.request.user)
        self._invalidate_cache()

    def retrieve(self, request, *args, **kwargs):
        """检索单个内容并增加浏览次数"""
        instance = self.get_object()
        instance.increment_view_count()
        serializer = self.get_serializer(instance)
        return StandardResponse(serializer.data)

    @extend_schema(request=None, responses=ContentSerializer)
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """发布内容（仅限未发布的内容）"""
        content = self.get_object()
        published_content = ContentService.publish_content(content, request.user)
        self._invalidate_cache()
        serializer = self.get_serializer(published_content)
        return StandardResponse(serializer.data)

    @extend_schema(request=None, responses=ContentSerializer)
    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        """归档内容"""
        content = self.get_object()
        archived_content = ContentService.archive_content(content, request.user)
        self._invalidate_cache()
        serializer = self.get_serializer(archived_content)
        return StandardResponse(serializer.data)

    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.query_params.get('status')

        if self.action == 'list':
            if self.request.user.is_authenticated:
                if self.request.user.is_admin or self.request.user.is_superuser:
                    if status_filter:
                        # 验证状态值是否在白名单中（防止 SQL 注入）
                        if status_filter not in self.VALID_STATUSES:
                            raise ValidationError(f"无效的状态值: {status_filter}。允许的值: {', '.join(self.VALID_STATUSES)}")
                        queryset = queryset.filter(status=status_filter)
                elif self.request.user.is_editor:
                    queryset = queryset.filter(author=self.request.user)
                    if status_filter:
                        # 验证状态值是否在白名单中（防止 SQL 注入）
                        if status_filter not in self.VALID_STATUSES:
                            raise ValidationError(f"无效的状态值: {status_filter}。允许的值: {', '.join(self.VALID_STATUSES)}")
                        queryset = queryset.filter(status=status_filter)
                else:
                    queryset = queryset.filter(status='published')
            else:
                queryset = queryset.filter(status='published')

        category_id = self.request.query_params.get('category')
        if category_id:
            from apps.categories.models import Category
            category = get_object_by_slug_or_id(Category, category_id)
            queryset = queryset.filter(category=category) if category else queryset.none()

        tag_id = self.request.query_params.get('tag')
        if tag_id:
            from apps.tags.models import Tag
            tag = get_object_by_slug_or_id(Tag, tag_id)
            queryset = queryset.filter(tags=tag) if tag else queryset.none()

        author_id = self.request.query_params.get('author')
        if author_id:
            queryset = queryset.filter(author_id=author_id)

        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)

        return queryset.order_by('-is_top', '-created_at')

