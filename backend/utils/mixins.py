import uuid

from django.http import Http404


class SlugOrUUIDMixin:
    """
    用于 ViewSet 的混入类，支持通过 UUID 或 slug 查找对象。
    
    此混入类重写了 get_object 方法，允许通过以下方式查找对象：
    - UUID（主键）
    - slug 字段
    
    使用示例：
        class MyViewSet(SlugOrUUIDMixin, viewsets.ModelViewSet):
            queryset = MyModel.objects.all()
            slug_field = 'slug'  # 可选，默认为 'slug'
    """
    # 定义 slug 字段名称，默认为 'slug'
    slug_field = 'slug'
    
    def get_object(self):
        """
        重写获取对象的方法，支持 UUID 和 slug 两种查找方式。
        
        首先尝试将传入的值解析为 UUID，如果成功则使用默认的 get_object 方法（按主键查找）。
        如果解析失败，则尝试按 slug 字段查找对象。
        """
        # 获取查找用的 URL 关键字参数，优先使用 lookup_url_kwarg，否则使用 lookup_field
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        # 从 URL _kwargs 中获取查找值
        lookup_value = self.kwargs.get(lookup_url_kwarg)
        
        # 尝试将查找值解析为 UUID
        try:
            uuid.UUID(lookup_value)
            # 如果是有效的 UUID，调用父类的 get_object 方法（按主键查找）
            return super().get_object()
        except (ValueError, AttributeError):
            # 如果不是有效的 UUID，尝试按 slug 查找
            try:
                # 获取查询集的模型类
                model_class = self.queryset.model
                # 构造过滤条件，使用 slug_field 作为查找字段
                filter_kwargs = {self.slug_field: lookup_value}
                # 根据 slug 查找对象
                obj = model_class.objects.get(**filter_kwargs)
                # 检查用户是否有权限访问该对象
                self.check_object_permissions(self.request, obj)
                return obj
            except model_class.DoesNotExist:
                # 如果对象不存在，抛出 404 错误
                model_name = model_class.__name__
                raise Http404(f'No {model_name} matches the given query.')
