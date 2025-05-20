from django.db import models
from users.models.user import User

class PlanEntrenamiento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='planes')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    objetivo = models.CharField(max_length=255)
    status = models.CharField(max_length=20, default='activo')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Plan de {self.usuario.username} ({self.objetivo})" 