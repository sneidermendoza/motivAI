from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.notification import NotificacionViewSet

router = DefaultRouter()
router.register(r'motivational', NotificacionViewSet, basename='motivational')

urlpatterns = [
    path('', include(router.urls)),
] 