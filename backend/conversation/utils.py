from plans.models.plan import UserFitnessProfile
from conversation.models import ConversationState

def extract_and_update_fitness_profile(usuario, plan, response):
    """
    Extrae información relevante de la respuesta y actualiza o crea el UserFitnessProfile asociado.
    """
    # Determinar el campo a actualizar según la pregunta
    question = response.question
    text = response.raw_text.strip()
    if not question or not text:
        return

    # Buscar o crear el perfil fitness para este usuario y plan
    profile, created = UserFitnessProfile.objects.get_or_create(usuario=usuario, plan=plan)

    # Lógica simple basada en el texto de la pregunta
    q_text = question.text.lower() if question else ''
    if 'motivación' in q_text or 'motiva' in q_text:
        profile.motivacion = text
    elif 'objetivo' in q_text:
        profile.objetivo = text
    elif 'edad' in q_text:
        try:
            profile.edad = int(text)
        except ValueError:
            pass
    elif 'sexo' in q_text:
        profile.sexo = text.lower()
    elif 'peso' in q_text:
        try:
            profile.peso = float(text.replace(',', '.'))
        except ValueError:
            pass
    elif 'altura' in q_text:
        try:
            profile.altura = float(text.replace(',', '.'))
        except ValueError:
            pass
    elif 'actividad' in q_text:
        profile.nivel_actividad = text
    elif 'restriccion' in q_text or 'restricción' in q_text:
        profile.restricciones = text
    else:
        # Guardar en 'otros' si no es un campo conocido
        otros = profile.otros or {}
        otros[q_text] = text
        profile.otros = otros

    profile.save()

def transition_conversation_state(conversation, current_state, context):
    """
    Determina el siguiente estado de la conversación basado en el estado actual y el contexto.
    Si el estado actual es final, marca la conversación como inactiva.
    """
    try:
        state = ConversationState.objects.get(name=current_state)
    except ConversationState.DoesNotExist:
        return

    # Si el estado es final, marcar la conversación como inactiva
    if state.is_final:
        conversation.is_active = False
        conversation.save()
        return

    # Verificar si se han recolectado los datos requeridos
    required_data = state.required_data
    collected_data = context.get('collected_data', {})
    missing_data = [field for field in required_data if field not in collected_data]

    # Si faltan datos, se puede decidir si avanzar o quedarse en el mismo estado
    # En este caso, avanzamos si hay al menos un dato recolectado
    if missing_data and len(collected_data) > 0:
        # Avanzar al siguiente estado si hay datos recolectados
        next_states = state.next_states
        if next_states:
            next_state = next_states[0]  # Tomar el primer estado siguiente
            conversation.current_state = next_state
            conversation.save()
    elif not missing_data:
        # Si no faltan datos, avanzar al siguiente estado
        next_states = state.next_states
        if next_states:
            next_state = next_states[0]  # Tomar el primer estado siguiente
            conversation.current_state = next_state
            conversation.save()

def validar_respuesta_usuario(question, raw_text):
    """
    Valida la respuesta del usuario según las reglas de la pregunta.
    Devuelve (is_valid, mensaje_validacion, fallback).
    """
    if not question or not raw_text or not raw_text.strip():
        return False, "La respuesta está vacía o no se entiende. Por favor, intenta ser más específico.", True
    # Validación por tipo
    if question.type == 'numeric':
        try:
            valor = float(raw_text.replace(',', '.'))
            reglas = question.validation_rules or {}
            if 'min' in reglas and valor < reglas['min']:
                return False, f"El valor debe ser mayor o igual a {reglas['min']}.", False
            if 'max' in reglas and valor > reglas['max']:
                return False, f"El valor debe ser menor o igual a {reglas['max']}.", False
        except Exception:
            return False, "Por favor, ingresa un número válido.", False
    elif question.type == 'multiple_choice':
        opciones = [o.lower() for o in (question.options or [])]
        if raw_text.lower() not in opciones:
            return False, f"Por favor, elige una de las opciones válidas: {', '.join(question.options)}.", False
    # Si pasa todas las validaciones
    return True, None, False 