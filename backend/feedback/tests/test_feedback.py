from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models.user import User
from ..models.feedback import Feedback

class FeedbackAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='Testpass123')
        self.admin = User.objects.create_superuser(username='admin', email='admin@example.com', password='Adminpass123')
        self.feedback_url = reverse('feedback-list')

    def test_create_feedback_anonymous(self):
        data = {'tipo': 'sugerencia', 'mensaje': 'Me gusta la app!'}
        response = self.client.post(self.feedback_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(Feedback.objects.first().usuario)

    def test_create_feedback_authenticated(self):
        self.client.login(username='testuser', password='Testpass123')
        data = {'tipo': 'reporte', 'mensaje': 'Encontré un bug.'}
        response = self.client.post(self.feedback_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Feedback.objects.first().usuario, self.user)

    def test_list_feedback_admin(self):
        Feedback.objects.create(mensaje='Test', tipo='feedback')
        self.client.login(username='admin', password='Adminpass123')
        response = self.client.get(self.feedback_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_list_feedback_user_forbidden(self):
        Feedback.objects.create(mensaje='Test', tipo='feedback')
        self.client.login(username='testuser', password='Testpass123')
        response = self.client.get(self.feedback_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) 