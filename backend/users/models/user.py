from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    edad = models.PositiveIntegerField(null=True, blank=True)
    sexo = models.CharField(max_length=10, null=True, blank=True)
    peso = models.FloatField(null=True, blank=True)
    altura = models.FloatField(null=True, blank=True)
    objetivo = models.CharField(max_length=255, null=True, blank=True)
    ocupacion = models.CharField(max_length=255, null=True, blank=True)
    nivel_actividad = models.CharField(max_length=50, null=True, blank=True)
    motivacion = models.TextField(null=True, blank=True)
    foto_perfil = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    tipo_usuario = models.CharField(max_length=20, default='usuario')
    status = models.CharField(max_length=20, default='activo')
    autenticacion_social = models.CharField(max_length=50, null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username 