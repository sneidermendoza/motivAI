from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User

class UserFlowTest(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = '/api/token/'
        self.profile_url = '/api/users/profile/me/'
        self.logout_url = reverse('logout')
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'Testpass123',
            'password2': 'Testpass123'
        }

    def test_register_login_profile_logout(self):
        # Registro
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        # Login
        login_data = {'username': 'testuser', 'password': 'Testpass123'}
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        access = response.data['access']
        refresh = response.data['refresh']
        # Perfil (usando JWT)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['username'], 'testuser')
        # Logout
        response = self.client.post(self.logout_url, {'refresh': refresh}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])

    def test_register_with_existing_email(self):
        User.objects.create_user(username='other', email='testuser@example.com', password='Testpass123')
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertIn('email', str(response.data['data']))

    def test_login_with_invalid_credentials(self):
        login_data = {'username': 'nouser', 'password': 'wrongpass'}
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 