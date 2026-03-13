from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.users.permissions import IsEditorUser, IsOwnerOrAdmin

from .models import Comment, CommentLike
from .serializers import CommentCreateSerializer, CommentListSerializer, CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('user', 'article', 'parent')
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
        if self.action == 'list':
            show_all = self.request.query_params.get('all')
            if show_all and self.request.user.is_authenticated and self.request.user.is_editor:
                return queryset
            queryset = queryset.filter(is_approved=True, parent__isnull=True)
        article_id = self.request.query_params.get('article')
        if article_id:
            # 支持通过 slug 或 UUID 查找文章
            try:
                import uuid
                uuid.UUID(article_id)
                queryset = queryset.filter(article_id=article_id)
            except (ValueError, AttributeError):
                # 如果不是有效的 UUID，尝试通过 slug 查找
                from apps.contents.models import Content
                try:
                    article = Content.objects.get(slug=article_id)
                    queryset = queryset.filter(article_id=article.id)
                except Content.DoesNotExist:
                    queryset = queryset.none()
        is_approved = self.request.query_params.get('is_approved')
        if is_approved is not None and self.request.user.is_authenticated:
            if self.request.user.is_editor:
                queryset = queryset.filter(is_approved=is_approved.lower() == 'true')
        return queryset

    @extend_schema(request=None, responses=CommentSerializer)
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        comment = self.get_object()
        comment.is_approved = True
        comment.save()
        return Response(CommentSerializer(comment).data)

    @extend_schema(request=None, responses=CommentSerializer)
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        comment = self.get_object()
        like, created = CommentLike.objects.get_or_create(
            comment=comment,
            user=request.user
        )
        if created:
            comment.like_count += 1
            comment.save(update_fields=['like_count'])
        else:
            like.delete()
            comment.like_count -= 1
            comment.save(update_fields=['like_count'])
        return Response(CommentSerializer(comment, context={'request': request}).data)
