from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.users.permissions import IsEditorUser

from .models import Category
from .serializers import CategoryListSerializer, CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryListSerializer
        return CategorySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsEditorUser()]
        return super().get_permissions()

    def perform_create(self, serializer):
        if not serializer.validated_data.get('slug'):
            from django.utils.text import slugify
            serializer.save(slug=slugify(serializer.validated_data['name']))
        else:
            serializer.save()
