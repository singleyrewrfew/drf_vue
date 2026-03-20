from rest_framework import serializers

from utils.serializer_mixins import AutoSlugMixin
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    content_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'description', 'sort_order', 'created_at', 'children', 'content_count']
        read_only_fields = ['id', 'slug', 'created_at']

    def get_children(self, obj):
        children = obj.children.all()
        return CategorySerializer(children, many=True).data

    def get_content_count(self, obj):
        return obj.contents.filter(status='published').count()


class CategoryListSerializer(serializers.ModelSerializer):
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    content_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'parent_name', 'description', 'sort_order', 'created_at', 'content_count']

    def get_content_count(self, obj):
        return obj.contents.filter(status='published').count()


class CategoryCreateUpdateSerializer(AutoSlugMixin, serializers.ModelSerializer):
    slug_source_field = 'name'
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'description', 'sort_order']
