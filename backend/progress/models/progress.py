from django.db import models
from users.models.user import User

class Progreso(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progresos')
    fecha = models.DateField(auto_now_add=True)
    peso = models.FloatField(null=True, blank=True)
    medidas = models.JSONField(null=True, blank=True)  # cintura, pecho, etc.
    imc = models.FloatField(null=True, blank=True)
    energia = models.CharField(max_length=100, null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    foto_progreso = models.ImageField(upload_to='progress_photos/', null=True, blank=True)

    def __str__(self):
        return f"Progreso de {self.usuario.username} - {self.fecha}" 