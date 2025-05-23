from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models.user import User
from ..models.progress import Progreso
from rest_framework.authtoken.models import Token
from django.core.files.uploadedfile import SimpleUploadedFile
import io
from PIL import Image

class ProgresoAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='Testpass123')
        self.admin = User.objects.create_superuser(username='admin', email='admin@example.com', password='Adminpass123')
        self.progreso_url = reverse('progreso-list')
        self.client.login(username='testuser', password='Testpass123')

    def get_image_file(self, name='test.jpg', ext='jpeg', size=(100, 100), color=(256,0,0)):
        file_obj = io.BytesIO()
        image = Image.new("RGB", size, color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return SimpleUploadedFile(name, file_obj.read(), content_type='image/jpeg')

    def test_create_progreso(self):
        data = {
            'peso': 70.5,
            'medidas': {'cintura': 80, 'pecho': 95},
            'imc': 22.5,
            'energia': 'Alta',
            'observaciones': 'Me siento bien',
            'foto_progreso': self.get_image_file()
        }
        response = self.client.post(self.progreso_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Progreso.objects.count(), 1)
        self.assertEqual(Progreso.objects.first().usuario, self.user)

    def test_list_progreso(self):
        Progreso.objects.create(usuario=self.user, peso=70)
        response = self.client.get(self.progreso_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_detail_progreso(self):
        progreso = Progreso.objects.create(usuario=self.user, peso=70)
        url = reverse('progreso-detail', args=[progreso.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['peso'], 70)

    def test_update_progreso(self):
        progreso = Progreso.objects.create(usuario=self.user, peso=70)
        url = reverse('progreso-detail', args=[progreso.id])
        data = {'peso': 72}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        progreso.refresh_from_db()
        self.assertEqual(progreso.peso, 72)

    def test_delete_progreso(self):
        progreso = Progreso.objects.create(usuario=self.user, peso=70)
        url = reverse('progreso-detail', args=[progreso.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Progreso.objects.count(), 0)

    def test_only_owner_can_access(self):
        other_user = User.objects.create_user(username='other', email='other@example.com', password='Otherpass123')
        progreso = Progreso.objects.create(usuario=other_user, peso=80)
        url = reverse('progreso-detail', args=[progreso.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_access_all(self):
        progreso = Progreso.objects.create(usuario=self.user, peso=70)
        self.client.logout()
        self.client.login(username='admin', password='Adminpass123')
        url = reverse('progreso-detail', args=[progreso.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 