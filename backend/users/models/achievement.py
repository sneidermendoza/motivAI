from django.db import models
from .user import User

class Logro(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    icono_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.nombre

class UsuarioLogro(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logros')
    logro = models.ForeignKey(Logro, on_delete=models.CASCADE, related_name='usuarios')
    fecha_obtenido = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.logro.nombre}" 