from rest_framework import serializers

from apps.tags.serializers import TagSerializer
from utils.serializer_mixins import AutoSlugMixin
from utils.html_utils import sanitize_html
from .models import Content


def extract_media_path(url):
    """从 URL 中提取媒体文件相对路径（去掉 /media/ 前缀）"""
    if not url:
        return None
    if url.startswith('http://') or url.startswith('https://'):
        try:
            from urllib.parse import urlparse
            path = urlparse(url).path
            if path.startswith('/media/'):
                return path[7:]  # 去掉 /media/
            return path.lstrip('/')
        except Exception:
            return None
    # 如果是相对路径 (如 /media/xxx),去掉 /media/ 前缀
    if url.startswith('/media/'):
        return url[7:]
    return url


class ContentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    author_avatar = serializers.ImageField(source='author.avatar', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    content_preview = serializers.SerializerMethodField(help_text='文章预览内容（前 5000 字符）')

    class Meta:
        model = Content
        fields = [
            'id', 'title', 'slug', 'summary', 'content', 'content_preview', 'cover_image',
            'author', 'author_name', 'author_avatar', 'category', 'category_name', 'category_slug', 'tags',
            'status', 'view_count', 'is_top', 'published_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'view_count', 'created_at', 'updated_at']

    def get_content_preview(self, obj):
        """
        返回文章预览内容（前 5000 个字符）

        结果返回给fields配置里的content_preview，最终返回给前端

        !!!注意：fields必须配置了 content_preview 才会触发
        """
        if not obj.content:
            return ''
        return obj.content[:5000] if len(obj.content) > 5000 else obj.content


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


class ContentCreateUpdateSerializer(AutoSlugMixin, serializers.ModelSerializer):
    slug_source_field = 'title'
    tags = serializers.ListField(child=serializers.UUIDField(), write_only=True, required=False)
    category = serializers.PrimaryKeyRelatedField(allow_null=True, required=False, queryset=Content._meta.get_field('category').related_model.objects.all())
    cover_image = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    status = serializers.CharField(required=False, default='draft')
    is_top = serializers.BooleanField(required=False, default=False)
    author = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, queryset=Content._meta.get_field('author').related_model.objects.all())

    class Meta:
        model = Content
        fields = [
            'title', 'slug', 'summary', 'content', 'cover_image',
            'category', 'tags', 'status', 'is_top', 'author'
        ]

    def validate_cover_image(self, value):
        if not value:
            return None
        return value

    def validate_content(self, value):
        return sanitize_html(value)

    def validate_summary(self, value):
        return sanitize_html(value) if value else value

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        cover_image_url = validated_data.pop('cover_image', None)

        request = self.context.get('request')
        if request and request.user.is_authenticated:
            if 'author' not in validated_data or not validated_data.get('author'):
                validated_data['author'] = request.user

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
