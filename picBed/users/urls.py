from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthViewSet, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('', AuthViewSet.as_view({
        'post': 'register'
    }), name='register'),
    path('login/', AuthViewSet.as_view({
        'post': 'login'
    }), name='login'),
    path('refresh/', AuthViewSet.as_view({
        'post': 'refresh'
    }), name='token-refresh'),
]
