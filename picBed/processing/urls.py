from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ImageProcessingViewSet

router = DefaultRouter()
router.register(r'process', ImageProcessingViewSet, basename='image-processing')

urlpatterns = [
    path('', include(router.urls)),
]
