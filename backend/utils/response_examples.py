"""
API 响应格式使用示例

本文件展示了如何在 views 中使用统一的 API 响应格式
"""

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from utils.response import StandardResponse, api_response, api_error


class ExampleViewSet(viewsets.ModelViewSet):
    """
    示例 ViewSet - 展示统一的 API 响应格式
    """
    
    # ==================== 标准 CRUD 操作 ====================
    
    def list(self, request, *args, **kwargs):
        """
        获取列表 - 使用 DRF 默认的分页格式
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # DRF 分页格式会自动包含 count, next, previous, results
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return StandardResponse(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        """
        获取单个对象 - 直接返回数据
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return StandardResponse(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """
        创建对象 - 返回创建的对象
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # 返回 201 状态码和创建的对象
        return StandardResponse(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        """
        更新对象 - 返回更新后的对象
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return StandardResponse(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """
        删除对象 - 返回 204 No Content
        """
        self.perform_destroy(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    # ==================== 自定义动作 ====================
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """
        发布内容 - 返回更新后的对象
        """
        instance = self.get_object()
        instance.status = 'published'
        instance.save()
        
        serializer = self.get_serializer(instance)
        return StandardResponse(serializer.data)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """
        审核评论 - 使用 api_response 辅助函数
        """
        comment = self.get_object()
        comment.is_approved = True
        comment.save()
        
        serializer = self.get_serializer(comment)
        return api_response(serializer.data)
    
    # ==================== 错误处理 ====================
    
    @action(detail=True, methods=['post'])
    def upload_file(self, request, pk=None):
        """
        上传文件 - 展示错误处理
        """
        if 'file' not in request.FILES:
            # 使用统一的错误格式
            return api_error(
                message='请上传文件',
                error_type='bad_request',
                status=status.HTTP_400_BAD_REQUEST
            )
        
        file = request.FILES['file']
        
        # 验证文件类型
        allowed_types = ['image/jpeg', 'image/png']
        if file.content_type not in allowed_types:
            return api_error(
                message='只支持 JPG/PNG 格式的图片',
                error_type='unsupported_media_type',
                code='INVALID_FILE_TYPE',
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
            )
        
        # 验证文件大小
        if file.size > 10 * 1024 * 1024:
            return api_error(
                message='图片大小不能超过 10MB',
                error_type='payload_too_large',
                code='FILE_TOO_LARGE',
                status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
            )
        
        # 保存文件...
        file_url = '/media/files/example.jpg'
        
        # 返回成功
        return api_response({
            'url': file_url,
            'filename': file.name
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        搜索 - 展示验证错误
        """
        keyword = request.query_params.get('q')
        
        if not keyword:
            return api_error(
                message='搜索关键词不能为空',
                error_type='bad_request',
                code='MISSING_KEYWORD',
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if len(keyword) < 2:
            return api_error(
                message='搜索关键词至少 2 个字符',
                error_type='bad_request',
                code='KEYWORD_TOO_SHORT',
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 执行搜索...
        results = []
        return StandardResponse(results)
    
    # ==================== 特殊场景 ====================
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        统计数据 - 返回复杂数据结构
        """
        stats = {
            'total': 100,
            'published': 80,
            'drafts': 20,
            'views': 10000,
            'recent_items': []
        }
        
        return StandardResponse(stats)
    
    @action(detail=False, methods=['post'])
    def batch_delete(self, request):
        """
        批量删除 - 返回操作结果
        """
        ids = request.data.get('ids', [])
        
        if not ids:
            return api_error(
                message='请提供要删除的 ID 列表',
                error_type='bad_request',
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 执行批量删除...
        deleted_count = len(ids)
        
        # 返回删除结果（可选）
        return api_response({
            'deleted_count': deleted_count,
            'deleted_ids': ids
        })


# ==================== 使用建议 ====================

"""
推荐做法：

1. ✅ 标准 CRUD 操作
   - list: 返回序列化数据（DRF 分页格式）
   - retrieve: 返回单个对象
   - create: 返回 201 + 创建的对象
   - update: 返回更新后的对象
   - destroy: 返回 204 No Content

2. ✅ 自定义动作
   - 成功时：StandardResponse(data)
   - 需要消息：api_response(data, message='...')
   - 错误时：api_error('错误信息', error_type='...', status=400)

3. ✅ 错误处理
   - 400: 请求参数错误
   - 401: 未授权（登录）
   - 403: 禁止访问（权限不足）
   - 404: 资源不存在
   - 409: 资源冲突（如重复）
   - 413: 文件过大
   - 415: 不支持的媒体类型
   - 500: 服务器内部错误

4. ❌ 避免的做法
   - 不要返回 {'code': 0, 'message': '成功', 'data': {...}}
   - 不要在成功时总是包装 message
   - 不要混用多种响应格式

5. 📝 前端处理建议
   - 成功响应：直接使用 response.data
   - 错误响应：检查 response.data.error 和 response.data.message
   - HTTP 状态码：用于判断请求类型（2xx 成功，4xx 客户端错误，5xx 服务器错误）
"""
