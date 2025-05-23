from rest_framework import serializers
from .models import Conversation, Question, Response, ConversationState

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

    class Meta:
        model = Conversation
        fields = ['id', 'user', 'created_at', 'updated_at', 'is_active', 
                 'context', 'current_state', 'responses', 'current_state_info']
        read_only_fields = ['id', 'created_at', 'updated_at', 'responses', 'current_state_info']

    def get_current_state_info(self, obj):
        try:
            state = ConversationState.objects.get(name=obj.current_state)
            return ConversationStateSerializer(state).data
        except ConversationState.DoesNotExist:
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