from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.users.permissions import IsEditorUser
from utils.viewset_mixins import CachedListMixin, SlugOrUUIDMixin
from .models import Tag
from .serializers import TagCreateUpdateSerializer, TagSerializer


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
    CachedListMixin,
    TagPermissionMixin,
    TagSerializerMixin,
    SlugOrUUIDMixin,
    viewsets.ModelViewSet
):
    cache_key_prefix = 'tags:list'
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
