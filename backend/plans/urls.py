from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.question import PreguntaPlanViewSet
from plans.views.plan import PlanEntrenamientoViewSet, UserFitnessProfileViewSet, RoutineViewSet, ExerciseViewSet

router = DefaultRouter()
router.register(r'preguntas', PreguntaPlanViewSet, basename='preguntaplan')
router.register(r'planentrenamiento', PlanEntrenamientoViewSet, basename='planentrenamiento')
router.register(r'fitnessprofile', UserFitnessProfileViewSet, basename='fitnessprofile')
router.register(r'rutinas', RoutineViewSet, basename='rutina')
router.register(r'ejercicios', ExerciseViewSet, basename='ejercicio')

urlpatterns = [
    path('', include(router.urls)),
] 