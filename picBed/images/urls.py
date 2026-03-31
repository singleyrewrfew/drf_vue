from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlbumViewSet, ImageViewSet, PublicImageViewSet

router = DefaultRouter()
router.register(r'albums', AlbumViewSet, basename='albums')
router.register(r'', ImageViewSet, basename='images')
router.register(r'public', PublicImageViewSet, basename='public-images')

urlpatterns = [
    path('', include(router.urls)),
]
