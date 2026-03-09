from rest_framework import serializers

from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'description', 'sort_order', 'created_at', 'children']
        read_only_fields = ['id', 'created_at']

    def get_children(self, obj):
        children = obj.children.all()
        return CategorySerializer(children, many=True).data


class CategoryListSerializer(serializers.ModelSerializer):
    parent_name = serializers.CharField(source='parent.name', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'parent_name', 'description', 'sort_order', 'created_at']
