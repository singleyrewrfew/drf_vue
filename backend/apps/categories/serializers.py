from rest_framework import serializers

from utils.serializer_mixins import AutoSlugMixin
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    content_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'description', 'sort_order', 'created_at', 'children', 'content_count']
        read_only_fields = ['id', 'slug', 'created_at']

    def get_children(self, obj):
        children = getattr(obj, 'prefetched_children', None)
        if children is None:
            children = obj.children.all()
        return CategoryChildSerializer(children, many=True).data


class CategoryChildSerializer(serializers.ModelSerializer):
    content_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'sort_order', 'content_count']


class CategoryListSerializer(serializers.ModelSerializer):
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    content_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'parent_name', 'description', 'sort_order', 'created_at', 'content_count']


class CategoryCreateUpdateSerializer(AutoSlugMixin, serializers.ModelSerializer):
    slug_source_field = 'name'

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'description', 'sort_order']
