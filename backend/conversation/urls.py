from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'conversations', views.ConversationViewSet, basename='conversation')
router.register(r'questions', views.QuestionViewSet, basename='question')
router.register(r'states', views.ConversationStateViewSet, basename='state')

urlpatterns = [
    path('', include(router.urls)),
] 