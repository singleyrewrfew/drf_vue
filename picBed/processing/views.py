from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.cache import cache
import logging

from images.models import Image
from images.serializers import ImageSerializer
from .serializers import ImageProcessSerializer
from .tasks import process_image_task, batch_process_images
from core.responses import APIResponse

logger = logging.getLogger('picBed')


class ImageProcessingViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        try:
            image = Image.objects.get(pk=pk, user=request.user)
        except Image.DoesNotExist:
            return APIResponse.error(
                message='图片不存在',
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        serializer = ImageProcessSerializer(data=request.data)
        if not serializer.is_valid():
            return APIResponse.error(
                message='参数验证失败',
                details=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        operations = serializer.validated_data['operations']
        
        task = process_image_task.delay(image.id, operations)
        
        return APIResponse.success(
            data={
                'task_id': task.id,
                'image_id': image.id,
                'status': 'processing'
            },
            message='图片处理任务已提交'
        )
    
    @action(detail=False, methods=['post'])
    def batch_process(self, request):
        image_ids = request.data.get('image_ids', [])
        operations = request.data.get('operations', [])
        
        if not image_ids:
            return APIResponse.error(
                message='图片ID列表不能为空',
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        if not operations:
            return APIResponse.error(
                message='操作列表不能为空',
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        valid_images = Image.objects.filter(
            id__in=image_ids,
            user=request.user
        )
        
        if valid_images.count() != len(image_ids):
            return APIResponse.error(
                message='部分图片不存在或无权访问',
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        task = batch_process_images.delay(image_ids, operations)
        
        return APIResponse.success(
            data={
                'task_id': task.id,
                'image_count': len(image_ids),
                'status': 'processing'
            },
            message='批量处理任务已提交'
        )
    
    @action(detail=True, methods=['post'])
    def compress(self, request, pk=None):
        try:
            image = Image.objects.get(pk=pk, user=request.user)
        except Image.DoesNotExist:
            return APIResponse.error(
                message='图片不存在',
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        quality = request.data.get('quality', 85)
        format = request.data.get('format')
        
        operations = [{
            'type': 'compress',
            'params': {
                'quality': quality,
                'format': format
            }
        }]
        
        task = process_image_task.delay(image.id, operations)
        
        return APIResponse.success(
            data={
                'task_id': task.id,
                'image_id': image.id
            },
            message='压缩任务已提交'
        )
    
    @action(detail=True, methods=['post'])
    def convert(self, request, pk=None):
        try:
            image = Image.objects.get(pk=pk, user=request.user)
        except Image.DoesNotExist:
            return APIResponse.error(
                message='图片不存在',
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        target_format = request.data.get('target_format')
        if not target_format:
            return APIResponse.error(
                message='目标格式不能为空',
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        operations = [{
            'type': 'convert',
            'params': {
                'target_format': target_format
            }
        }]
        
        task = process_image_task.delay(image.id, operations)
        
        return APIResponse.success(
            data={
                'task_id': task.id,
                'image_id': image.id
            },
            message='格式转换任务已提交'
        )
    
    @action(detail=True, methods=['post'])
    def resize(self, request, pk=None):
        try:
            image = Image.objects.get(pk=pk, user=request.user)
        except Image.DoesNotExist:
            return APIResponse.error(
                message='图片不存在',
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        width = request.data.get('width')
        height = request.data.get('height')
        maintain_aspect = request.data.get('maintain_aspect', True)
        
        if not width and not height:
            return APIResponse.error(
                message='至少需要提供宽度或高度',
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        operations = [{
            'type': 'resize',
            'params': {
                'width': width,
                'height': height,
                'maintain_aspect': maintain_aspect
            }
        }]
        
        task = process_image_task.delay(image.id, operations)
        
        return APIResponse.success(
            data={
                'task_id': task.id,
                'image_id': image.id
            },
            message='尺寸调整任务已提交'
        )
    
    @action(detail=True, methods=['post'])
    def watermark(self, request, pk=None):
        try:
            image = Image.objects.get(pk=pk, user=request.user)
        except Image.DoesNotExist:
            return APIResponse.error(
                message='图片不存在',
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        watermark_text = request.data.get('watermark_text')
        position = request.data.get('position', 'bottom-right')
        opacity = request.data.get('opacity', 128)
        
        if not watermark_text:
            return APIResponse.error(
                message='水印文本不能为空',
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        operations = [{
            'type': 'watermark',
            'params': {
                'watermark_text': watermark_text,
                'position': position,
                'opacity': opacity
            }
        }]
        
        task = process_image_task.delay(image.id, operations)
        
        return APIResponse.success(
            data={
                'task_id': task.id,
                'image_id': image.id
            },
            message='水印添加任务已提交'
        )
