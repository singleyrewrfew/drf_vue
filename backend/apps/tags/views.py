from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.users.permissions import IsEditorUser
from utils.viewset_mixins import SlugOrUUIDMixin
from utils.response import StandardResponse
from utils.cache_utils import get_cache_key
from .models import Tag
from .serializers import TagCreateUpdateSerializer, TagSerializer

CACHE_KEY_TAGS = 'tags:list'


class TagSerializerMixin:
    default_serializer_class = TagSerializer

    def get_serializer_class(self):
        serializer_mapping = {
            'create': TagCreateUpdateSerializer,
            'update': TagCreateUpdateSerializer,
            'partial_update': TagCreateUpdateSerializer,
        }
        return serializer_mapping.get(self.action, self.default_serializer_class)


class TagPermissionMixin:
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsEditorUser()]
        return super().get_permissions()


class TagViewSet(
    TagPermissionMixin,
    TagSerializerMixin,
    SlugOrUUIDMixin,
    viewsets.ModelViewSet
):
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'

    def list(self, request, *args, **kwargs):
        cache_key = get_cache_key(CACHE_KEY_TAGS)
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
        cache.delete(get_cache_key(CACHE_KEY_TAGS))

    def perform_update(self, serializer):
        serializer.save()
        cache.delete(get_cache_key(CACHE_KEY_TAGS))

    def perform_destroy(self, instance):
        instance.delete()
        cache.delete(get_cache_key(CACHE_KEY_TAGS))
