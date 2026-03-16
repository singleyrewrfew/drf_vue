from django.contrib.auth import get_user_model
from django.db.models import Count, Sum
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from apps.comments.models import Comment
from apps.contents.models import Content
from apps.media.models import Media
from .permissions import IsAdminUser
from .serializers import (
    PasswordChangeSerializer,
    UserRegisterSerializer,
    UserSerializer,
    UserUpdateSerializer,
)

# 获取自定义用户模型
User = get_user_model()

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
        - 其他: 需要认证
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
        - 其他: UserSerializer（读取）
        """
        if self.action == 'create':
            return UserRegisterSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """
        用户登录
        
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
            return Response({'error': '用户名和密码不能为空'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': '用户不存在'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.check_password(password):
            return Response({'error': '密码错误'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.is_active:
            return Response({'error': '账户已被禁用'}, status=status.HTTP_403_FORBIDDEN)
        
        # 生成 JWT 令牌
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        })
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        """
        获取当前登录用户的个人信息
        
        返回完整的用户信息，包括计算属性
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch', 'post'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        """
        更新用户个人信息
        
        支持的字段：
        - email: 邮箱
        - avatar: 头像（支持文件对象或 URL）
        - role: 角色
        - is_staff: 是否为后台用户
        """
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserSerializer(request.user).data)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """
        修改用户密码
        
        步骤：
        1. 验证原密码
        2. 验证新密码和确认密码
        3. 更新密码
        """
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': '密码修改成功'})
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def logout(self, request):
        """
        用户登出
        
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
        return Response({'message': '退出成功'})
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def popular(self, request):
        """
        获取热门作者列表
        
        排序规则：
        - 按已发布的文章数量降序
        - 返回前 10 名
        """
        users = User.objects.filter(
            contents__status='published'
        ).annotate(
            article_count=Count('contents')
        ).order_by('-article_count')[:10]
        
        data = []
        for user in users:
            data.append({
                'id': str(user.id),
                'username': user.username,
                'avatar': user.avatar.url if user.avatar else None,
                'article_count': user.article_count,
            })
        return Response(data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def stats(self, request):
        """
        获取仪表盘统计数据
        
        根据用户角色返回不同的数据：
        
        管理员（is_admin 或 is_superuser）：
        - 所有内容统计
        - 所有用户数
        - 所有评论数
        - 所有媒体数
        - 总浏览量
        - 最近 5 篇文章
        
        编辑者（is_editor）：
        - 自己的内容统计
        - 自己的评论数
        - 自己的浏览量
        - 最近 5 篇文章
        
        普通用户：
        - 空数据
        """
        # 判断用户角色
        is_admin = request.user.is_admin or request.user.is_superuser
        is_editor = request.user.is_admin or request.user.is_superuser or (request.user.role and request.user.role.code == 'editor')
        
        if is_admin:
            # 管理员显示全部数据 - 使用聚合减少查询次数
            content_stats = Content.objects.aggregate(
                total=Count('id'),
                published=Count('id', filter=models.Q(status='published')),
                drafts=Count('id', filter=models.Q(status='draft')),
                total_views=Sum('view_count')
            )
            
            content_count = content_stats['total']
            published_count = content_stats['published']
            draft_count = content_stats['drafts']
            total_views = content_stats['total_views'] or 0
            
            comment_count = Comment.objects.count()
            user_count = User.objects.count()
            media_count = Media.objects.count()
            
            # 获取最近 5 篇文章
            recent_contents = Content.objects.filter(status='published').select_related('author').order_by('-created_at')[:5]
            
            return Response({
                'contents': content_count,
                'published': published_count,
                'drafts': draft_count,
                'comments': comment_count,
                'users': user_count,
                'media': media_count,
                'views': total_views,
                'recent_contents': [
                    {
                        'id': str(content.id),
                        'title': content.title,
                        'author_name': content.author.username,
                        'view_count': content.view_count,
                        'created_at': content.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    }
                    for content in recent_contents
                ],
            })
        else:
            # 非管理员只显示个人数据 - 使用聚合减少查询次数
            my_content_stats = Content.objects.filter(author=request.user).aggregate(
                total=Count('id'),
                published=Count('id', filter=models.Q(status='published')),
                drafts=Count('id', filter=models.Q(status='draft')),
                total_views=Sum('view_count')
            )
            
            my_contents = my_content_stats['total']
            my_published = my_content_stats['published']
            my_drafts = my_content_stats['drafts']
            my_views = my_content_stats['total_views'] or 0
            
            my_comments = Comment.objects.filter(user=request.user).count()
            
            # 获取最近 5 篇文章
            recent_contents = Content.objects.filter(author=request.user, status='published').order_by('-created_at')[:5]
            
            return Response({
                'my_contents': my_contents,
                'my_published': my_published,
                'my_drafts': my_drafts,
                'my_comments': my_comments,
                'my_views': my_views,
                'recent_contents': [
                    {
                        'id': str(content.id),
                        'title': content.title,
                        'view_count': content.view_count,
                        'created_at': content.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    }
                    for content in recent_contents
                ],
            })
