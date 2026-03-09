from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.users.permissions import IsEditorUser, IsOwnerOrAdmin

from .models import Comment
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
        elif self.action in ['approve']:
            return [IsEditorUser()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'list':
            queryset = queryset.filter(is_approved=True, parent__isnull=True)
        article_id = self.request.query_params.get('article')
        if article_id:
            queryset = queryset.filter(article_id=article_id)
        is_approved = self.request.query_params.get('is_approved')
        if is_approved is not None and self.request.user.is_authenticated:
            if self.request.user.is_editor:
                queryset = Comment.objects.select_related('user', 'article', 'parent')
                queryset = queryset.filter(is_approved=is_approved.lower() == 'true')
        return queryset

    @extend_schema(request=None, responses=CommentSerializer)
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        comment = self.get_object()
        comment.is_approved = True
        comment.save()
        return Response(CommentSerializer(comment).data)
