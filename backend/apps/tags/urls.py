from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TagViewSet

# 创建默认路由器
router = DefaultRouter()

# 注册标签视图集到路由器
router.register(r'', TagViewSet)

# URL 模式配置
urlpatterns = [
    path('', include(router.urls)),
]
