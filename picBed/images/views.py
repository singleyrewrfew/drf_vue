import os
import hashlib
import json
from io import BytesIO
from PIL import Image as PILImage
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
import uuid

from .models import Image, Album, UploadChunk
from .serializers import (
    ImageSerializer,
    ImageUploadSerializer,
    AlbumSerializer,
    ChunkUploadInitSerializer,
    ChunkUploadSerializer,
    ChunkUploadCompleteSerializer
)
from core.responses import APIResponse


class AlbumViewSet(viewsets.ModelViewSet):
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_public']
    
    def get_queryset(self):
        return Album.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['album', 'is_public', 'format']
    search_fields = ['title', 'description', 'filename']
    ordering_fields = ['created_at', 'file_size', 'access_count']
    
    def get_queryset(self):
        queryset = Image.objects.filter(user=self.request.user)
        
        album_id = self.request.query_params.get('album')
        if album_id:
            queryset = queryset.filter(album_id=album_id)
        
        return queryset.select_related('album', 'user')
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        cache_key = f'image:{instance.id}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return APIResponse.success(data=cached_data)
        
        serializer = self.get_serializer(instance)
        data = serializer.data
        
        cache.set(cache_key, data, timeout=3600)
        
        instance.increment_access_count()
        
        return APIResponse.success(data=data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        user = request.user
        user.storage_used -= instance.file_size
        user.save(update_fields=['storage_used'])
        
        if instance.file:
            instance.file.delete(save=False)
        
        instance.delete()
        
        cache_key = f'image:{instance.id}'
        cache.delete(cache_key)
        
        return APIResponse.success(message='图片删除成功')
    
    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def upload(self, request):
        serializer = ImageUploadSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            image = serializer.save()
            return APIResponse.success(
                data=ImageSerializer(image).data,
                message='图片上传成功',
                status_code=status.HTTP_201_CREATED
            )
        
        return APIResponse.error(
            message='图片上传失败',
            details=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['post'])
    def upload_init(self, request):
        serializer = ChunkUploadInitSerializer(data=request.data)
        
        if serializer.is_valid():
            data = serializer.validated_data
            
            upload_id = str(uuid.uuid4())
            
            total_chunks = (data['file_size'] + data['chunk_size'] - 1) // data['chunk_size']
            
            UploadChunk.objects.create(
                upload_id=upload_id,
                chunk_number=0,
                chunk_size=data['chunk_size'],
                total_chunks=total_chunks,
                total_size=data['file_size'],
                filename=data['filename'],
                file_hash=data['file_hash'],
                user=request.user
            )
            
            return APIResponse.success(
                data={
                    'upload_id': upload_id,
                    'total_chunks': total_chunks,
                    'chunk_size': data['chunk_size']
                },
                message='分块上传初始化成功'
            )
        
        return APIResponse.error(
            message='初始化失败',
            details=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def upload_chunk(self, request):
        serializer = ChunkUploadSerializer(data=request.data)
        
        if serializer.is_valid():
            data = serializer.validated_data
            
            try:
                upload_chunk = UploadChunk.objects.get(
                    upload_id=data['upload_id'],
                    chunk_number=0
                )
            except UploadChunk.DoesNotExist:
                return APIResponse.error(
                    message='上传ID不存在',
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            chunk_number = data['chunk_number']
            chunk_file = data['chunk']
            
            chunk_dir = os.path.join(settings.MEDIA_ROOT, 'chunks', data['upload_id'])
            os.makedirs(chunk_dir, exist_ok=True)
            
            chunk_path = os.path.join(chunk_dir, f'chunk_{chunk_number}')
            
            with open(chunk_path, 'wb+') as destination:
                for chunk in chunk_file.chunks():
                    destination.write(chunk)
            
            UploadChunk.objects.create(
                upload_id=data['upload_id'],
                chunk_number=chunk_number,
                chunk_size=chunk_file.size,
                total_chunks=upload_chunk.total_chunks,
                total_size=upload_chunk.total_size,
                filename=upload_chunk.filename,
                file_hash=upload_chunk.file_hash,
                user=request.user
            )
            
            uploaded_chunks = UploadChunk.objects.filter(
                upload_id=data['upload_id']
            ).exclude(chunk_number=0).count()
            
            return APIResponse.success(
                data={
                    'chunk_number': chunk_number,
                    'uploaded_chunks': uploaded_chunks,
                    'total_chunks': upload_chunk.total_chunks
                },
                message=f'分块 {chunk_number} 上传成功'
            )
        
        return APIResponse.error(
            message='分块上传失败',
            details=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['post'])
    def upload_complete(self, request):
        serializer = ChunkUploadCompleteSerializer(data=request.data)
        
        if serializer.is_valid():
            data = serializer.validated_data
            upload_id = data['upload_id']
            
            chunks = UploadChunk.objects.filter(upload_id=upload_id).exclude(chunk_number=0)
            first_chunk = UploadChunk.objects.filter(upload_id=upload_id, chunk_number=0).first()
            
            if not first_chunk:
                return APIResponse.error(
                    message='上传记录不存在',
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            if chunks.count() != first_chunk.total_chunks:
                return APIResponse.error(
                    message='分块上传未完成',
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            
            chunk_dir = os.path.join(settings.MEDIA_ROOT, 'chunks', upload_id)
            complete_file = BytesIO()
            
            for i in range(1, first_chunk.total_chunks + 1):
                chunk_path = os.path.join(chunk_dir, f'chunk_{i}')
                with open(chunk_path, 'rb') as chunk_file:
                    complete_file.write(chunk_file.read())
            
            complete_file.seek(0)
            
            file_hash = hashlib.md5(complete_file.read()).hexdigest()
            complete_file.seek(0)
            
            if file_hash != first_chunk.file_hash:
                import shutil
                shutil.rmtree(chunk_dir)
                UploadChunk.objects.filter(upload_id=upload_id).delete()
                return APIResponse.error(
                    message='文件哈希校验失败',
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            
            if Image.objects.filter(file_hash=file_hash).exists():
                existing_image = Image.objects.get(file_hash=file_hash)
                import shutil
                shutil.rmtree(chunk_dir)
                UploadChunk.objects.filter(upload_id=upload_id).delete()
                return APIResponse.success(
                    data=ImageSerializer(existing_image).data,
                    message='文件已存在'
                )
            
            img = PILImage.open(complete_file)
            
            from django.core.files.uploadedfile import InMemoryUploadedFile
            uploaded_file = InMemoryUploadedFile(
                complete_file,
                None,
                first_chunk.filename,
                f'image/{img.format.lower()}',
                complete_file.tell(),
                None
            )
            
            image = Image.objects.create(
                user=request.user,
                file=uploaded_file,
                filename=first_chunk.filename,
                file_size=first_chunk.total_size,
                file_hash=file_hash,
                width=img.width,
                height=img.height,
                format=img.format,
                album=data.get('album'),
                title=data.get('title', ''),
                description=data.get('description', ''),
                tags=data.get('tags', []),
                is_public=data.get('is_public', False),
                storage_backend=settings.STORAGE_BACKEND,
                storage_path=''
            )
            
            request.user.storage_used += first_chunk.total_size
            request.user.save(update_fields=['storage_used'])
            
            import shutil
            shutil.rmtree(chunk_dir)
            UploadChunk.objects.filter(upload_id=upload_id).delete()
            
            return APIResponse.success(
                data=ImageSerializer(image).data,
                message='图片上传成功',
                status_code=status.HTTP_201_CREATED
            )
        
        return APIResponse.error(
            message='完成上传失败',
            details=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['get'])
    def preview(self, request, pk=None):
        image = self.get_object()
        
        if not image.is_public and image.user != request.user:
            return APIResponse.error(
                message='无权访问该图片',
                status_code=status.HTTP_403_FORBIDDEN
            )
        
        image.increment_access_count()
        
        return APIResponse.success(
            data={
                'url': image.url,
                'width': image.width,
                'height': image.height,
                'format': image.format
            }
        )
    
    @action(detail=False, methods=['get'])
    def public(self, request):
        queryset = Image.objects.filter(is_public=True)
        
        queryset = queryset.order_by('-created_at')
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return APIResponse.success(data=serializer.data)


class PublicImageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ImageSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        return Image.objects.filter(is_public=True).select_related('album', 'user')
    
    @action(detail=True, methods=['get'])
    def preview(self, request, pk=None):
        image = self.get_object()
        image.increment_access_count()
        
        return APIResponse.success(
            data={
                'url': image.url,
                'width': image.width,
                'height': image.height,
                'format': image.format
            }
        )
