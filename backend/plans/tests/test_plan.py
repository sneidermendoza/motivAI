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

    def test_cronograma_and_exercises_created(self):
        data = {
            'objetivo': 'Ganar músculo',
            'fecha_inicio': '2024-06-03',
            'dias_entrenar': 3,
            'dias_semana_entrenar': [0,2,4]  # Lunes, Miércoles, Viernes
        }
        response = self.client.post(self.plan_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        plan = response.data['data']['plan']
        rutinas = plan['rutinas']
        self.assertEqual(len(rutinas), 28)  # 4 semanas por default
        entrenamientos = [r for r in rutinas if r['tipo'] == 'entrenamiento']
        descansos = [r for r in rutinas if r['tipo'] == 'descanso']
        self.assertGreater(len(entrenamientos), 0)
        self.assertGreater(len(descansos), 0)
        # Verificar que cada rutina de entrenamiento tiene ejercicios
        for r in entrenamientos:
            self.assertIn('ejercicios', r)
            self.assertGreater(len(r['ejercicios']), 0)
            for ej in r['ejercicios']:
                self.assertIn('ejercicio', ej)
                self.assertIn('nombre', ej['ejercicio'])
                self.assertIn('imagen_url', ej['ejercicio'])
                self.assertIn('video_url', ej['ejercicio'])

    def test_marcar_rutina_realizada_dueno(self):
        # Crear plan y obtener una rutina
        data = {'objetivo': 'Ganar músculo', 'fecha_inicio': '2024-06-03'}
        response = self.client.post(self.plan_url, data, format='json')
        plan = response.data['data']['plan']
        rutina_id = plan['rutinas'][0]['id']
        url = f'/api/plans/rutinas/{rutina_id}/realizar/'
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['success'])
        self.assertTrue(response.data['data']['realizada'])

    def test_marcar_rutina_realizada_admin(self):
        # Crear plan con user1, luego loguear como admin y marcar rutina
        user2 = User.objects.create_superuser(username='admin', email='admin@example.com', password='Adminpass123')
        data = {'objetivo': 'Ganar músculo', 'fecha_inicio': '2024-06-03'}
        response = self.client.post(self.plan_url, data, format='json')
        plan = response.data['data']['plan']
        rutina_id = plan['rutinas'][0]['id']
        self.client.credentials()  # Logout user1
        login = self.client.post('/api/token/', {'username': 'admin', 'password': 'Adminpass123'}, format='json')
        access = login.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        url = f'/api/plans/rutinas/{rutina_id}/realizar/'
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['success'])
        self.assertTrue(response.data['data']['realizada'])

    def test_marcar_rutina_realizada_no_autorizado(self):
        # Crear plan con user1, luego loguear como user2 y tratar de marcar rutina
        user2 = User.objects.create_user(username='otro', email='otro@example.com', password='Testpass123')
        data = {'objetivo': 'Ganar músculo', 'fecha_inicio': '2024-06-03'}
        response = self.client.post(self.plan_url, data, format='json')
        plan = response.data['data']['plan']
        rutina_id = plan['rutinas'][0]['id']
        self.client.credentials()  # Logout user1
        login = self.client.post('/api/token/', {'username': 'otro', 'password': 'Testpass123'}, format='json')
        access = login.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        url = f'/api/plans/rutinas/{rutina_id}/realizar/'
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertFalse(response.data['success'])

    def test_no_duplicar_rutina_realizada(self):
        # Crear plan y marcar rutina dos veces
        data = {'objetivo': 'Ganar músculo', 'fecha_inicio': '2024-06-03'}
        response = self.client.post(self.plan_url, data, format='json')
        plan = response.data['data']['plan']
        rutina_id = plan['rutinas'][0]['id']
        url = f'/api/plans/rutinas/{rutina_id}/realizar/'
        response1 = self.client.post(url, {}, format='json')
        self.assertEqual(response1.status_code, 200)
        response2 = self.client.post(url, {}, format='json')
        self.assertEqual(response2.status_code, 400)
        self.assertFalse(response2.data['success'])

    def test_soft_delete_plan(self):
        data = {'objetivo': 'Soft Delete', 'fecha_inicio': '2024-06-03'}
        response = self.client.post(self.plan_url, data, format='json')
        plan_id = response.data['data']['plan']['id']
        url = f'/api/plans/planentrenamiento/{plan_id}/'
        # Soft delete
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        # El plan sigue existiendo pero con status inactivo
        from plans.models.plan import PlanEntrenamiento
        plan = PlanEntrenamiento.objects.get(id=plan_id)
        self.assertEqual(plan.status, 'inactivo')
        # No aparece en listado por default
        response = self.client.get(self.plan_url)
        ids = [p['id'] for p in response.data['data']]
        self.assertNotIn(plan_id, ids)
        # Aparece si filtro por status=inactivo
        response = self.client.get(self.plan_url + '?status=inactivo')
        ids = [p['id'] for p in response.data['data']]
        self.assertIn(plan_id, ids)

    def test_soft_delete_routine(self):
        data = {'objetivo': 'Soft Delete Routine', 'fecha_inicio': '2024-06-03'}
        response = self.client.post(self.plan_url, data, format='json')
        rutina_id = response.data['data']['plan']['rutinas'][0]['id']
        url = f'/api/plans/rutinas/{rutina_id}/'
        # Soft delete
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        from plans.models.routine import Routine
        rutina = Routine.objects.get(id=rutina_id)
        self.assertEqual(rutina.status, 'inactivo')
        # No aparece en listado por default
        response = self.client.get('/api/plans/rutinas/')
        ids = [r['id'] for r in response.data['data']]
        self.assertNotIn(rutina_id, ids)
        # Aparece si filtro por status=inactivo
        response = self.client.get('/api/plans/rutinas/?status=inactivo')
        ids = [r['id'] for r in response.data['data']]
        self.assertIn(rutina_id, ids)

    def test_soft_delete_exercise(self):
        from plans.models.exercise import Exercise
        # Crear ejercicio
        ejercicio = Exercise.objects.create(nombre='SoftDeleteTest', grupo_muscular='Test')
        url = f'/api/plans/ejercicios/{ejercicio.id}/'
        # Soft delete
        login = self.client.post('/api/token/', {'username': 'planuser', 'password': 'Testpass123'}, format='json')
        access = login.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        ejercicio.refresh_from_db()
        self.assertEqual(ejercicio.status, 'inactivo')
        # No aparece en listado por default
        response = self.client.get('/api/plans/ejercicios/')
        ids = [e['id'] for e in response.data['data']]
        self.assertNotIn(ejercicio.id, ids)
        # Aparece si filtro por status=inactivo
        response = self.client.get('/api/plans/ejercicios/?status=inactivo')
        ids = [e['id'] for e in response.data['data']]
        self.assertIn(ejercicio.id, ids) 