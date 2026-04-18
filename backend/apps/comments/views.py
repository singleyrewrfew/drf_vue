from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from apps.users.permissions import IsOwnerOrAdmin
from utils.response import StandardResponse
from .models import Comment, CommentLike
from .serializers import CommentCreateSerializer, CommentListSerializer, CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """
    评论视图集
    
    提供对评论模型的完整 CRUD 操作，支持评论审核、点赞功能，
    以及根据用户角色和请求参数动态过滤评论数据。
    
    Attributes:
        queryset: 查询集，包含所有评论对象并预加载关联的用户、文章和父评论数据
        permission_classes: 权限类列表，读操作允许认证用户或只读，写操作需要特定权限
    
    Methods:
        get_serializer_class: 根据当前动作动态返回对应的序列化器类
        get_permissions: 根据当前动作动态返回对应的权限实例列表
        perform_create: 执行评论创建操作
        get_queryset: 根据请求参数和用户角色动态过滤查询集
        approve: 审核评论的自定义动作
        like: 点赞/取消点赞评论的自定义动作
    """
    queryset = Comment.objects.select_related('user', 'article', 'parent')
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        """
        获取序列化器类
        
        根据当前的 action 动态选择使用对应的序列化器：
        - list 操作使用列表序列化器
        - create 操作使用创建序列化器
        - 其他操作（如 retrieve、update）使用详细序列化器
        
        Returns:
            type: 序列化器类，CommentListSerializer、CommentCreateSerializer 或 CommentSerializer
        
        Raises:
            无
        """
        if self.action == 'list':
            return CommentListSerializer
        elif self.action == 'create':
            return CommentCreateSerializer
        return CommentSerializer

    def get_permissions(self):
        """
        获取权限实例列表
        
        根据当前的 action 动态分配权限：
        - 创建评论需要用户认证
        - 更新、部分更新、删除操作需要所有者或管理员权限
        - 审核、点赞操作需要用户认证
        - 其他操作使用默认权限配置
        
        Returns:
            list: 权限实例列表，包含 IsAuthenticated、IsOwnerOrAdmin 实例或父类的权限实例
        
        Raises:
            无
        """
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        elif self.action in ['approve', 'like']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def perform_create(self, serializer):
        """
        执行评论创建操作
        
        保存序列化后的评论对象到数据库。
        
        Args:
            serializer: 已验证数据的序列化器实例
        
        Returns:
            None
        
        Raises:
            无
        """
        serializer.save()

    def get_queryset(self):
        """
        获取动态过滤后的查询集
        
        根据请求参数和用户角色对评论数据进行多层过滤：
        - show_my 参数：返回当前用户的评论
        - show_all 参数：编辑或管理员可查看所有评论
        - 默认情况：只显示已审核的主评论（无父评论）
        - article 参数：通过文章 ID、slug 或 UUID 过滤评论
        - is_approved 参数：编辑或管理员可按审核状态过滤
        
        Returns:
            QuerySet: 经过过滤的评论查询集
        
        Raises:
            无
        """
        queryset = super().get_queryset()
        request: Request = self.request  # type: ignore
        if self.action == 'list':
            show_all = request.query_params.get('all')
            show_my = request.query_params.get('my')
            
            # 如果请求的是自己的评论
            if show_my and self.request.user.is_authenticated:
                queryset = queryset.filter(user=self.request.user)
            # 如果是编辑或管理员请求所有评论
            elif show_all and request.user.is_authenticated and request.user.is_editor:
                return queryset
            # 默认只显示已审核的主评论
            else:
                queryset = queryset.filter(is_approved=True, parent__isnull=True)
        
        article_id = request.query_params.get('article')
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
        is_approved = request.query_params.get('is_approved')
        if is_approved is not None and request.user.is_authenticated:
            if request.user.is_editor:
                queryset = queryset.filter(is_approved=is_approved.lower() == 'true')
        return queryset

    def list(self, request, *args, **kwargs):
        """
        获取评论列表（统一响应格式）
        
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

    @extend_schema(request=None, responses=CommentSerializer)
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """
        审核评论
        
        将指定评论标记为已审核状态。仅允许有权限的用户（如编辑或管理员）执行此操作。
        
        Args:
            request: HTTP 请求对象，包含请求方法和用户信息
            pk: 评论的主键或 UUID
        
        Returns:
            Response: 包含审核后评论数据的响应对象，HTTP 状态码为 200
        
        Raises:
            无
        """
        comment = self.get_object()
        comment.is_approved = True
        comment.save()
        return StandardResponse(CommentSerializer(comment).data)

    @extend_schema(request=None, responses=CommentSerializer)
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """
        点赞或取消点赞评论
        
        如果用户未点过赞则创建点赞记录并增加评论点赞数；
        如果用户已点过赞则删除点赞记录并减少评论点赞数（切换点赞状态）。
        
        Args:
            request: HTTP 请求对象，包含请求方法和当前用户信息
            pk: 评论的主键或 UUID
        
        Returns:
            Response: 包含更新后评论数据的响应对象，包含最新点赞数和 HTTP 状态码 200
        
        Raises:
            无
        """
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
        return StandardResponse(CommentSerializer(comment, context={'request': request}).data)
