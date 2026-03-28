import uuid

from django.utils.text import slugify


def generate_unique_slug(model_class, base_text, instance=None, slug_field='slug'):
    """
    为 Django 模型实例生成唯一的 slug。
    
    参数说明：
        model_class: Django 模型类，用于查询和验证 slug 的唯一性
        base_text: 要转换为 slug 的原始文本，会被 slugify 处理
        instance: 当前实例对象（用于更新操作），在唯一性检查时会排除此实例
        slug_field: slug 字段的名称，默认为 'slug'
    
    返回值：
        返回一个在数据库中唯一的 slug 字符串
    
    工作流程：
        1. 将 base_text 转换为 slug 格式
        2. 如果转换结果为空，生成随机 UUID 作为基础 slug
        3. 检查 slug 是否已存在，如果存在则添加数字后缀
        4. 返回第一个不重复的 slug
    """
    # 将基础文本转换为 slug 格式
    base_slug = slugify(base_text)
    # 如果 slug 为空，使用 UUID 的前 8 位作为默认值
    if not base_slug:
        base_slug = uuid.uuid4().hex[:8]
    
    # 初始化 slug 和计数器
    slug = base_slug
    counter = 1
    
    # 构建查询集，用于检查 slug 的唯一性
    queryset = model_class.objects.all()
    # 如果是更新操作，排除当前实例本身
    if instance and instance.pk:
        queryset = queryset.exclude(pk=instance.pk)
    
    # 循环检查 slug 是否已存在，如果存在则添加数字后缀
    while queryset.filter(**{slug_field: slug}).exists():
        slug = f'{base_slug}-{counter}'
        counter += 1
    
    return slug


class AutoSlugMixin:
    """
    用于 ModelSerializer 的混入类，自动生成唯一的 slug。
    
    此混入类在序列化器的 validate 方法中自动为模型实例生成 slug，
    当 slug 字段未提供时，会根据指定的源字段自动生成唯一 slug。
    
    属性说明：
        slug_source_field: 用于生成 slug 的源字段名称，默认为 'name'
                           该字段的值会被转换为 slug 格式
        slug_field: 存储 slug 的字段名称，默认为 'slug'
    
    使用示例：
        class MySerializer(AutoSlugMixin, serializers.ModelSerializer):
            slug_source_field = 'title'  # 使用 title 字段作为 slug 源
            slug_field = 'slug'          # slug 存储在 slug 字段
            
            class Meta:
                model = MyModel
                fields = [...]
    
    注意事项：
        - 必须与 serializers.ModelSerializer 一起使用
        - 源字段的值会在验证阶段被自动转换为 slug
        - 生成的 slug 保证在数据库中唯一
    """
    # 定义 slug 源字段名称，默认为 'name'
    slug_source_field = 'name'
    # 定义 slug 字段名称，默认为 'slug'
    slug_field = 'slug'
    
    def validate(self, data):
        """
        重写验证方法，在数据验证阶段自动生成 slug。
        
        参数：
            data: 待验证的序列化数据字典
        
        返回：
            验证通过的数据字典，包含自动生成的 slug 字段
        """
        # 调用父类的验证方法
        data = super().validate(data)
        
        # 如果用户未提供 slug 字段，则自动生成
        if not data.get(self.slug_field):
            # 获取源字段的值
            source_value = data.get(self.slug_source_field, '')
            # 获取关联的模型类
            model_class = self.Meta.model
            # 生成唯一的 slug 并赋值
            data[self.slug_field] = generate_unique_slug(
                model_class,
                source_value,
                instance=self.instance,
                slug_field=self.slug_field
            )
        
        return data
