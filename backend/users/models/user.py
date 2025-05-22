from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    foto_perfil = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    tipo_usuario = models.CharField(max_length=20, default='usuario')
    status = models.CharField(max_length=20, default='activo')
    autenticacion_social = models.CharField(max_length=50, null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    TIPO_USUARIO_CHOICES = (
        ('admin', 'Administrador'),
        ('usuario', 'Usuario'),
    )
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES, default='usuario')

    def __str__(self):
        return self.username 