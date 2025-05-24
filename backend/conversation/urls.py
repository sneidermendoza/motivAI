from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'conversations', views.ConversationViewSet, basename='conversation')
router.register(r'questions', views.QuestionViewSet, basename='question')
router.register(r'states', views.ConversationStateViewSet, basename='state')
router.register(r'flows', views.ConversationFlowViewSet, basename='flow')

urlpatterns = [
    path('', include(router.urls)),
    path('extract/', views.FitnessExtractionView.as_view(), name='fitness-extract'),
] 