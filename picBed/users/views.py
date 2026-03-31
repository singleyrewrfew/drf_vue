from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

from .models import User
from .serializers import (
    UserSerializer, 
    UserRegistrationSerializer,
    UserProfileSerializer,
    UserUpdateSerializer
)
from core.responses import APIResponse


class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return APIResponse.success(
                data={
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'access': str(refresh.access_token),
                        'refresh': str(refresh)
                    }
                },
                message='注册成功',
                status_code=status.HTTP_201_CREATED
            )
        return APIResponse.error(
            message='注册失败',
            details=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['post'])
    @method_decorator(ratelimit(key='ip', rate='5/m', method='POST'))
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return APIResponse.error(
                message='用户名和密码不能为空',
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=username, password=password)
        
        if user is None:
            return APIResponse.error(
                message='用户名或密码错误',
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.is_active:
            return APIResponse.error(
                message='账户已被禁用',
                status_code=status.HTTP_403_FORBIDDEN
            )
        
        refresh = RefreshToken.for_user(user)
        return APIResponse.success(
            data={
                'user': UserSerializer(user).data,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            },
            message='登录成功'
        )
    
    @action(detail=False, methods=['post'])
    def refresh(self, request):
        refresh_token = request.data.get('refresh')
        
        if not refresh_token:
            return APIResponse.error(
                message='Refresh token不能为空',
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            refresh = RefreshToken(refresh_token)
            return APIResponse.success(
                data={
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            )
        except Exception as e:
            return APIResponse.error(
                message='无效的refresh token',
                status_code=status.HTTP_401_UNAUTHORIZED
            )


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'partial_update':
            return UserUpdateSerializer
        return UserProfileSerializer
    
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    
    def list(self, request):
        serializer = self.get_serializer(request.user)
        return APIResponse.success(data=serializer.data)
    
    @action(detail=False, methods=['get'])
    def profile(self, request):
        serializer = UserSerializer(request.user)
        return APIResponse.success(data=serializer.data)
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not old_password or not new_password:
            return APIResponse.error(
                message='旧密码和新密码不能为空',
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        if not user.check_password(old_password):
            return APIResponse.error(
                message='旧密码错误',
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        if len(new_password) < 8:
            return APIResponse.error(
                message='新密码长度至少为8位',
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(new_password)
        user.save()
        
        return APIResponse.success(message='密码修改成功')
