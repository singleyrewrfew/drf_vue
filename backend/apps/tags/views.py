from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.users.permissions import IsEditorUser

from .models import Tag
from .serializers import TagCreateUpdateSerializer, TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TagCreateUpdateSerializer
        return TagSerializer

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs.get(lookup_url_kwarg)
        
        # 尝试通过 slug 或 UUID 查找
        try:
            import uuid
            uuid.UUID(lookup_value)
            return super().get_object()
        except (ValueError, AttributeError):
            # 如果不是有效的 UUID，尝试通过 slug 查找
            try:
                obj = Tag.objects.get(slug=lookup_value)
                self.check_object_permissions(self.request, obj)
                return obj
            except Tag.DoesNotExist:
                from django.http import Http404
                raise Http404('No Tag matches the given query.')

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsEditorUser()]
        return super().get_permissions()
