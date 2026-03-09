from django.utils.text import slugify
from rest_framework import serializers

from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'description', 'sort_order', 'created_at', 'children']
        read_only_fields = ['id', 'slug', 'created_at']

    def get_children(self, obj):
        children = obj.children.all()
        return CategorySerializer(children, many=True).data


class CategoryListSerializer(serializers.ModelSerializer):
    parent_name = serializers.CharField(source='parent.name', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'parent_name', 'description', 'sort_order', 'created_at']


class CategoryCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'parent', 'description', 'sort_order']

    def validate(self, data):
        if not data.get('slug'):
            base_slug = slugify(data['name'])
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exclude(id=self.instance.id if self.instance else None).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            data['slug'] = slug
        return data
