from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Conversation(models.Model):
    """Modelo para mantener el estado de una conversación con un usuario."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='conversations'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    context = models.JSONField(default=dict, help_text=_("Contexto actual de la conversación"))
    current_state = models.CharField(
        max_length=50,
        default='initial',
        help_text=_("Estado actual de la conversación")
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Conversación de {self.user.email} - {self.created_at}"

class Question(models.Model):
    """Modelo para las preguntas que puede hacer la IA."""
    class QuestionType(models.TextChoices):
        OPEN = 'open', _('Abierta')
        MULTIPLE_CHOICE = 'multiple_choice', _('Opción Múltiple')
        NUMERIC = 'numeric', _('Numérica')

    text = models.TextField(help_text=_("Texto de la pregunta"))
    type = models.CharField(
        max_length=20,
        choices=QuestionType.choices,
        default=QuestionType.OPEN
    )
    options = models.JSONField(
        null=True,
        blank=True,
        help_text=_("Opciones para preguntas de opción múltiple")
    )
    validation_rules = models.JSONField(
        null=True,
        blank=True,
        help_text=_("Reglas de validación para la respuesta")
    )
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.text[:50]}..."

class Response(models.Model):
    """Modelo para las respuestas del usuario."""
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='responses'
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.SET_NULL,
        null=True,
        related_name='responses'
    )
    raw_text = models.TextField(help_text=_("Respuesta original del usuario"))
    extracted_data = models.JSONField(
        default=dict,
        help_text=_("Datos extraídos de la respuesta")
    )
    is_valid = models.BooleanField(default=True)
    validation_message = models.TextField(
        null=True,
        blank=True,
        help_text=_("Mensaje de validación si la respuesta no es válida")
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Respuesta de {self.conversation.user.email} - {self.created_at}"

class ConversationState(models.Model):
    """Modelo para mantener el estado de la conversación y sus transiciones."""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    next_states = models.JSONField(
        default=list,
        help_text=_("Lista de estados posibles después de este")
    )
    required_data = models.JSONField(
        default=list,
        help_text=_("Datos requeridos para este estado")
    )
    is_final = models.BooleanField(
        default=False,
        help_text=_("Indica si este es un estado final de la conversación")
    )

    def __str__(self):
        return self.name 