from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.user import UserViewSet, RegisterView
from .views.role import PermissionViewSet, RoleViewSet

router = DefaultRouter()
router.register(r'', UserViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'roles', RoleViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', include(router.urls)),
] 