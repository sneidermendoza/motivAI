from rest_framework import serializers
from .models import Conversation, Question, Response, ConversationState, ConversationFlow

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'type', 'options', 'validation_rules', 'order']
        read_only_fields = ['id']

class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ['id', 'conversation', 'question', 'raw_text', 'extracted_data', 
                 'is_valid', 'validation_message', 'created_at']
        read_only_fields = ['id', 'extracted_data', 'is_valid', 'validation_message', 'created_at']

class ConversationStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationState
        fields = ['id', 'name', 'description', 'next_states', 'required_data', 'is_final']
        read_only_fields = ['id']

class ConversationSerializer(serializers.ModelSerializer):
    responses = ResponseSerializer(many=True, read_only=True)
    current_state_info = serializers.SerializerMethodField()
    current_question = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'user', 'created_at', 'updated_at', 'is_active', 
                 'context', 'current_state', 'responses', 'current_state_info', 'current_question']
        read_only_fields = ['id', 'created_at', 'updated_at', 'responses', 'current_state_info', 'current_question']

    def get_current_state_info(self, obj):
        try:
            state = ConversationState.objects.get(name=obj.current_state)
            return ConversationStateSerializer(state).data
        except ConversationState.DoesNotExist:
            return None

    def get_current_question(self, obj):
        # Si la IA dejó un mensaje personalizado en el contexto, úsalo como pregunta conversacional
        context = obj.context or {}
        ia_message = None
        if 'ia_message' in context:
            ia_message = context['ia_message']
        elif 'collected_data' in context and 'ia_message' in context['collected_data']:
            ia_message = context['collected_data']['ia_message']
        if ia_message:
            return {'id': None, 'text': ia_message}
        # Mapeo de estado a orden de pregunta (fallback tradicional)
        state_to_order = {
            'initial': 1,
            'motivation': 1,
            'personal_info': 2,
            'goals': 6,
            'experience': 8,
            'medical': 10,
            'final': None
        }
        state_name = obj.current_state
        order = state_to_order.get(state_name)
        question = None
        if order:
            question = Question.objects.filter(order=order, is_active=True).first()
        # Fallback: si no hay pregunta para el estado, busca la de order=1 (motivación)
        if not question:
            question = Question.objects.filter(order=1, is_active=True).first()
        if question:
            return QuestionSerializer(question).data
        return None

class ConversationCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Conversation
        fields = ['id', 'user', 'context', 'current_state']
        read_only_fields = ['id', 'user']

class UserResponseSerializer(serializers.Serializer):
    """Serializer para procesar la respuesta del usuario."""
    conversation_id = serializers.IntegerField(
        help_text="ID de la conversación a la que pertenece la respuesta.", required=True
    )
    raw_text = serializers.CharField(
        help_text="Texto de la respuesta del usuario.", required=True
    )
    question_id = serializers.IntegerField(
        help_text="ID de la pregunta que se está respondiendo.", required=True
    )

    def validate(self, data):
        try:
            conversation = Conversation.objects.get(id=data['conversation_id'])
            if not conversation.is_active:
                raise serializers.ValidationError("Esta conversación ya no está activa.")
            data['conversation'] = conversation
            return data
        except Conversation.DoesNotExist:
            raise serializers.ValidationError("Conversación no encontrada.")

class FitnessExtractionInputSerializer(serializers.Serializer):
    message = serializers.CharField()

class FitnessExtractionOutputSerializer(serializers.Serializer):
    edad = serializers.IntegerField(required=False, allow_null=True)
    sexo = serializers.CharField(required=False, allow_null=True)
    peso = serializers.FloatField(required=False, allow_null=True)
    altura = serializers.FloatField(required=False, allow_null=True)
    objetivo = serializers.CharField(required=False, allow_null=True)
    motivacion = serializers.CharField(required=False, allow_null=True)
    nivel_actividad = serializers.CharField(required=False, allow_null=True)
    restricciones = serializers.CharField(required=False, allow_null=True)
    frecuencia_ejercicio = serializers.CharField(required=False, allow_null=True)
    nivel_experiencia = serializers.CharField(required=False, allow_null=True)
    dias_entrenar = serializers.IntegerField(required=False, allow_null=True)
    lugar_entrenamiento = serializers.CharField(required=False, allow_null=True)
    otros = serializers.DictField(required=False, allow_null=True)
    missing_fields = serializers.ListField(child=serializers.CharField(), required=False)
    error = serializers.CharField(required=False)

class ConversationFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationFlow
        fields = ['id', 'name', 'description', 'questions', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at'] 