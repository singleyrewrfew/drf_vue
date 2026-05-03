from django.db.models import Count, Prefetch, Q
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.request import Request

from apps.users.permissions import IsOwnerOrAdmin
from services.comment_service import CommentService
from utils.response import StandardResponse
from utils.viewset_mixins import StandardListMixin
from .models import Comment, CommentLike
from .serializers import CommentCreateSerializer, CommentListSerializer, CommentSerializer


class CommentViewSet(StandardListMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('user', 'article', 'parent', 'reply_to')
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return CommentListSerializer
        elif self.action == 'create':
            return CommentCreateSerializer
        return CommentSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        elif self.action in ['approve', 'like']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        queryset = super().get_queryset()
        request: Request = self.request

        if self.action == 'list':
            show_all = request.query_params.get('all')
            show_my = request.query_params.get('my')

            if show_my and self.request.user.is_authenticated:
                queryset = queryset.filter(user=self.request.user)
            elif show_all and request.user.is_authenticated and request.user.is_editor:
                pass
            else:
                queryset = queryset.filter(is_approved=True, parent__isnull=True)

            queryset = queryset.annotate(reply_count=Count('replies', filter=Q(replies__is_approved=True)))

            approved_replies = Comment.objects.filter(is_approved=True).select_related('user', 'reply_to')
            queryset = queryset.prefetch_related(
                Prefetch('replies', queryset=approved_replies, to_attr='prefetched_replies')
            )

            if request.user.is_authenticated:
                self._liked_comment_ids = CommentService.get_user_liked_comment_ids(request.user)

        article_id = request.query_params.get('article')
        if article_id:
            from utils.query_utils import get_object_by_slug_or_id
            from apps.contents.models import Content

            article = get_object_by_slug_or_id(Content, article_id)
            if article:
                queryset = queryset.filter(article_id=article.id)
            else:
                queryset = queryset.none()

        is_approved = request.query_params.get('is_approved')
        if is_approved is not None and request.user.is_authenticated:
            if request.user.is_editor:
                # 验证 is_approved 参数是否为有效的布尔值字符串
                if is_approved.lower() not in ['true', 'false']:
                    raise ValidationError(f"无效的 is_approved 值: {is_approved}。允许的值: true, false")
                queryset = queryset.filter(is_approved=is_approved.lower() == 'true')

        return queryset

    @extend_schema(request=None, responses=CommentSerializer)
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        comment = self.get_object()
        comment = CommentService.approve_comment(comment)
        return StandardResponse(CommentSerializer(comment).data)

    @extend_schema(request=None, responses=CommentSerializer)
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        comment = self.get_object()
        
        # 检查点赞频率限制
        from services.comment_service import CommentService
        CommentService.check_like_rate_limit(request.user)
        
        comment, is_liked = CommentService.toggle_like(comment, request.user)
        return StandardResponse(CommentSerializer(comment, context={'request': request}).data)
