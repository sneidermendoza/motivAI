from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.question import PreguntaPlanViewSet

router = DefaultRouter()
router.register(r'preguntas', PreguntaPlanViewSet, basename='preguntaplan')

urlpatterns = [
    path('', include(router.urls)),
] 