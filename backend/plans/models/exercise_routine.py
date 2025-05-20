from django.db import models
from .routine import Routine
from .exercise import Exercise

class ExerciseRoutine(models.Model):
    rutina = models.ForeignKey(Routine, on_delete=models.CASCADE, related_name='ejercicios')
    ejercicio = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    repeticiones = models.PositiveIntegerField()
    series = models.PositiveIntegerField()
    peso_sugerido = models.FloatField(null=True, blank=True)
    descanso_segundos = models.PositiveIntegerField(default=60)
    orden = models.PositiveIntegerField(default=1)
    observaciones = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.ejercicio.nombre} en rutina {self.rutina.id}" 