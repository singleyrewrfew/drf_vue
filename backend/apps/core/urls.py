from django.urls import path
from . import views

urlpatterns = [
    path('', views.health_check, name='health-check'),
    path('live/', views.liveness_check, name='liveness-check'),
]
