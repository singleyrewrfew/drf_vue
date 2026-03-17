import uuid

from django.utils.text import slugify


def generate_unique_slug(model_class, base_text, instance=None, slug_field='slug'):
    """
    Generate a unique slug for a model instance.
    
    Args:
        model_class: The Django model class
        base_text: The text to slugify
        instance: The current instance (for updates, to exclude from uniqueness check)
        slug_field: The name of the slug field
    
    Returns:
        A unique slug string
    """
    base_slug = slugify(base_text)
    if not base_slug:
        base_slug = uuid.uuid4().hex[:8]
    
    slug = base_slug
    counter = 1
    
    queryset = model_class.objects.all()
    if instance and instance.pk:
        queryset = queryset.exclude(pk=instance.pk)
    
    while queryset.filter(**{slug_field: slug}).exists():
        slug = f'{base_slug}-{counter}'
        counter += 1
    
    return slug


class AutoSlugMixin:
    """
    Mixin for ModelSerializer to auto-generate unique slugs.
    
    Attributes:
        slug_source_field: The field to use as source for slug generation (default: 'name')
        slug_field: The field to store the slug (default: 'slug')
    
    Usage:
        class MySerializer(AutoSlugMixin, serializers.ModelSerializer):
            slug_source_field = 'title'
            slug_field = 'slug'
            
            class Meta:
                model = MyModel
                fields = [...]
    """
    slug_source_field = 'name'
    slug_field = 'slug'
    
    def validate(self, data):
        data = super().validate(data)
        
        if not data.get(self.slug_field):
            source_value = data.get(self.slug_source_field, '')
            model_class = self.Meta.model
            data[self.slug_field] = generate_unique_slug(
                model_class,
                source_value,
                instance=self.instance,
                slug_field=self.slug_field
            )
        
        return data
