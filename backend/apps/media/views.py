import json
import logging
import os

from django.http import FileResponse, HttpResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.users.permissions import IsOwnerOrAdmin
from services.media_service import MediaService
from utils.response import StandardResponse, api_error
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
            return api_error(
                message=str(e),
                error_type=ErrorTypes.UNSUPPORTED_MEDIA_TYPE,
                status=status.HTTP_400_BAD_REQUEST
            )


def stream_media_file(request, file_path, content_type, filename):
    """流式传输媒体文件，支持 HTTP Range 请求"""
    try:
        if not os.path.exists(file_path):
            logger.warning(f"文件不存在: {file_path}")
            return api_error(
                message='文件不存在',
                error_type=ErrorTypes.NOT_FOUND,
                status=status.HTTP_404_NOT_FOUND
            )

        if not os.access(file_path, os.R_OK):
            logger.error(f"文件无法访问: {file_path}")
            return api_error(
                message='文件无法访问',
                error_type=ErrorTypes.FORBIDDEN,
                status=status.HTTP_403_FORBIDDEN
            )

        file_size = os.path.getsize(file_path)
        range_header = request.headers.get('Range', '')

        if range_header:
            range_match = range_header.replace('bytes=', '').split('-')
            start = int(range_match[0]) if range_match[0] else 0
            end = int(range_match[1]) if range_match[1] else file_size - 1

            if start >= file_size or end >= file_size:
                return HttpResponse(status=416)

            length = end - start + 1

            def file_iterator():
                try:
                    with open(file_path, 'rb') as f:
                        f.seek(start)
                        remaining = length
                        chunk_size = 8192
                        while remaining > 0:
                            read_size = min(chunk_size, remaining)
                            data = f.read(read_size)
                            if not data:
                                break
                            yield data
                            remaining -= len(data)
                except PermissionError:
                    raise

            response = HttpResponse(
                file_iterator(),
                status=206,
                content_type=content_type,
            )
            response['Content-Length'] = str(length)
            response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
        else:
            try:
                response = FileResponse(
                    open(file_path, 'rb'),
                    content_type=content_type,
                )
                response['Content-Length'] = str(file_size)
            except PermissionError:
                raise

        response['Accept-Ranges'] = 'bytes'
        response['Content-Disposition'] = f'inline; filename="{filename}"'
        return response

    except PermissionError:
        logger.warning(f"文件被占用: {file_path}")
        return HttpResponse(
            json.dumps({'message': '视频正在处理中，文件被占用，请稍后再试'}),
            status=423,
            content_type='application/json'
        )
    except FileNotFoundError as e:
        logger.error(f"文件不存在: {file_path}, {e}")
        return api_error(
            message='文件不存在',
            error_type=ErrorTypes.NOT_FOUND,
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"流式传输失败: {file_path}, {type(e).__name__}: {e}", exc_info=True)
        return api_error(
            message='文件处理失败',
            error_type=ErrorTypes.FILE_PROCESSING_ERROR,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
