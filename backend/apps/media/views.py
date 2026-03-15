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
    queryset = Media.objects.select_related('uploader')
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.action == 'retrieve':
            return [AllowAny()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return MediaUploadSerializer
        return MediaSerializer

    def perform_create(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        # 只有当没有引用或者是原始文件时，才删除实际文件
        if not instance.reference and instance.file:
            # 检查是否有其他记录引用这个文件
            has_references = Media.objects.filter(reference=instance).exists()
            if not has_references:
                try:
                    file_path = instance.file.path
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                except Exception:
                    pass
            
            try:
                if instance.thumbnails:
                    thumbnails_dir = os.path.dirname(instance.thumbnails.path)
                    if os.path.isdir(thumbnails_dir):
                        shutil.rmtree(thumbnails_dir)
            except Exception:
                pass
        
        instance.delete()

    @extend_schema(request=MediaUploadSerializer, responses=MediaSerializer)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(MediaSerializer(serializer.instance).data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action != 'retrieve' and self.request.user.is_authenticated and not self.request.user.is_admin:
            queryset = queryset.filter(uploader=self.request.user)
        file_type = self.request.query_params.get('file_type')
        if file_type:
            queryset = queryset.filter(file_type__startswith=file_type)
        return queryset

    @extend_schema(exclude=True)
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        file_path = instance.actual_file.path if instance.actual_file else instance.file.path
        return stream_media_file(request, file_path, instance.file_type, instance.filename)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsOwnerOrAdmin])
    def regenerate_thumbnails(self, request, pk=None):
        """重新生成视频缩略图"""
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
