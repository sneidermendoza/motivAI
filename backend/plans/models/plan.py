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

class UserFitnessProfile(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fitness_profiles')
    plan = models.ForeignKey(PlanEntrenamiento, on_delete=models.CASCADE, related_name='fitness_profiles')
    motivacion = models.TextField(null=True, blank=True)
    objetivo = models.CharField(max_length=255, null=True, blank=True)
    edad = models.PositiveIntegerField(null=True, blank=True)
    sexo = models.CharField(max_length=10, null=True, blank=True)
    peso = models.FloatField(null=True, blank=True)
    altura = models.FloatField(null=True, blank=True)
    nivel_actividad = models.CharField(max_length=50, null=True, blank=True)
    restricciones = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    otros = models.JSONField(null=True, blank=True, default=dict)

    def __str__(self):
        return f"Perfil fitness de {self.usuario.username} para plan {self.plan.id}" 