from django.core.cache import cache
from django.db.models import Count, Prefetch, Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.users.permissions import IsEditorUser
from utils.viewset_mixins import SlugOrUUIDMixin
from utils.response import StandardResponse
from utils.cache_utils import get_cache_key

from .models import Category
from .serializers import (
    CategoryChildSerializer,
    CategoryCreateUpdateSerializer,
    CategoryListSerializer,
    CategorySerializer,
)

CACHE_KEY_CATEGORIES = 'categories:list'


class CategorySerializerMixin:
    default_serializer_class = CategorySerializer

    def get_serializer_class(self):
        serializer_mapping = {
            'list': CategoryListSerializer,
            'create': CategoryCreateUpdateSerializer,
            'update': CategoryCreateUpdateSerializer,
            'partial_update': CategoryCreateUpdateSerializer,
        }
        return serializer_mapping.get(self.action, self.default_serializer_class)


class CategoryPermissionMixin:
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsEditorUser()]
        return super().get_permissions()


class CategoryViewSet(
    CategoryPermissionMixin,
    CategorySerializerMixin,
    SlugOrUUIDMixin,
    viewsets.ModelViewSet
):
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == 'list':
            queryset = queryset.select_related('parent').annotate(
                content_count=Count('contents', filter=Q(contents__status='published'))
            )
        elif self.action == 'retrieve':
            children_qs = Category.objects.annotate(
                content_count=Count('contents', filter=Q(contents__status='published'))
            )
            queryset = queryset.prefetch_related(
                Prefetch('children', queryset=children_qs, to_attr='prefetched_children')
            ).annotate(
                content_count=Count('contents', filter=Q(contents__status='published'))
            )

        return queryset

    def list(self, request, *args, **kwargs):
        cache_key = get_cache_key(CACHE_KEY_CATEGORIES)
        cached_data = cache.get(cache_key)
        if cached_data:
            return StandardResponse(cached_data)

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data).data
            cache.set(cache_key, paginated_data, 300)
            return StandardResponse(paginated_data)

        serializer = self.get_serializer(queryset, many=True)
        cache.set(cache_key, serializer.data, 300)
        return StandardResponse(serializer.data)

    def perform_create(self, serializer):
        serializer.save()
        cache.delete(get_cache_key(CACHE_KEY_CATEGORIES))

    def perform_update(self, serializer):
        serializer.save()
        cache.delete(get_cache_key(CACHE_KEY_CATEGORIES))

    def perform_destroy(self, instance):
        instance.delete()
        cache.delete(get_cache_key(CACHE_KEY_CATEGORIES))
