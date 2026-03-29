"""
后端 API 统一响应格式使用指南

本文件展示了如何在 Django ViewSet 中使用统一的 API 响应格式。
"""

from utils.response import StandardResponse, api_response, api_error
from rest_framework import status, viewsets
from rest_framework.decorators import action


# ==================== 标准 CRUD 操作 ====================

class ExampleViewSet(viewsets.ModelViewSet):
    """
    示例 ViewSet - 展示统一的 API 响应格式
    """
    
    def list(self, request, *args, **kwargs):
        """
        获取列表（分页）
        
        ✅ 正确做法：使用 StandardResponse 包装分页数据
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data).data
            # 返回：{ code: 0, message: "操作成功", data: { count, next, previous, results } }
            return StandardResponse(paginated_data)
        
        serializer = self.get_serializer(queryset, many=True)
        # 返回：{ code: 0, message: "操作成功", data: [...] }
        return StandardResponse(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        """
        获取单个对象
        
        ✅ 正确做法：直接返回序列化数据
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # 返回：{ code: 0, message: "操作成功", data: { id, title, ... } }
        return StandardResponse(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """
        创建对象
        
        ✅ 正确做法：使用 201 状态码
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # 返回：{ code: 0, message: "操作成功", data: { id, title, ... } }
        return StandardResponse(
            serializer.data,
            message='创建成功',
            status=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        """
        更新对象
        
        ✅ 正确做法：返回更新后的数据
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # 返回：{ code: 0, message: "操作成功", data: { id, title, ... } }
        return StandardResponse(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """
        删除对象
        
        ✅ 正确做法：使用 204 No Content
        """
        self.perform_destroy(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)


# ==================== 自定义动作 ====================

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """
        发布内容
        
        ✅ 正确做法：返回更新后的对象
        """
        instance = self.get_object()
        instance.status = 'published'
        instance.save()
        
        serializer = self.get_serializer(instance)
        # 返回：{ code: 0, message: "操作成功", data: { id, status: 'published', ... } }
        return StandardResponse(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        获取统计数据
        
        ✅ 正确做法：返回复杂数据结构
        """
        stats = {
            'total': 100,
            'published': 80,
            'drafts': 20,
            'views': 10000,
            'recent_items': []
        }
        
        # 返回：{ code: 0, message: "操作成功", data: { total, published, ... } }
        return StandardResponse(stats)
    
    @action(detail=False, methods=['post'])
    def batch_delete(self, request):
        """
        批量删除
        
        ✅ 正确做法：返回操作结果
        """
        ids = request.data.get('ids', [])
        
        if not ids:
            # 错误处理
            return api_error(
                message='请提供要删除的 ID 列表',
                error_type='bad_request',
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 执行删除...
        deleted_count = len(ids)
        
        # 返回：{ code: 0, message: "操作成功", data: { deleted_count, deleted_ids } }
        return api_response({
            'deleted_count': deleted_count,
            'deleted_ids': ids
        }, message=f'成功删除 {deleted_count} 条记录')


# ==================== 错误处理 ====================

    @action(detail=True, methods=['post'])
    def upload_file(self, request, pk=None):
        """
        上传文件
        
        ✅ 正确做法：各种错误场景处理
        """
        # 检查文件是否存在
        if 'file' not in request.FILES:
            return api_error(
                message='请上传文件',
                error_type='bad_request',
                status=status.HTTP_400_BAD_REQUEST
            )
        
        file = request.FILES['file']
        
        # 验证文件类型
        allowed_types = ['image/jpeg', 'image/png', 'video/mp4']
        if file.content_type not in allowed_types:
            return api_error(
                message=f'不支持的文件类型：{file.content_type}，只支持 JPG/PNG/MP4',
                error_type='unsupported_media_type',
                code='INVALID_FILE_TYPE',
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
            )
        
        # 验证文件大小
        max_size = 100 * 1024 * 1024  # 100MB
        if file.size > max_size:
            return api_error(
                message=f'文件大小超过限制（最大 100MB，当前 {file.size / 1024 / 1024:.2f}MB）',
                error_type='payload_too_large',
                code='FILE_TOO_LARGE',
                status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
            )
        
        # 保存文件...
        file_url = '/media/files/example.jpg'
        
        # 成功返回
        return api_response({
            'url': file_url,
            'filename': file.name,
            'size': file.size,
            'type': file.content_type
        }, message='文件上传成功', status=status.HTTP_201_CREATED)


# ==================== MediaViewSet 实际案例 ====================

class MediaViewSet(viewsets.ModelViewSet):
    """
    媒体文件视图集（实际案例）
    """
    
    def list(self, request, *args, **kwargs):
        """
        获取媒体列表（分页）
        
        ✅ 这是正确的实现方式
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data).data
            # 返回：
            # {
            #     "code": 0,
            #     "message": "操作成功",
            #     "data": {
            #         "count": 100,
            #         "next": "/api/media/?page=2",
            #         "previous": null,
            #         "results": [...]
            #     }
            # }
            return StandardResponse(paginated_data)
        
        serializer = self.get_serializer(queryset, many=True)
        return StandardResponse(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """
        上传媒体文件
        
        ✅ 使用 201 状态码和完整数据
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # 返回：
        # {
        #     "code": 0,
        #     "message": "操作成功",
        #     "data": {
        #         "id": "uuid",
        #         "file": "http://...",
        #         "filename": "...",
        #         ...
        #     }
        # }
        return StandardResponse(
            MediaSerializer(serializer.instance).data,
            status=status.HTTP_201_CREATED
        )


# ==================== 常见错误示例 ====================

"""
❌ 错误做法 1：直接返回 Response（没有统一包装）

def list(self, request, *args, **kwargs):
    queryset = self.get_queryset()
    serializer = self.get_serializer(queryset, many=True)
    return Response(serializer.data)  # ❌ 错误！前端无法统一处理

✅ 正确做法：

def list(self, request, *args, **kwargs):
    queryset = self.get_queryset()
    serializer = self.get_serializer(queryset, many=True)
    return StandardResponse(serializer.data)  # ✅ 正确！


❌ 错误做法 2：混用多种响应格式

def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    return Response({'success': True, 'data': serializer.data})  # ❌ 错误！

✅ 正确做法：

def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    return StandardResponse(serializer.data)  # ✅ 正确！


❌ 错误做法 3：错误时返回不规范的格式

if not file:
    return Response({'error': '请上传文件'})  # ❌ 错误！

✅ 正确做法：

if not file:
    return api_error(
        message='请上传文件',
        error_type='bad_request',
        status=status.HTTP_400_BAD_REQUEST
    )  # ✅ 正确！
"""


# ==================== 总结 ====================

"""
📋 核心要点：

1. ✅ 所有响应都使用 StandardResponse 或辅助函数
2. ✅ 成功响应：code=0, message="操作成功", data={实际数据}
3. ✅ 错误响应：code=状态码，message="错误信息", error="错误类型", data=null
4. ✅ 分页列表：data 包含 {count, next, previous, results}
5. ✅ 单个对象：data 包含对象字段
6. ✅ 数组：data 包含对象数组
7. ✅ 状态码：使用正确的 HTTP 状态码（200, 201, 204, 400, 404 等）

🎯 前端处理：

由于拦截器已经适配，前端代码无需修改：

const response = await api.get('/api/media/')
console.log(response.data) // 直接就是 data 字段的内容

// 错误处理
try {
    await api.post('/api/media/upload/', formData)
} catch (error) {
    console.log(error.response.data.message) // 错误信息
    console.log(error.response.data.error)   // 错误类型
}
"""
