from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.user import UserViewSet, RegisterView, LogoutView
from .views.role import PermissionViewSet, RoleViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

router = DefaultRouter()
router.register(r'profile', UserViewSet, basename='users')
router.register(r'permissions', PermissionViewSet)
router.register(r'roles', RoleViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('', include(router.urls)),
] 