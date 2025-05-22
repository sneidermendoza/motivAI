from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from conversation.models import Conversation

class ConversationFlowTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='convuser', email='convuser@example.com', password='Testpass123')
        login = self.client.post('/api/token/', {'username': 'convuser', 'password': 'Testpass123'}, format='json')
        self.access = login.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access)
        self.conversation_url = reverse('conversation-list')

    def test_create_conversation(self):
        data = {}
        response = self.client.post(self.conversation_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])

    def test_create_conversation_unauthenticated(self):
        self.client.credentials()  # Remove auth
        response = self.client.post(self.conversation_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 