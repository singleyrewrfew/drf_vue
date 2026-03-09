from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('api/contents/', include('apps.contents.urls')),
    path('api/categories/', include('apps.categories.urls')),
    path('api/tags/', include('apps.tags.urls')),
    path('api/media/', include('apps.media.urls')),
    path('api/comments/', include('apps.comments.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
