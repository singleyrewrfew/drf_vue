import logging

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken

from services.user_service import UserService
from utils.response import StandardResponse, api_error
from utils.error_codes import ErrorTypes
from .permissions import IsAdminUser
from .serializers import (
    PasswordChangeSerializer,
    UserRegisterSerializer,
    UserSerializer,
    UserUpdateSerializer,
)

logger = logging.getLogger(__name__)


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
        if self.action == 'login':
            return [AllowAny()]
        elif self.action == 'create':
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
            error_type = ErrorTypes.UNAUTHORIZED
            if error == '用户名和密码不能为空':
                error_type = ErrorTypes.BAD_REQUEST
            elif error == '账户已被禁用':
                error_type = ErrorTypes.ACCOUNT_DISABLED
            return api_error(message=error, error_type=error_type, status=status.HTTP_401_UNAUTHORIZED)

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
        refresh_token_str = request.data.get('refresh')

        if not refresh_token_str:
            return api_error(
                message='刷新令牌不能为空',
                error_type=ErrorTypes.BAD_REQUEST,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            refresh_token = RefreshToken(refresh_token_str)
            new_access_token = str(refresh_token.access_token)

            new_refresh_token = None
            if hasattr(refresh_token, 'rotate'):
                new_refresh = refresh_token.rotate()
                new_refresh_token = str(new_refresh)

            response_data = {"access": new_access_token}
            if new_refresh_token:
                response_data["refresh"] = new_refresh_token

            return StandardResponse(response_data)

        except (TokenError, InvalidToken) as e:
            return api_error(
                message=f'刷新令牌无效或已过期: {str(e)}',
                error_type=ErrorTypes.TOKEN_INVALID,
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            return api_error(
                message='服务器内部错误',
                error_type=ErrorTypes.INTERNAL_ERROR,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
