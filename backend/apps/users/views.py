from django.db import models
from django.db.models import Count, Sum
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken

from apps.comments.models import Comment
from apps.contents.models import Content
from apps.core.models import User
from apps.media.models import Media
from utils.response import StandardResponse, api_error
from utils.error_codes import ErrorTypes
from .permissions import IsAdminUser
from .serializers import (
    PasswordChangeSerializer,
    UserRegisterSerializer,
    UserSerializer,
    UserUpdateSerializer,
)
from utils.response import api_error


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

        AllowAny()：允许任何用户访问（无需登录、无需权限）；
        IsAdminUser()：仅允许 Django 后台的管理员用户（is_staff=True）访问；
        IsAuthenticated()：仅允许已登录（认证通过）的用户访问。
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

    @action(detail=False, methods=['post'],)
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
            return api_error(
                message='用户名和密码不能为空',
                error_type=ErrorTypes.BAD_REQUEST,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return api_error(
                message='用户名或密码错误',
                error_type=ErrorTypes.UNAUTHORIZED,
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.check_password(password):
            return api_error(
                message='用户名或密码错误',
                error_type=ErrorTypes.UNAUTHORIZED,
                status=status.HTTP_401_UNAUTHORIZED
            )

        # 用户是否激活
        if not user.is_active:
            return api_error(
                message='账户已被禁用',
                error_type=ErrorTypes.ACCOUNT_DISABLED,
                status=status.HTTP_403_FORBIDDEN
            )

        # 生成 JWT 令牌
        refresh = RefreshToken.for_user(user)
        return StandardResponse({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        })

    @action(detail=False, methods=['get'])
    def profile(self, request):
        """
        获取当前登录用户的个人信息

        返回完整的用户信息，包括计算属性
        """
        serializer = UserSerializer(request.user)
        return StandardResponse(serializer.data)

    @action(detail=False, methods=['put', 'patch', 'post'])
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
        return StandardResponse(UserSerializer(request.user).data)

    @action(detail=False, methods=['post'])
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
        return StandardResponse({'message': '密码修改成功'})

    @action(detail=False, methods=['post'])
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
        return StandardResponse({'message': '退出成功'})

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def refresh(self, request):
        """
        刷新访问令牌

        使用刷新令牌获取新的访问令牌和刷新令牌
        
        请求体：
        {
            "refresh": "your_refresh_token"
        }
        
        响应：
        {
            "access": "new_access_token",
            "refresh": "new_refresh_token"
        }
        """
        refresh_token_str = request.data.get('refresh')
        
        # 验证 refresh token 是否存在
        if not refresh_token_str:
            return api_error(
                message='刷新令牌不能为空',
                error_type=ErrorTypes.BAD_REQUEST,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # 验证 refresh token 并生成新的 access token
            refresh_token = RefreshToken(refresh_token_str)
            
            # 生成新的 access token
            new_access_token = str(refresh_token.access_token)
            
            # 如果启用了 token 轮换，生成新的 refresh token
            new_refresh_token = None
            if hasattr(refresh_token, 'rotate'):
                new_refresh = refresh_token.rotate()
                new_refresh_token = str(new_refresh)
            
            response_data = {"access": new_access_token}
            if new_refresh_token:
                response_data["refresh"] = new_refresh_token
            
            return StandardResponse(response_data)
            
        except (TokenError, InvalidToken) as e:
            # JWT 相关的特定异常：token 过期、格式错误、已加入黑名单等
            return api_error(
                message=f'刷新令牌无效或已过期: {str(e)}',
                error_type=ErrorTypes.TOKEN_INVALID,
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            # 其他未预期的异常
            return api_error(
                message='服务器内部错误',
                error_type=ErrorTypes.INTERNAL_ERROR,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
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
        return StandardResponse(data)

    @action(detail=False, methods=['get'])
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

            return StandardResponse({
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

            return StandardResponse({
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

