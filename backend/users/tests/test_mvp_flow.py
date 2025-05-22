from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class MVPFlowTest(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = '/api/token/'
        self.plan_url = reverse('planentrenamiento-list')
        self.conversation_url = reverse('conversation-list')
        self.profile_url = '/api/users/profile/me/'
        self.fitness_url = reverse('fitnessprofile-list')
        self.logout_url = reverse('logout')
        self.user_data = {
            'username': 'mvpuser',
            'email': 'mvpuser@example.com',
            'password': 'Testpass123',
            'password2': 'Testpass123'
        }

    def test_full_mvp_flow(self):
        # Registro
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Login
        login_data = {'username': 'mvpuser', 'password': 'Testpass123'}
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access = response.data['access']
        refresh = response.data['refresh']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        # Crear plan
        plan_data = {'objetivo': 'MVP objetivo', 'fecha_inicio': '2024-06-01'}
        response = self.client.post(self.plan_url, plan_data, format='json')
        if response.status_code != status.HTTP_201_CREATED:
            print('Plan creation error:', response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Crear conversación
        response = self.client.post(self.conversation_url, {}, format='json')
        if response.status_code != status.HTTP_201_CREATED:
            print('Conversation creation error:', response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Consultar perfil
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Consultar perfil fitness
        response = self.client.get(self.fitness_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Logout
        response = self.client.post(self.logout_url, {'refresh': refresh}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_without_token(self):
        # Intentar acceder a perfil sin token
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 