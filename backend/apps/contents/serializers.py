import uuid

from django.utils.text import slugify
from rest_framework import serializers

from apps.categories.serializers import CategorySerializer
from apps.tags.serializers import TagSerializer

from .models import Content


def extract_media_path(url):
    """从 URL 中提取媒体文件相对路径"""
    if not url:
        return None
    if url.startswith('http://') or url.startswith('https://'):
        try:
            from urllib.parse import urlparse
            path = urlparse(url).path
            if path.startswith('/media/'):
                return path[7:]
            return path.lstrip('/')
        except Exception:
            return None
    return url


class ContentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    author_avatar = serializers.ImageField(source='author.avatar', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Content
        fields = [
            'id', 'title', 'slug', 'summary', 'content', 'cover_image',
            'author', 'author_name', 'author_avatar', 'category', 'category_name', 'tags',
            'status', 'view_count', 'is_top', 'published_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'view_count', 'created_at', 'updated_at']


class ContentListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    author_avatar = serializers.ImageField(source='author.avatar', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Content
        fields = [
            'id', 'title', 'slug', 'summary', 'cover_image',
            'author_name', 'author_avatar', 'category_name', 'tags',
            'status', 'view_count', 'is_top', 'published_at', 'created_at'
        ]


class ContentCreateUpdateSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.UUIDField(), write_only=True, required=False)
    category = serializers.PrimaryKeyRelatedField(allow_null=True, required=False, queryset=Content._meta.get_field('category').related_model.objects.all())
    cover_image = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    status = serializers.CharField(required=False, default='draft')
    is_top = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = Content
        fields = [
            'title', 'slug', 'summary', 'content', 'cover_image',
            'category', 'tags', 'status', 'is_top'
        ]

    def validate_cover_image(self, value):
        if not value:
            return None
        return value

    def validate(self, data):
        if not data.get('slug'):
            base_slug = slugify(data['title'])
            if not base_slug:
                base_slug = uuid.uuid4().hex[:8]
            slug = base_slug
            counter = 1
            while Content.objects.filter(slug=slug).exclude(id=self.instance.id if self.instance else None).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            data['slug'] = slug
        return data

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        cover_image_url = validated_data.pop('cover_image', None)
        
        content = Content.objects.create(**validated_data)
        
        if cover_image_url:
            relative_path = extract_media_path(cover_image_url)
            if relative_path:
                content.cover_image.name = relative_path
                content.save(update_fields=['cover_image'])
        
        if tags_data:
            from apps.tags.models import Tag
            content.tags.set(Tag.objects.filter(id__in=tags_data))
        return content

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        cover_image_url = validated_data.pop('cover_image', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if cover_image_url is not None:
            if cover_image_url:
                relative_path = extract_media_path(cover_image_url)
                if relative_path:
                    instance.cover_image.name = relative_path
                else:
                    instance.cover_image = None
            else:
                instance.cover_image = None
        
        instance.save()
        
        if tags_data is not None:
            from apps.tags.models import Tag
            instance.tags.set(Tag.objects.filter(id__in=tags_data))
        return instance
