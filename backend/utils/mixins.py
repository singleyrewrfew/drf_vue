import uuid

from django.http import Http404


class SlugOrUUIDMixin:
    """
    Mixin for ViewSet to support lookup by UUID or slug.
    
    This mixin overrides get_object to allow finding objects by either:
    - UUID (primary key)
    - slug field
    
    Usage:
        class MyViewSet(SlugOrUUIDMixin, viewsets.ModelViewSet):
            queryset = MyModel.objects.all()
            slug_field = 'slug'  # Optional, defaults to 'slug'
    """
    slug_field = 'slug'
    
    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs.get(lookup_url_kwarg)
        
        try:
            uuid.UUID(lookup_value)
            return super().get_object()
        except (ValueError, AttributeError):
            try:
                model_class = self.queryset.model
                filter_kwargs = {self.slug_field: lookup_value}
                obj = model_class.objects.get(**filter_kwargs)
                self.check_object_permissions(self.request, obj)
                return obj
            except model_class.DoesNotExist:
                model_name = model_class.__name__
                raise Http404(f'No {model_name} matches the given query.')
