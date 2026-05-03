import logging
import os

from django.conf import settings
from django.http import FileResponse, HttpResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.users.permissions import IsOwnerOrAdmin
from services.media_service import MediaService
from utils.response import StandardResponse, unsupported_media_type, not_found, forbidden, conflict, file_processing_error
from utils.error_codes import ErrorTypes
from utils.viewset_mixins import StandardListMixin
from .models import Media
from .serializers import MediaSerializer, MediaUploadSerializer

logger = logging.getLogger(__name__)


class MediaViewSet(StandardListMixin, viewsets.ModelViewSet):
    """媒体文件视图集

    提供媒体文件的 CRUD 操作，支持文件上传、流式下载、删除及缩略图管理。
    实现基于角色的权限控制和智能文件清理机制。
    """
    queryset = Media.objects.select_related('uploader')
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    # 有效的文件类型前缀白名单（防止 SQL 注入）
    VALID_FILE_TYPE_PREFIXES = ['image/', 'video/', 'application/']

    def get_permissions(self):
        """动态分配权限"""
        if self.action == 'retrieve':
            return [AllowAny()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return super().get_permissions()

    def get_serializer_class(self):
        """根据操作选择序列化器"""
        if self.action == 'create':
            return MediaUploadSerializer
        return MediaSerializer

    def perform_create(self, serializer):
        """保存媒体对象"""
        serializer.save()

    def perform_destroy(self, instance):
        """删除媒体对象及关联文件"""
        MediaService.delete_media(instance)

    @extend_schema(request=MediaUploadSerializer, responses=MediaSerializer)
    def create(self, request, *args, **kwargs):
        """创建媒体文件，返回完整数据"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return StandardResponse(MediaSerializer(serializer.instance).data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        """根据用户角色和参数过滤查询集"""
        queryset = super().get_queryset()

        if (self.action != 'retrieve' and
            self.request.user.is_authenticated and
            not self.request.user.is_admin):
            queryset = queryset.filter(uploader=self.request.user)

        file_type = self.request.query_params.get('file_type')
        if file_type:
            # 验证文件类型前缀是否在白名单中（防止 SQL 注入）
            if not any(file_type.startswith(prefix) for prefix in self.VALID_FILE_TYPE_PREFIXES):
                raise ValidationError(
                    f"无效的文件类型: {file_type}。允许的前缀: {', '.join(self.VALID_FILE_TYPE_PREFIXES)}"
                )
            queryset = queryset.filter(file_type__startswith=file_type)

        return queryset

    @extend_schema(exclude=True)
    def retrieve(self, request, *args, **kwargs):
        """流式传输媒体文件"""
        instance = self.get_object()
        file_path = instance.actual_file.path if instance.actual_file else instance.file.path
        return stream_media_file(request, file_path, instance.file_type, instance.filename)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsOwnerOrAdmin])
    def regenerate_thumbnails(self, request, pk=None):
        """重新生成视频缩略图"""
        media = self.get_object()

        try:
            result = MediaService.regenerate_thumbnails(media)
            return StandardResponse(result)
        except ValueError as e:
            return unsupported_media_type(str(e))


def stream_media_file(request, file_path, content_type, filename):
    """
    流式传输媒体文件，智能选择传输方式
    
    - 生产环境（有 Nginx）：使用 X-Accel-Redirect，零 Python 资源占用
    - 开发环境：使用 Django FileResponse，自动利用 sendfile
    """
    try:
        if not os.path.exists(file_path):
            logger.warning(f"文件不存在: {file_path}")
            return not_found('文件不存在')

        if not os.access(file_path, os.R_OK):
            logger.error(f"文件无法访问: {file_path}")
            return forbidden('文件无法访问')
        
        # 检查是否启用 Nginx X-Accel-Redirect
        use_nginx_accel = getattr(settings, 'USE_NGINX_ACCEL_REDIRECT', False)
        
        if use_nginx_accel:
            # 生产环境：使用 Nginx X-Accel-Redirect
            return _serve_with_nginx_accel(request, file_path, content_type, filename)
        else:
            # 开发环境：使用 Django FileResponse（已足够高效）
            return _serve_with_django(file_path, content_type, filename)

    except PermissionError:
        logger.warning(f"文件被占用: {file_path}")
        return conflict('视频正在处理中，文件被占用，请稍后再试')
    except FileNotFoundError as e:
        logger.error(f"文件不存在: {file_path}, {e}")
        return not_found('文件不存在')
    except Exception as e:
        logger.error(f"流式传输失败: {file_path}, {type(e).__name__}: {e}", exc_info=True)
        return file_processing_error('文件处理失败')


def _serve_with_nginx_accel(request, file_path, content_type, filename):
    """
    使用 Nginx X-Accel-Redirect 传输文件
    
    优势：
    - Nginx 直接处理文件传输，完全绕过 Python
    - 支持高效的 Range 请求
    - 零内存和 CPU 占用（Python 层面）
    - 可以配合 Nginx 的缓存、限流等功能
    
    注意：需要在 Nginx 中配置 internal location
    """
    # 获取媒体文件的内部路径（相对于 Nginx 的 alias）
    media_root = str(settings.MEDIA_ROOT)
    # 将绝对路径转换为 Nginx internal location 的路径
    internal_path = file_path.replace(media_root, '/media_internal')
    
    response = HttpResponse()
    response['Content-Type'] = content_type
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    # 关键头：告诉 Nginx 传输哪个文件
    response['X-Accel-Redirect'] = internal_path
    # 启用 Nginx 缓冲
    response['X-Accel-Buffering'] = 'yes'
    
    logger.debug(f"Using Nginx X-Accel-Redirect: {internal_path}")
    return response


def _serve_with_django(file_path, content_type, filename):
    """
    使用 Django FileResponse 传输文件
    
    优势：
    - 开发环境足够高效
    - 自动使用 wsgi.file_wrapper（支持 sendfile）
    - 支持 Range 请求（视频拖动进度条）
    - 流式传输，不占用大量内存
    - 代码简单，易于调试
    """
    # Django FileResponse 已经非常高效：
    # 1. 自动检测并使用 wsgi.file_wrapper
    # 2. 在 Linux/Mac 上会使用操作系统的 sendfile() 系统调用
    # 3. 自动处理 Range 请求（视频拖动进度条）
    # 4. 流式传输，不会一次性加载整个文件到内存
    
    # ⚠️ 关键：as_attachment=False 才能支持 Range 请求
    response = FileResponse(
        open(file_path, 'rb'),
        content_type=content_type,
        as_attachment=False,  # 必须为 False 才能支持 Range 请求
    )
    
    # ⚠️ 关键：显式添加 Accept-Ranges 头
    response['Accept-Ranges'] = 'bytes'
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    
    logger.debug(f"Using Django FileResponse: {file_path}")
    return response
