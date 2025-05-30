from conversation.models import Conversation, Question, ConversationState
from conversation.serializers import ConversationSerializer
from users.models import User

# Cambia esto por el username de un usuario real de tu base
USERNAME = 'convuser'

user = User.objects.filter(username=USERNAME).first()
if not user:
    print(f'Usuario {USERNAME} no encontrado')
    exit(1)

# Crear una conversación
conv = Conversation.objects.create(user=user, current_state='motivation', context={})
serializer = ConversationSerializer(conv)
data = serializer.data
print('Conversación creada:')
print(data)

# Mostrar la pregunta actual
current_question = data.get('current_question')
print('\nPregunta actual:')
print(current_question)

# Simular una respuesta
if current_question:
    print('\nSimulando respuesta...')
    from conversation.models import Response as UserResponse
    resp = UserResponse.objects.create(
        conversation=conv,
        question_id=current_question['id'],
        raw_text='Mi motivación es mejorar mi salud.'
    )
    conv.context = {'collected_data': {'motivacion': 'Mi motivación es mejorar mi salud.'}}
    conv.save()
    # Serializar de nuevo para ver el siguiente estado/pregunta
    serializer2 = ConversationSerializer(conv)
    print('\nDespués de responder:')
    print(serializer2.data)
else:
    print('No hay pregunta actual para este estado.') 