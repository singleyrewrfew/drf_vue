"""
ViewSet Mixin 类

提供常用的 ViewSet 功能扩展。
"""

import uuid


class SlugOrUUIDMixin:
    """
    支持通过 slug 或 UUID 查找对象的 Mixin
    
    使用方法：
    1. 在 ViewSet 中继承此 Mixin
    2. 确保模型有 slug 字段和 UUID 主键（或 id 字段）
    
    功能：
    - 自动识别 lookup_field 的值是 slug 还是 UUID
    - 如果是 UUID，直接按 ID 查找
    - 如果是 slug，按 slug 字段查找
    
    Example:
        class CategoryViewSet(SlugOrUUIDMixin, viewsets.ModelViewSet):
            queryset = Category.objects.all()
            lookup_field = 'pk'  # 可以是 pk、id 或 slug
    """
    
    def get_object(self):
        """
        重写获取对象方法，支持 slug 或 UUID
        
        根据 lookup_field 的值智能判断：
        - 如果是有效的 UUID 格式，按主键查找
        - 否则尝试按 slug 字段查找（如果模型有 slug 字段）
        - 最后按主键查找
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        # 获取查找字段的值
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs[lookup_url_kwarg]
        
        # 尝试判断是否为 UUID
        try:
            uuid.UUID(str(lookup_value))
            # 是 UUID，按主键查找
            filter_kwargs = {self.lookup_field: lookup_value}
        except (ValueError, AttributeError):
            # 不是 UUID，可能是 slug
            # 优先尝试按 slug 字段查找（如果模型有 slug 字段）
            model = self.queryset.model
            if hasattr(model, 'slug'):
                filter_kwargs = {'slug': lookup_value}
            else:
                # 模型没有 slug 字段，按主键查找
                filter_kwargs = {self.lookup_field: lookup_value}
        
        # 执行查询
        obj = queryset.filter(**filter_kwargs).first()
        
        if obj is None:
            from rest_framework.exceptions import NotFound
            raise NotFound(f'未找到{self.queryset.model._meta.verbose_name}')
        
        # 检查对象权限
        self.check_object_permissions(self.request, obj)
        
        return obj
