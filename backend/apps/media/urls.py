from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MediaViewSet
from .sse_views import thumbnail_status_stream

router = DefaultRouter()
router.register(r'', MediaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<uuid:media_id>/thumbnail_status/', thumbnail_status_stream, name='thumbnail-status-stream'),
]
