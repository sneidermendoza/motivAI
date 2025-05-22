from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Conversation, Question, Response as UserResponse, ConversationState
from .serializers import (
    ConversationSerializer,
    ConversationCreateSerializer,
    QuestionSerializer,
    ResponseSerializer,
    ConversationStateSerializer,
    UserResponseSerializer
)
from plans.models.plan import UserFitnessProfile, PlanEntrenamiento
from .utils import extract_and_update_fitness_profile
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from backend.utils import ResponseStandard

class ConversationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationSerializer

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = ConversationCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return ResponseStandard.error(message="Datos inválidos", data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        conversation = serializer.save(user=request.user)
        return ResponseStandard.success(
            data=ConversationSerializer(conversation).data,
            message="Conversación creada correctamente.",
            status=status.HTTP_201_CREATED
        )

    @swagger_auto_schema(
        method='post',
        request_body=UserResponseSerializer,
        responses={200: ConversationSerializer},
        operation_description="Responde una pregunta en la conversación. Campos requeridos: conversation_id (int), question_id (int), raw_text (str)."
    )
    @action(detail=True, methods=['post'])
    def respond(self, request, pk=None):
        conversation = self.get_object()
        serializer = UserResponseSerializer(data=request.data)
        if not serializer.is_valid():
            return ResponseStandard.error(message="Datos inválidos", data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # Crear la respuesta
        response = UserResponse.objects.create(
            conversation=conversation,
            raw_text=serializer.validated_data['raw_text'],
            question_id=serializer.validated_data.get('question_id')
        )
        # Procesar la respuesta y actualizar el perfil fitness
        plan = PlanEntrenamiento.objects.filter(usuario=request.user, status='activo').order_by('-fecha_inicio').first()
        if plan:
            extract_and_update_fitness_profile(request.user, plan, response)
        response.extracted_data = {'raw_text': response.raw_text}
        response.save()
        conversation.save()
        return ResponseStandard.success(
            data=ConversationSerializer(conversation).data,
            message="Respuesta registrada y perfil actualizado.",
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def reset(self, request, pk=None):
        conversation = self.get_object()
        conversation.current_state = 'initial'
        conversation.context = {}
        conversation.save()
        return ResponseStandard.success(
            data=ConversationSerializer(conversation).data,
            message="Conversación reiniciada.",
            status=status.HTTP_200_OK
        )

class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Question.objects.filter(is_active=True)
    serializer_class = QuestionSerializer

class ConversationStateViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ConversationState.objects.all()
    serializer_class = ConversationStateSerializer 