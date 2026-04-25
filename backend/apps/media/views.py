import logging
import os
import shutil
import time

from django.http import FileResponse, HttpResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.users.permissions import IsOwnerOrAdmin
from utils.response import StandardResponse, api_error
from utils.error_codes import ErrorTypes
from .models import Media
from .serializers import MediaSerializer, MediaUploadSerializer

logger = logging.getLogger(__name__)


class MediaViewSet(viewsets.ModelViewSet):
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

    def _delete_physical_files(self, instance):
        """删除物理文件和缩略图目录
        
        Args:
            instance: 媒体对象实例
        """
        # 删除主文件
        if instance.file:
            try:
                file_path = instance.file.path
                if os.path.isfile(file_path):
                    # Windows 下文件可能被占用，尝试多次删除
                    for attempt in range(3):
                        try:
                            os.remove(file_path)
                            logger.info(f"已删除文件: {file_path}")
                            break
                        except PermissionError:
                            if attempt < 2:
                                time.sleep(1)
                            else:
                                logger.error(f"删除文件失败（被占用）: {file_path}")
                        except Exception as e:
                            logger.error(f"删除文件异常: {e}")
                            break
                else:
                    logger.warning(f"文件不存在: {file_path}")
            except Exception as e:
                logger.error(f"删除文件异常: {e}")
        
        # 删除缩略图目录
        if instance.thumbnails:
            try:
                thumbnails_dir = os.path.dirname(instance.thumbnails.path)
                if os.path.isdir(thumbnails_dir):
                    shutil.rmtree(thumbnails_dir)
                    logger.info(f"已删除缩略图目录: {thumbnails_dir}")
            except Exception as e:
                logger.error(f"删除缩略图失败: {e}")

    def perform_destroy(self, instance):
        """删除媒体对象及关联文件
        
        使用引用计数机制，只有当没有引用时才删除物理文件。
        """
        instance_id = str(instance.id)  # 删除前保存 ID
        
        # 如果是引用记录，减少原始文件的引用计数
        if instance.reference:
            original = instance.reference
            original.decrement_reference_count()
            logger.info(f"删除引用记录 {instance_id}，原始文件 {original.id} 引用计数: {original.reference_count}")
        else:
            # 原始文件：只有引用计数为 0 且无引用记录时才删除物理文件
            logger.info(f"删除原始文件 {instance_id}，引用计数: {instance.reference_count}，引用记录数: {instance.references.count()}")
            
            if instance.reference_count == 0 and not instance.references.exists():
                self._delete_physical_files(instance)
            else:
                logger.info(f"保留物理文件（仍有引用）")
        
        instance.delete()
        logger.info(f"已删除数据库记录: {instance_id}")

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
        
        # 非管理员只能查看自己的文件（检索除外）
        if (self.action != 'retrieve' and 
            self.request.user.is_authenticated and 
            not self.request.user.is_admin):
            queryset = queryset.filter(uploader=self.request.user)
        
        # 按文件类型过滤
        file_type = self.request.query_params.get('file_type')
        if file_type:
            queryset = queryset.filter(file_type__startswith=file_type)
        
        return queryset

    def list(self, request, *args, **kwargs):
        """获取媒体列表（统一响应格式）"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data).data
            return StandardResponse(paginated_data)
        
        serializer = self.get_serializer(queryset, many=True)
        return StandardResponse(serializer.data)

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
        
        if not media.is_video:
            return api_error(
                message='只能为视频文件生成缩略图',
                error_type=ErrorTypes.UNSUPPORTED_MEDIA_TYPE,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        media.thumbnail_status = 'pending'
        media.save(update_fields=['thumbnail_status'])
        media.generate_thumbnails_async()
        
        return StandardResponse({
            'message': '缩略图生成任务已启动',
            'thumbnail_status': 'pending'
        })


def stream_media_file(request, file_path, content_type, filename):
    """流式传输媒体文件，支持 HTTP Range 请求
    
    Args:
        request: HTTP 请求对象
        file_path: 文件绝对路径
        content_type: MIME 类型
        filename: 显示名称
    
    Returns:
        HttpResponse: 文件流响应（206/200/404/403/416）
    """
    try:
        # 检查文件是否存在和可读
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

        # 处理 Range 请求
        if range_header:
            range_match = range_header.replace('bytes=', '').split('-')
            start = int(range_match[0]) if range_match[0] else 0
            end = int(range_match[1]) if range_match[1] else file_size - 1

            if start >= file_size or end >= file_size:
                return HttpResponse(status=416)

            length = end - start + 1

            def file_iterator():
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

            response = HttpResponse(
                file_iterator(),
                status=206,
                content_type=content_type,
            )
            response['Content-Length'] = str(length)
            response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
        else:
            response = FileResponse(
                open(file_path, 'rb'),
                content_type=content_type,
            )
            response['Content-Length'] = str(file_size)

        response['Accept-Ranges'] = 'bytes'
        response['Content-Disposition'] = f'inline; filename="{filename}"'
        return response
        
    except PermissionError as e:
        logger.error(f"权限错误: {file_path}, {e}")
        return api_error(
            message='文件访问权限错误',
            error_type=ErrorTypes.FORBIDDEN,
            status=status.HTTP_403_FORBIDDEN
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
