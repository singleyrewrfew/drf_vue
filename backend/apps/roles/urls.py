from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PermissionViewSet, RoleViewSet

router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'permissions', PermissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
