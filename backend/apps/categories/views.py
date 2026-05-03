from django.db.models import Count, Prefetch, Q
from django.conf import settings
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.users.permissions import IsEditorUser
from utils.viewset_mixins import CachedListMixin, SlugOrUUIDMixin

from .models import Category
from .serializers import (
    CategoryCreateUpdateSerializer,
    CategoryListSerializer,
    CategorySerializer,
)


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
    CachedListMixin,
    CategoryPermissionMixin,
    CategorySerializerMixin,
    SlugOrUUIDMixin,
    viewsets.ModelViewSet
):
    cache_key_prefix = 'categories:list'
    cache_timeout = settings.CACHE_TTL['CATEGORY_LIST']
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
