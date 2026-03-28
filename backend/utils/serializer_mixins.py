from utils.slug_utils import generate_unique_slug


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
