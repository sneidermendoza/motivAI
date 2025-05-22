from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Conversation, Question, Response, ConversationState
from .serializers import (
    ConversationSerializer,
    ConversationCreateSerializer,
    QuestionSerializer,
    ResponseSerializer,
    ConversationStateSerializer,
    UserResponseSerializer
)

class ConversationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationSerializer

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = ConversationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save(user=request.user)
        return Response(
            ConversationSerializer(conversation).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'])
    def respond(self, request, pk=None):
        conversation = self.get_object()
        serializer = UserResponseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Crear la respuesta
        response = Response.objects.create(
            conversation=conversation,
            raw_text=serializer.validated_data['raw_text'],
            question_id=serializer.validated_data.get('question_id')
        )

        # TODO: Procesar la respuesta con IA
        # Por ahora, solo guardamos la respuesta sin procesar
        response.extracted_data = {'raw_text': response.raw_text}
        response.save()

        # Actualizar el estado de la conversación
        # TODO: Implementar lógica de transición de estados
        conversation.save()

        return Response(
            ConversationSerializer(conversation).data,
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def reset(self, request, pk=None):
        conversation = self.get_object()
        conversation.current_state = 'initial'
        conversation.context = {}
        conversation.save()
        return Response(
            ConversationSerializer(conversation).data,
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