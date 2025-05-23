from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProgresoViewSet

router = DefaultRouter()
router.register(r'progreso', ProgresoViewSet, basename='progreso')

urlpatterns = [
    path('', include(router.urls)),
] 