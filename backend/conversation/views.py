from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from .models import Conversation, Question, Response as UserResponse, ConversationState, ConversationFlow
from .serializers import (
    ConversationSerializer,
    ConversationCreateSerializer,
    QuestionSerializer,
    ResponseSerializer,
    ConversationStateSerializer,
    UserResponseSerializer,
    FitnessExtractionInputSerializer,
    FitnessExtractionOutputSerializer,
    ConversationFlowSerializer
)
from plans.models.plan import UserFitnessProfile, PlanEntrenamiento
from .utils import extract_and_update_fitness_profile, transition_conversation_state, validar_respuesta_usuario
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from backend.utils import ResponseStandard, StandardResponseMixin
from .ai import extract_fitness_data_with_groq
from rest_framework.views import APIView

class ConversationViewSet(StandardResponseMixin, viewsets.ModelViewSet):
    """
    API endpoint para gestionar conversaciones
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationCreateSerializer
    permission_classes = [IsAuthenticated]
    swagger_tags = ['Conversación']

    @swagger_auto_schema(
        operation_description="Lista las conversaciones del usuario",
        responses={200: ConversationSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Crea una nueva conversación",
        request_body=ConversationCreateSerializer,
        responses={201: ConversationSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_description="Reinicia una conversación existente",
        responses={200: ConversationSerializer()}
    )
    @action(detail=True, methods=['post'])
    def reset(self, request, pk=None):
        conversation = self.get_object()
        conversation.reset()
        return ResponseStandard.success(
            data=ConversationSerializer(conversation).data,
            message="Conversación reiniciada correctamente."
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
        question_id = serializer.validated_data.get('question_id')
        raw_text = serializer.validated_data['raw_text']
        question = None
        if question_id:
            from .models import Question
            question = Question.objects.filter(id=question_id).first()
        # Validar respuesta
        is_valid, mensaje_validacion, is_fallback = validar_respuesta_usuario(question, raw_text)
        if not is_valid:
            return ResponseStandard.error(
                message=mensaje_validacion or "Respuesta no válida.",
                data={"fallback": is_fallback},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Crear la respuesta
        response = UserResponse.objects.create(
            conversation=conversation,
            raw_text=raw_text,
            question_id=question_id
        )
        # Procesar la respuesta y actualizar el perfil fitness
        plan = PlanEntrenamiento.objects.filter(usuario=request.user, status='activo').order_by('-fecha_inicio').first()
        if plan:
            extract_and_update_fitness_profile(request.user, plan, response)
        response.extracted_data = {'raw_text': response.raw_text}
        response.save()
        conversation.save()
        # Llamar al helper de transición de estado
        transition_conversation_state(conversation, conversation.current_state, conversation.context)
        return ResponseStandard.success(
            data=ConversationSerializer(conversation).data,
            message="Respuesta registrada y perfil actualizado.",
            status=status.HTTP_200_OK
        )

class QuestionViewSet(StandardResponseMixin, viewsets.ModelViewSet):
    """
    API endpoint para gestionar preguntas
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    swagger_tags = ['Conversación']

class ConversationStateViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ConversationState.objects.all()
    serializer_class = ConversationStateSerializer

class FitnessExtractionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FitnessExtractionInputSerializer(data=request.data)
        if not serializer.is_valid():
            return ResponseStandard.error(message="Datos inválidos", data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        message = serializer.validated_data['message']
        result = extract_fitness_data_with_groq(message)
        output_serializer = FitnessExtractionOutputSerializer(data=result)
        if output_serializer.is_valid():
            # Si hay error o campos faltantes, responder con error
            if result.get('error'):
                return ResponseStandard.error(message="Error al extraer datos con IA", data=result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            if result.get('missing_fields'):
                return ResponseStandard.error(message="Faltan campos", data=result, status=status.HTTP_400_BAD_REQUEST)
            return ResponseStandard.success(data=result, message="Datos extraídos correctamente", status=status.HTTP_200_OK)
        else:
            return ResponseStandard.error(message="Respuesta inválida de la IA", data=output_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ConversationFlowViewSet(StandardResponseMixin, viewsets.ModelViewSet):
    """
    API endpoint para gestionar flujos de conversación.
    Solo accesible para administradores.
    """
    serializer_class = ConversationFlowSerializer
    queryset = ConversationFlow.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    swagger_tags = ['Conversación']

    @swagger_auto_schema(
        operation_description="Lista todos los flujos de conversación (solo admin)",
        responses={200: ConversationFlowSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Crea un nuevo flujo de conversación (solo admin)",
        request_body=ConversationFlowSerializer,
        responses={201: ConversationFlowSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Actualiza un flujo de conversación existente (solo admin)",
        request_body=ConversationFlowSerializer,
        responses={200: ConversationFlowSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Elimina un flujo de conversación (solo admin)",
        responses={204: "No Content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs) 