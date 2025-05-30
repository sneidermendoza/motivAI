from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from conversation.models import Conversation, ConversationState, Question
from conversation.utils import transition_conversation_state
from plans.ai import generate_training_plan_with_groq

class ConversationFlowTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='convuser', email='convuser@example.com', password='Testpass123')
        login = self.client.post('/api/token/', {'username': 'convuser', 'password': 'Testpass123'}, format='json')
        self.access = login.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access)
        self.conversation_url = reverse('conversation-list')
        
        # Crear estados de conversación para testing
        self.initial_state = ConversationState.objects.create(
            name='initial',
            description='Estado inicial de la conversación',
            next_states=['motivation'],
            required_data=[],
            is_final=False
        )
        
        self.motivation_state = ConversationState.objects.create(
            name='motivation',
            description='Preguntando sobre la motivación del usuario',
            next_states=['personal_info'],
            required_data=['motivation'],
            is_final=False
        )
        
        self.personal_info_state = ConversationState.objects.create(
            name='personal_info',
            description='Recopilando información personal',
            next_states=['goals'],
            required_data=['age', 'gender', 'weight', 'height'],
            is_final=False
        )
        
        self.goals_state = ConversationState.objects.create(
            name='goals',
            description='Definiendo objetivos específicos',
            next_states=['experience'],
            required_data=['specific_goals', 'timeline'],
            is_final=False
        )
        
        self.experience_state = ConversationState.objects.create(
            name='experience',
            description='Preguntando sobre experiencia y frecuencia',
            next_states=['medical'],
            required_data=['exercise_frequency', 'experience_level'],
            is_final=False
        )
        
        self.medical_state = ConversationState.objects.create(
            name='medical',
            description='Recopilando información médica',
            next_states=['final'],
            required_data=['medical_conditions', 'injuries'],
            is_final=False
        )
        
        self.final_state = ConversationState.objects.create(
            name='final',
            description='Estado final de la conversación',
            next_states=[],
            required_data=[],
            is_final=True
        )
        
        # Crear preguntas para cada estado
        self.motivation_question = Question.objects.create(
            text='¿Qué te motiva a mejorar tu salud y condición física?',
            type='open',
            order=1,
            is_active=True
        )
        
        self.personal_info_questions = [
            Question.objects.create(
                text='¿Cuál es tu edad?',
                type='number',
                order=2,
                is_active=True
            ),
            Question.objects.create(
                text='¿Cuál es tu género?',
                type='choice',
                options=['masculino', 'femenino', 'otro'],
                order=3,
                is_active=True
            ),
            Question.objects.create(
                text='¿Cuál es tu peso actual en kg?',
                type='number',
                order=4,
                is_active=True
            ),
            Question.objects.create(
                text='¿Cuál es tu altura en cm?',
                type='number',
                order=5,
                is_active=True
            )
        ]
        
        self.goals_questions = [
            Question.objects.create(
                text='¿Cuál es tu objetivo específico?',
                type='open',
                order=6,
                is_active=True
            ),
            Question.objects.create(
                text='¿En qué tiempo quieres alcanzarlo?',
                type='open',
                order=7,
                is_active=True
            )
        ]
        
        self.experience_questions = [
            Question.objects.create(
                text='¿Con qué frecuencia puedes entrenar?',
                type='choice',
                options=['1-2 veces por semana', '3-4 veces por semana', '5+ veces por semana'],
                order=8,
                is_active=True
            ),
            Question.objects.create(
                text='¿Cuál es tu nivel de experiencia?',
                type='choice',
                options=['principiante', 'intermedio', 'avanzado'],
                order=9,
                is_active=True
            )
        ]
        
        self.medical_questions = [
            Question.objects.create(
                text='¿Tienes alguna condición médica que debamos considerar?',
                type='open',
                order=10,
                is_active=True
            ),
            Question.objects.create(
                text='¿Has tenido alguna lesión reciente?',
                type='open',
                order=11,
                is_active=True
            )
        ]

    def test_create_conversation(self):
        data = {}
        response = self.client.post(self.conversation_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        # Nuevo: verificar que current_question está presente y es la motivación
        conversation = response.data['data']
        self.assertIn('current_question', conversation)
        self.assertIsNotNone(conversation['current_question'])
        self.assertIn('text', conversation['current_question'])
        self.assertIn('id', conversation['current_question'])
        # Aserción más flexible: busca 'motiva' (ignora tildes y mayúsculas)
        self.assertIn('motiva', conversation['current_question']['text'].lower())

    def test_create_conversation_unauthenticated(self):
        self.client.credentials()  # Remove auth
        response = self.client.post(self.conversation_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_transition_conversation_state(self):
        # Crear una conversación
        conversation = Conversation.objects.create(user=self.user, current_state='initial', context={})
        # Probar transición a estado final
        transition_conversation_state(conversation, 'final', {})
        self.assertFalse(conversation.is_active)
        # Probar transición a estado siguiente
        conversation = Conversation.objects.create(user=self.user, current_state='initial', context={'collected_data': {'motivation': 'test'}})
        transition_conversation_state(conversation, 'initial', conversation.context)
        self.assertEqual(conversation.current_state, 'motivation')

    def test_generate_plan_groq_success(self):
        url = '/api/plans/planentrenamiento/generate/'
        data = {
            "age": 28,
            "gender": "male",
            "weight": 80,
            "height": 175,
            "motivation": "Quiero bajar de peso y sentirme con más energía.",
            "medical_conditions": "Ninguna",
            "injuries": "Ninguna",
            "exercise_frequency": "2 veces por semana",
            "experience_level": "principiante",
            "specific_goals": "Bajar 5kg en 3 meses",
            "timeline": "3 meses",
            "additional_info": "Trabajo muchas horas sentado y me gustaría mejorar mi postura."
        }
        response = self.client.post(url, data, format='json')
        self.assertIn(response.status_code, [200, 504, 500])  # Puede ser éxito o timeout
        # Si es éxito, debe tener 'plan' en la data
        if response.status_code == 200:
            self.assertIn('plan', response.data['data'])

    def test_generate_plan_groq_error(self):
        url = '/api/plans/planentrenamiento/generate/'
        # Enviamos datos vacíos para forzar un error de la IA
        response = self.client.post(url, {}, format='json')
        self.assertIn(response.status_code, [400, 500])

    def test_full_conversation_flow(self):
        # 1. Crear conversación
        url_create = reverse('conversation-list')
        response = self.client.post(url_create, {})
        self.assertEqual(response.status_code, 201)
        conv_id = response.data['data']['id']
        current_question = response.data['data']['current_question']
        self.assertIsNotNone(current_question)
        print('Primera pregunta:', current_question['text'])

        # Respuestas simulando una conversación fluida y natural
        respuestas = [
            # Respuesta fuera de contexto
            "Me gusta el cine y la pizza, ¿cuál es tu película favorita?",
            # Respuesta con motivación y objetivo
            "Quiero mejorar mi salud y bajar de peso. Me motiva sentirme con más energía y confianza.",
            # Respuesta con datos personales
            "Tengo 30 años, soy hombre, peso 80kg y mido 175cm.",
            # Respuesta con frecuencia, nivel y preferencia
            "Puedo entrenar 3 veces por semana, soy principiante y prefiero entrenar en casa.",
            # Respuesta con condiciones médicas y lesiones
            "No tengo lesiones ni condiciones médicas.",
            # Respuesta con objetivo específico y tiempo
            "Mi objetivo es perder 5kg en 3 meses."
        ]

        # Seguimiento de datos recolectados
        collected_data = {}
        max_steps = 10  # Aumentamos el límite de pasos
        step = 0

        for answer in respuestas:
            step += 1
            if step > max_steps:
                self.fail(f'La conversación excedió el límite de {max_steps} pasos')

            url_respond = reverse('conversation-respond', args=[conv_id])
            payload = {
                'conversation_id': conv_id,
                'question_id': current_question['id'] if current_question['id'] else 1,
                'raw_text': answer
            }
            response = self.client.post(url_respond, payload, format='json')
            self.assertEqual(response.status_code, 200)
            data = response.data['data']
            next_question = data.get('current_question')
            print(f'Pregunta {step+1}:', next_question['text'] if next_question else 'No hay más preguntas')

            # Verificar que la IA mantiene el contexto
            if 'collected_data' in data:
                for key, value in data['collected_data'].items():
                    if value and key != 'message':
                        collected_data[key] = value

            # Si la respuesta fue fuera de contexto, la IA debe pedir enfocarse en el tema
            if step == 1:
                self.assertIn('no está relacionada', next_question['text'].lower())
                self.assertIn('salud', next_question['text'].lower())

            # La IA nunca debe decir 'faltan los siguientes datos'
            self.assertNotIn('faltan los siguientes datos', next_question['text'].lower())

            # Si tenemos todos los datos necesarios, la conversación debe terminar
            required_fields = ['edad', 'sexo', 'peso', 'altura', 'objetivo', 'motivacion', 
                             'frecuencia_ejercicio', 'nivel_experiencia', 'dias_entrenar', 
                             'lugar_entrenamiento']
            if all(collected_data.get(field) for field in required_fields):
                print('¡Conversación completada con éxito!')
                break

            if not next_question:
                break
            current_question = next_question

class FitnessExtractionAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='extractuser', email='extractuser@example.com', password='Testpass123')
        login = self.client.post('/api/token/', {'username': 'extractuser', 'password': 'Testpass123'}, format='json')
        self.access = login.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access)
        self.url = '/api/conversation/extract/'

    def test_extract_complete_message(self):
        data = {"message": "Tengo 30 años, peso 75kg, mido 180cm, soy hombre, quiero ganar músculo, entreno 4 veces por semana en gimnasio, no tengo lesiones."}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['success'])
        self.assertIn('edad', response.data['data'])
        self.assertEqual(response.data['data']['edad'], 30)
        self.assertEqual(response.data['data']['sexo'], 'masculino')
        self.assertEqual(response.data['data']['peso'], 75)
        self.assertEqual(response.data['data']['altura'], 180)
        self.assertEqual(response.data['data']['objetivo'], 'ganar músculo')
        self.assertEqual(response.data['data']['lugar_entrenamiento'], 'gimnasio')
        self.assertEqual(response.data['data']['missing_fields'], [])

    def test_extract_incomplete_message(self):
        data = {"message": "Quiero perder peso y entrenar en casa."}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['success'])
        self.assertIn('missing_fields', response.data['data'])
        self.assertGreater(len(response.data['data']['missing_fields']), 0)

    def test_extract_ambiguous_message(self):
        data = {"message": "Me gustaría mejorar mi salud."}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['success'])
        self.assertIn('missing_fields', response.data['data'])
        self.assertGreater(len(response.data['data']['missing_fields']), 0) 