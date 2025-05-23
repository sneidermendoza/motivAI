"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView

schema_view = get_schema_view(
   openapi.Info(
      title="motivAI API",
      default_version='v1',
      description="""
      # Documentación de la API motivAI
      
      ## Secciones
      - **Autenticación**: Registro, login y gestión de usuarios
      - **Planes**: Creación y gestión de planes de entrenamiento
      - **Ejercicios**: Gestión de ejercicios y rutinas diarias
      - **Conversación**: Sistema conversacional y extracción de información
      - **Progreso**: Seguimiento del progreso y métricas
      - **Notificaciones**: Sistema de notificaciones y alertas
      - **Feedback**: Sistema de feedback y sugerencias
      
      ## Notas
      - Todos los endpoints requieren autenticación excepto los marcados como públicos
      - Los tokens JWT deben incluirse en el header como `Authorization: Bearer <token>`
      """,
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="tu-email@ejemplo.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/users/', include('users.urls')),
    path('api/plans/', include('plans.urls')),
    path('api/progress/', include('progress.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/feedback/', include('feedback.urls')),
    path('api/conversation/', include('conversation.urls')),
    # Swagger/OpenAPI
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui-root'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # Social Auth URLs
    path('auth/', include('social_django.urls', namespace='social')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)