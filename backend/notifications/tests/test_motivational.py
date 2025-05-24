from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models.user import User
from ..models.notification import Notificacion
from datetime import time

class MotivationalNotificationAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='Testpass123')
        self.admin = User.objects.create_superuser(username='admin', email='admin@example.com', password='Adminpass123')
        self.noti_url = reverse('motivational-list')
        self.gen_url = reverse('motivational-generar-motivacional')

    def test_create_notification_authenticated(self):
        self.client.login(username='testuser', password='Testpass123')
        data = {'tipo': 'motivacional', 'mensaje': '¡Vamos, tú puedes!', 'hora_preferida': '08:00:00'}
        response = self.client.post(self.noti_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Notificacion.objects.first().usuario, self.user)

    def test_list_notification_user(self):
        Notificacion.objects.create(usuario=self.user, tipo='motivacional', mensaje='¡Hola!', hora_preferida=time(8,0))
        self.client.login(username='testuser', password='Testpass123')
        response = self.client.get(self.noti_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_notification_admin(self):
        Notificacion.objects.create(usuario=self.user, tipo='motivacional', mensaje='¡Hola!', hora_preferida=time(8,0))
        self.client.login(username='admin', password='Adminpass123')
        response = self.client.get(self.noti_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_mark_as_read(self):
        noti = Notificacion.objects.create(usuario=self.user, tipo='motivacional', mensaje='¡Hola!', hora_preferida=time(8,0))
        self.client.login(username='testuser', password='Testpass123')
        url = reverse('motivational-marcar-leido', args=[noti.id])
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        noti.refresh_from_db()
        self.assertEqual(noti.status, 'leido')

    def test_generate_motivational(self):
        self.client.login(username='testuser', password='Testpass123')
        data = {'contexto': {'rutina_hecha': True, 'objetivo': 'bajar de peso', 'hora_preferida': '07:30:00'}}
        response = self.client.post(self.gen_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Felicidades', response.data['mensaje'])
        self.assertTrue(Notificacion.objects.filter(usuario=self.user, tipo='felicitacion').exists())

    def test_permissions_other_user(self):
        other = User.objects.create_user(username='other', email='other@example.com', password='Otherpass123')
        noti = Notificacion.objects.create(usuario=other, tipo='motivacional', mensaje='¡Hola!', hora_preferida=time(8,0))
        self.client.login(username='testuser', password='Testpass123')
        url = reverse('motivational-detail', args=[noti.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) 