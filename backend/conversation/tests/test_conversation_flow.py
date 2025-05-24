from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from conversation.models import ConversationFlow, Question

class ConversationFlowAPITestCase(APITestCase):
    def setUp(self):
        ConversationFlow.objects.all().delete()  # Limpia todos los flujos antes de cada test
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='Testpass123')
        self.admin = User.objects.create_superuser(username='admin', email='admin@example.com', password='Adminpass123')
        self.question = Question.objects.create(
            text="¿Cuál es tu objetivo principal?",
            type="open"
        )
        self.flow = ConversationFlow.objects.create(
            name="Flujo Principal",
            description="Flujo principal de conversación"
        )
        self.flow.questions.add(self.question)
        self.url = reverse('flow-list')

    def test_create_flow_admin(self):
        self.client.login(username='admin', password='Adminpass123')
        data = {
            'name': 'Nuevo Flujo',
            'description': 'Descripción del nuevo flujo',
            'questions': [self.question.id],
            'is_active': True
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ConversationFlow.objects.count(), 2)

    def test_create_flow_non_admin(self):
        self.client.login(username='testuser', password='Testpass123')
        data = {
            'name': 'Nuevo Flujo',
            'description': 'Descripción del nuevo flujo',
            'questions': [self.question.id],
            'is_active': True
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_flows_admin(self):
        self.client.login(username='admin', password='Adminpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)

    def test_list_flows_non_admin(self):
        self.client.login(username='testuser', password='Testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_flow_admin(self):
        self.client.login(username='admin', password='Adminpass123')
        url = reverse('flow-detail', args=[self.flow.id])
        data = {
            'name': 'Flujo Actualizado',
            'description': 'Nueva descripción',
            'questions': [self.question.id],
            'is_active': True
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.flow.refresh_from_db()
        self.assertEqual(self.flow.name, 'Flujo Actualizado')

    def test_delete_flow_admin(self):
        self.client.login(username='admin', password='Adminpass123')
        url = reverse('flow-detail', args=[self.flow.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ConversationFlow.objects.count(), 0) 