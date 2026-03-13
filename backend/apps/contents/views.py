from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.users.permissions import IsEditorUser, IsOwnerOrAdmin

from .models import Content
from .serializers import ContentCreateUpdateSerializer, ContentListSerializer, ContentSerializer


class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.select_related('author', 'category').prefetch_related('tags')
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'

    def get_serializer_class(self):
        if self.action == 'list':
            return ContentListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ContentCreateUpdateSerializer
        return ContentSerializer

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs.get(lookup_url_kwarg)
        
        # 尝试通过 slug 或 UUID 查找
        try:
            # 首先尝试通过 UUID 查找
            import uuid
            uuid.UUID(lookup_value)
            return super().get_object()
        except (ValueError, AttributeError):
            # 如果不是有效的 UUID，尝试通过 slug 查找
            try:
                obj = Content.objects.get(slug=lookup_value)
                self.check_object_permissions(self.request, obj)
                return obj
            except Content.DoesNotExist:
                from django.http import Http404
                raise Http404('No Content matches the given query.')

    def get_permissions(self):
        if self.action in ['create']:
            return [IsEditorUser()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return super().get_permissions()

    def perform_create(self, serializer):
        author_id = self.request.data.get('author')
        if author_id and (self.request.user.is_admin or self.request.user.is_superuser):
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                author = User.objects.get(id=author_id)
                serializer.save(author=author)
                return
            except User.DoesNotExist:
                pass
        serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.increment_view_count()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @extend_schema(request=None, responses=ContentSerializer)
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        content = self.get_object()
        if content.status == 'published':
            return Response({'message': '内容已发布'}, status=status.HTTP_400_BAD_REQUEST)
        content.status = 'published'
        content.published_at = timezone.now()
        content.save()
        return Response(ContentSerializer(content).data)

    @extend_schema(request=None, responses=ContentSerializer)
    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        content = self.get_object()
        content.status = 'archived'
        content.save()
        return Response(ContentSerializer(content).data)

    def get_queryset(self):
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
