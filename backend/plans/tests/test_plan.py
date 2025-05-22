from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from plans.models.plan import PlanEntrenamiento, UserFitnessProfile

class PlanFlowTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='planuser', email='planuser@example.com', password='Testpass123')
        login = self.client.post('/api/token/', {'username': 'planuser', 'password': 'Testpass123'}, format='json')
        self.access = login.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access)
        self.plan_url = reverse('planentrenamiento-list')
        self.fitness_url = reverse('fitnessprofile-list')

    def test_create_plan_and_fitness_profile(self):
        # Crear plan (asegúrate de incluir todos los campos requeridos)
        data = {'objetivo': 'Bajar de peso', 'fecha_inicio': '2024-06-01'}
        response = self.client.post(self.plan_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        plan_id = response.data['data']['plan']['id']
        # Consultar perfil fitness (debe estar vacío inicialmente)
        response = self.client.get(self.fitness_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])

    def test_create_plan_missing_fields(self):
        # Falta objetivo
        data = {'fecha_inicio': '2024-06-01'}
        response = self.client.post(self.plan_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success']) 