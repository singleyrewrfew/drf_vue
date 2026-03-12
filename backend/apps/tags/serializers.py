from django.utils.text import slugify
from rest_framework import serializers

from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    content_count = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'created_at', 'content_count']
        read_only_fields = ['id', 'slug', 'created_at']

    def get_content_count(self, obj):
        return obj.contents.filter(status='published').count()


class TagCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name', 'slug']

    def validate(self, data):
        if not data.get('slug'):
            base_slug = slugify(data['name'])
            slug = base_slug
            counter = 1
            while Tag.objects.filter(slug=slug).exclude(id=self.instance.id if self.instance else None).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            data['slug'] = slug
        return data
