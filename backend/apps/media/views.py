import os
import shutil

from django.conf import settings
from django.http import FileResponse, HttpResponse
from django.views.decorators.http import require_GET
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.users.permissions import IsOwnerOrAdmin

from .models import Media
from .serializers import MediaSerializer, MediaUploadSerializer


class MediaViewSet(viewsets.ModelViewSet):
    """
    媒体文件视图集
    
    提供对媒体文件的完整 CRUD 操作，支持文件上传、下载、删除以及缩略图管理功能。
    实现了基于用户角色的权限控制和智能文件清理机制。
    
    Attributes:
        queryset: 查询集，包含所有媒体对象并预加载关联的上传者数据
        permission_classes: 权限类列表，默认要求用户认证，特定操作有不同权限要求
        parser_classes: 解析器类列表，支持 multipart 和 form-data 格式的文件上传
    
    Methods:
        get_permissions: 根据当前动作动态返回对应的权限实例列表
        get_serializer_class: 根据当前动作动态返回对应的序列化器类
        perform_create: 执行媒体文件创建操作
        perform_destroy: 执行媒体文件删除操作，包含智能文件清理逻辑
        create: 重写创建方法，处理文件上传并返回完整数据
        get_queryset: 根据用户角色过滤查询集
        retrieve: 检索并提供媒体文件的流式传输
        regenerate_thumbnails: 重新生成视频缩略图的自定义动作
    """
    queryset = Media.objects.select_related('uploader')
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        """
        获取权限实例列表
        
        根据当前的 action 动态分配权限：
        - 检索（下载）操作允许任何人访问
        - 更新、部分更新、删除操作需要所有者或管理员权限
        - 其他操作使用默认权限配置
        
        Returns:
            list: 权限实例列表，包含 AllowAny、IsOwnerOrAdmin 实例或父类的权限实例
        
        Raises:
            无
        """
        if self.action == 'retrieve':
            return [AllowAny()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return super().get_permissions()

    def get_serializer_class(self):
        """
        获取序列化器类
        
        根据当前的 action 动态选择使用对应的序列化器：
        - create 操作使用上传序列化器，处理文件上传验证
        - 其他操作使用通用序列化器
        
        Returns:
            type: 序列化器类，MediaUploadSerializer 或 MediaSerializer
        
        Raises:
            无
        """
        if self.action == 'create':
            return MediaUploadSerializer
        return MediaSerializer

    def perform_create(self, serializer):
        """
        执行媒体文件创建操作
        
        保存序列化后的媒体对象到数据库，包含上传的文件数据。
        
        Args:
            serializer: 已验证数据的序列化器实例
        
        Returns:
            None
        
        Raises:
            无
        """
        serializer.save()

    def perform_destroy(self, instance):
        """
        执行媒体文件删除操作
        
        删除媒体对象及其关联的物理文件。采用智能清理策略：
        - 使用引用计数机制，只有当记录没有引用且是原始文件时，才删除实际文件
        - 检查是否有其他记录引用该文件，避免误删共享文件
        - 同时删除关联的缩略图目录
        - 如果删除过程出现异常则忽略，确保数据库记录被删除
        
        Args:
            instance: 要删除的媒体对象实例
        
        Returns:
            None
        
        Raises:
            无
        """
        import time
        
        # 如果是引用记录，减少原始文件的引用计数
        if instance.reference:
            original = instance.reference
            original.decrement_reference_count()
            print(f"[删除] 引用记录 {instance.id}，已减少原始文件 {original.id} 的引用计数至 {original.reference_count}")
        else:
            # 原始文件的删除逻辑
            # 只有当引用计数为 0 且没有其他引用记录时，才删除物理文件
            print(f"[删除] 原始文件 {instance.id}，当前引用计数：{instance.reference_count}，引用记录数：{instance.references.count()}")
            
            if instance.reference_count == 0 and not instance.references.exists():
                # 删除物理文件
                if instance.file:
                    try:
                        file_path = instance.file.path
                        print(f"[删除] 文件路径：{file_path}")
                        
                        # Windows 下文件可能被占用，尝试多次删除
                        max_retries = 3
                        for attempt in range(max_retries):
                            try:
                                if os.path.isfile(file_path):
                                    os.remove(file_path)
                                    print(f"[删除] 已删除物理文件：{file_path}")
                                    break
                                else:
                                    print(f"[警告] 文件不存在：{file_path}")
                                    break
                            except PermissionError as e:
                                if attempt < max_retries - 1:
                                    print(f"[重试] 文件被占用，{attempt + 1}/{max_retries} 次重试，等待 1 秒...")
                                    time.sleep(1)
                                else:
                                    print(f"[错误] 删除文件失败（被占用）：{e}")
                                    print(f"[提示] 请关闭正在使用该文件的程序（如视频播放器、FFmpeg 等）")
                            except Exception as e:
                                print(f"[错误] 删除文件失败：{e}")
                                break
                    except Exception as e:
                        print(f"[错误] 删除文件失败：{e}")
                
                # 删除缩略图目录
                if instance.thumbnails:
                    try:
                        thumbnails_dir = os.path.dirname(instance.thumbnails.path)
                        print(f"[删除] 缩略图目录：{thumbnails_dir}")
                        if os.path.isdir(thumbnails_dir):
                            shutil.rmtree(thumbnails_dir)
                            print(f"[删除] 已删除缩略图目录：{thumbnails_dir}")
                        else:
                            print(f"[警告] 缩略图目录不存在：{thumbnails_dir}")
                    except Exception as e:
                        print(f"[错误] 删除缩略图失败：{e}")
            else:
                print(f"[跳过] 保留物理文件（引用计数：{instance.reference_count}，引用记录：{instance.references.count()})")
        
        instance.delete()
        print(f"[删除] 已删除数据库记录：{instance.id}")

    @extend_schema(request=MediaUploadSerializer, responses=MediaSerializer)
    def create(self, request, *args, **kwargs):
        """
        创建媒体文件
        
        处理文件上传请求，验证上传数据并保存到数据库。
        重写父类方法以返回完整的媒体数据而非空响应。
        
        Args:
            request: HTTP 请求对象，包含上传的文件数据
            *args: 位置参数
            **kwargs: 关键字参数
        
        Returns:
            Response: 包含创建后媒体数据的响应对象，HTTP 状态码为 201
        
        Raises:
            APIException: 当数据验证失败时抛出异常
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(MediaSerializer(serializer.instance).data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        """
        获取动态过滤后的查询集
        
        根据用户角色和请求参数对媒体数据进行过滤：
        - 非管理员用户只能查看自己上传的文件（检索操作除外）
        - file_type 参数：按文件类型前缀过滤
        
        Returns:
            QuerySet: 经过过滤的媒体查询集
        
        Raises:
            无
        """
        queryset = super().get_queryset()
        if self.action != 'retrieve' and self.request.user.is_authenticated and not self.request.user.is_admin:
            queryset = queryset.filter(uploader=self.request.user)
        file_type = self.request.query_params.get('file_type')
        if file_type:
            queryset = queryset.filter(file_type__startswith=file_type)
        return queryset

    @extend_schema(exclude=True)
    def retrieve(self, request, *args, **kwargs):
        """
        检索并提供媒体文件的流式传输
        
        获取指定的媒体对象，并以流式方式返回文件内容。
        优先使用 actual_file（如有），否则使用 file 字段。
        
        Args:
            request: HTTP 请求对象
            *args: 位置参数
            **kwargs: 关键字参数，包含 pk 等查找参数
        
        Returns:
            FileResponse: 包含文件流内容的响应对象，支持范围请求
        
        Raises:
            无
        """
        instance = self.get_object()
        file_path = instance.actual_file.path if instance.actual_file else instance.file.path
        return stream_media_file(request, file_path, instance.file_type, instance.filename)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsOwnerOrAdmin])
    def regenerate_thumbnails(self, request, pk=None):
        """
        重新生成视频缩略图
        
        为视频文件异步重新生成缩略图。仅允许视频文件执行此操作，
        将缩略图状态设置为 pending 并触发异步任务。
        
        Args:
            request: HTTP 请求对象
            pk: 媒体对象的主键或 UUID
        
        Returns:
            Response: 包含操作结果消息和缩略图状态的响应对象，HTTP 状态码为 200
                     非视频文件返回 400 错误
        
        Raises:
            无
        """
        media = self.get_object()
        
        if not media.is_video:
            return Response({'error': '只能为视频文件生成缩略图'}, status=status.HTTP_400_BAD_REQUEST)
        
        media.thumbnail_status = 'pending'
        media.save(update_fields=['thumbnail_status'])
        
        media.generate_thumbnails_async()
        
        return Response({
            'message': '缩略图生成任务已启动',
            'thumbnail_status': 'pending'
        })


def stream_media_file(request, file_path, content_type, filename):
    """
    流式传输媒体文件
    
    处理媒体文件的流式传输，支持 HTTP Range 请求以实现断点续传和分片加载。
    对于视频等大文件特别有用，可以按需传输部分内容而非整个文件。
    
    Args:
        request: HTTP 请求对象，可能包含 Range 头信息
        file_path: 要传输的文件在服务器上的绝对路径
        content_type: 文件的 MIME 类型，如 'video/mp4'、'image/jpeg' 等
        filename: 文件的显示名称，用于 Content-Disposition 头
    
    Returns:
        HttpResponse: 包含文件流内容的响应对象
                      - 如果有 Range 请求且有效，返回 206 Partial Content
                      - 如果 Range 无效，返回 416 Range Not Satisfiable
                      - 如果没有 Range 请求，返回 200 OK 和完整文件
                      - 如果文件不存在，返回 404
                      - 如果无访问权限，返回 403
    
    Raises:
        无
    """
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            logger.warning(f"File not found: {file_path}")
            return HttpResponse(
                {'error': '文件不存在'},
                status=status.HTTP_404_NOT_FOUND,
                content_type='application/json'
            )
        
        # 检查文件是否可读
        if not os.access(file_path, os.R_OK):
            logger.error(f"Permission denied: {file_path}")
            return HttpResponse(
                {'error': '文件无法访问'},
                status=status.HTTP_403_FORBIDDEN,
                content_type='application/json'
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
        logger.error(f"Permission error accessing file {file_path}: {e}")
        return HttpResponse(
            {'error': '文件访问权限错误'},
            status=status.HTTP_403_FORBIDDEN,
            content_type='application/json'
        )
    except FileNotFoundError as e:
        logger.error(f"File not found error: {file_path}, {e}")
        return HttpResponse(
            {'error': '文件不存在'},
            status=status.HTTP_404_NOT_FOUND,
            content_type='application/json'
        )
    except Exception as e:
        logger.error(f"Unexpected error streaming file {file_path}: {type(e).__name__}: {e}", exc_info=True)
        return HttpResponse(
            {'error': '文件处理失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content_type='application/json'
        )
