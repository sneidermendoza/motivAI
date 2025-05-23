from django.db import models
from .plan import PlanEntrenamiento

class Routine(models.Model):
    plan = models.ForeignKey(PlanEntrenamiento, on_delete=models.CASCADE, related_name='rutinas')
    dia = models.PositiveIntegerField()  # Día dentro del plan
    tipo = models.CharField(max_length=20, choices=[('entrenamiento', 'Entrenamiento'), ('descanso', 'Descanso')])
    observaciones = models.TextField(null=True, blank=True)
    fecha = models.DateField(null=True, blank=True)
    realizada = models.BooleanField(default=False)
    fecha_realizacion = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default='activo')

    def __str__(self):
        return f"Rutina día {self.dia} ({self.tipo}) - Plan {self.plan.id}" 