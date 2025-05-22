from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from conversation.models import Conversation, ConversationState
from conversation.utils import transition_conversation_state

class ConversationFlowTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='convuser', email='convuser@example.com', password='Testpass123')
        login = self.client.post('/api/token/', {'username': 'convuser', 'password': 'Testpass123'}, format='json')
        self.access = login.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access)
        self.conversation_url = reverse('conversation-list')
        # Crear estados de conversación para testing
        self.initial_state = ConversationState.objects.create(name='initial', next_states=['motivation'], required_data=[], is_final=False)
        self.motivation_state = ConversationState.objects.create(name='motivation', next_states=['personal_info'], required_data=['motivation'], is_final=False)
        self.final_state = ConversationState.objects.create(name='final', next_states=[], required_data=[], is_final=True)

    def test_create_conversation(self):
        data = {}
        response = self.client.post(self.conversation_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])

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