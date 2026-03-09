from rest_framework import serializers

from apps.categories.serializers import CategorySerializer
from apps.tags.serializers import TagSerializer

from .models import Content


class ContentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Content
        fields = [
            'id', 'title', 'slug', 'summary', 'content', 'cover_image',
            'author', 'author_name', 'category', 'category_name', 'tags',
            'status', 'view_count', 'is_top', 'published_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'view_count', 'created_at', 'updated_at']


class ContentListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Content
        fields = [
            'id', 'title', 'slug', 'summary', 'cover_image',
            'author_name', 'category_name', 'tags',
            'status', 'view_count', 'is_top', 'published_at', 'created_at'
        ]


class ContentCreateUpdateSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.UUIDField(), write_only=True, required=False)

    class Meta:
        model = Content
        fields = [
            'title', 'slug', 'summary', 'content', 'cover_image',
            'category', 'tags', 'status', 'is_top'
        ]

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        content = Content.objects.create(**validated_data)
        if tags_data:
            from apps.tags.models import Tag
            content.tags.set(Tag.objects.filter(id__in=tags_data))
        return content

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tags_data is not None:
            from apps.tags.models import Tag
            instance.tags.set(Tag.objects.filter(id__in=tags_data))
        return instance
