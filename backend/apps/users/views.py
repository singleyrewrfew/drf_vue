import logging

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken

from services.user_service import UserService
from utils.response import StandardResponse, bad_request, unauthorized, forbidden, account_disabled, token_invalid, rate_limit_exceeded, internal_error
from utils.error_codes import ErrorTypes
from utils.log_utils import mask_token
from .permissions import IsAdminUser
from .serializers import (
    PasswordChangeSerializer,
    UserRegisterSerializer,
    UserSerializer,
    UserUpdateSerializer,
)

logger = logging.getLogger(__name__)

User = get_user_model()


@extend_schema_view(
    list=extend_schema(summary='列出用户', description='获取用户列表（需要管理员权限）'),
    retrieve=extend_schema(summary='获取用户详情', description='获取单个用户的详细信息'),
    create=extend_schema(summary='注册用户', description='创建新用户账户'),
    update=extend_schema(summary='更新用户', description='更新用户信息'),
    partial_update=extend_schema(summary='部分更新用户', description='部分更新用户信息'),
    destroy=extend_schema(summary='删除用户', description='删除用户（需要管理员权限）'),
    login=extend_schema(summary='用户登录', description='使用用户名和密码登录，返回 JWT Token'),
    profile=extend_schema(summary='获取个人资料', description='获取当前登录用户的个人信息'),
    update_profile=extend_schema(summary='更新个人资料', description='更新当前登录用户的个人信息'),
    change_password=extend_schema(summary='修改密码', description='修改当前登录用户的密码'),
    logout=extend_schema(summary='用户登出', description='登出并将 Refresh Token 加入黑名单'),
    refresh=extend_schema(summary='刷新 Token', description='使用 Refresh Token 获取新的 Access Token'),
)
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
    queryset = UserService.model_class.objects.all()
    serializer_class = UserSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_permissions(self):
        if self.action in ['login', 'refresh', 'create']:
            return [AllowAny()]
        elif self.action in ['list', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegisterSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer

    @action(detail=False, methods=['post'],)
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user, error = UserService.authenticate(username, password)
        if error:
            if error == '用户名和密码不能为空':
                return bad_request(error)
            elif error == '账户已被禁用':
                return account_disabled(error)
            return unauthorized(error)

        refresh = RefreshToken.for_user(user)
        return StandardResponse({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        })

    @action(detail=False, methods=['get'])
    def profile(self, request):
        serializer = UserSerializer(request.user)
        return StandardResponse(serializer.data)

    @action(detail=False, methods=['put', 'patch', 'post'])
    def update_profile(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return StandardResponse(UserSerializer(request.user).data)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return StandardResponse({'message': '密码修改成功'})

    @action(detail=False, methods=['post'])
    def logout(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except (TokenError, InvalidToken) as e:
            logger.warning(f"登出时 Token 黑名单失败: {e}")
        except Exception as e:
            logger.error(f"登出异常: {type(e).__name__}: {e}")
        return StandardResponse({'message': '退出成功'})

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def refresh(self, request):
        """
        刷新 Access Token
        
        安全特性：
        1. 验证 Refresh Token 有效性
        2. 检查用户账户状态（是否活跃）
        3. 旧 Refresh Token 立即加入黑名单（防止重放攻击）
        4. 生成新的 Access Token 和 Refresh Token（轮换机制）
        5. 记录刷新日志用于审计
        """
        from utils.cache_utils import cache_get, cache_set
        import logging
        
        logger = logging.getLogger(__name__)
        refresh_token_str = request.data.get('refresh')

        if not refresh_token_str:
            return bad_request('刷新令牌不能为空')

        try:
            # 第 1 步：验证 Refresh Token 格式和签名
            refresh_token = RefreshToken(refresh_token_str)
            
            # 第 2 步：提取用户 ID，检查用户状态
            user_id = refresh_token.get('user_id')
            if not user_id:
                return token_invalid('刷新令牌格式错误')
            
            # 第 3 步：查询用户并验证状态
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return token_invalid('用户不存在')
            
            # 第 4 步：检查用户账户状态
            if not user.is_active:
                # 账户被禁用，立即将 token 加入黑名单
                try:
                    refresh_token.blacklist()
                except Exception:
                    pass
                return forbidden('账户已被禁用')
            
            # 第 5 步：检查刷新频率限制（防止滥用）
            rate_limit_key = f'token_refresh_rate_{user_id}'
            refresh_count = cache_get(rate_limit_key, 0)
            
            # 每分钟最多刷新 5 次
            if refresh_count >= 5:
                logger.warning(
                    f'用户 {user.username} (ID:{user_id}) Token 刷新频率超限: '
                    f'{refresh_count} 次/分钟'
                )
                return rate_limit_exceeded('刷新过于频繁，请稍后再试')
            
            # 更新刷新计数（60秒过期）
            cache_set(rate_limit_key, refresh_count + 1, timeout=60)
            
            # 第 6 步：旧 Refresh Token 立即加入黑名单（防止重放攻击）
            try:
                refresh_token.blacklist()
                logger.info(f'用户 {user.username} (ID:{user_id}) 旧 Refresh Token 已加入黑名单')
            except Exception as e:
                logger.error(f'Refresh Token 黑名单失败: {e}')
                # 即使黑名单失败，也继续执行（避免影响用户体验）
            
            # 第 7 步：生成新的 Access Token 和 Refresh Token
            new_access_token = str(refresh_token.access_token)
            new_refresh_token = None
            
            # 如果启用了轮换，生成新的 Refresh Token
            try:
                new_refresh = RefreshToken.for_user(user)
                new_refresh_token = str(new_refresh)
                logger.info(f'用户 {user.username} (ID:{user_id}) Token 轮换成功')
            except Exception as e:
                logger.error(f'Token 轮换失败: {e}')
                # 如果轮换失败，不返回新的 refresh token
            
            # 第 8 步：构建响应数据
            response_data = {"access": new_access_token}
            if new_refresh_token:
                response_data["refresh"] = new_refresh_token
            
            # 记录成功刷新日志（脱敏 Token）
            logger.info(
                f'用户 {user.username} (ID:{user_id}) Token 刷新成功, '
                f'Access Token: {mask_token(new_access_token)}, '
                f'IP: {request.META.get("REMOTE_ADDR", "unknown")}'
            )
            
            return StandardResponse(response_data)

        except (TokenError, InvalidToken) as e:
            logger.warning(f'Token 刷新失败 - 无效令牌: {str(e)}')
            return token_invalid('刷新令牌无效或已过期')
        except User.DoesNotExist:
            logger.warning(f'Token 刷新失败 - 用户不存在')
            return token_invalid('用户不存在')
        except Exception as e:
            logger.error(f'Token 刷新异常: {type(e).__name__}: {str(e)}')
            return internal_error('服务器内部错误')

    @action(detail=False, methods=['get'])
    def popular(self, request):
        data = UserService.get_popular_authors(limit=10)
        return StandardResponse(data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        is_admin = request.user.is_admin or request.user.is_superuser

        if is_admin:
            data = UserService.get_admin_statistics()
        else:
            data = UserService.get_user_statistics(request.user)

        return StandardResponse(data)
