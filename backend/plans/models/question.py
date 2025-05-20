from django.db import models

class PreguntaPlan(models.Model):
    texto = models.CharField(max_length=255)
    tipo_respuesta = models.CharField(max_length=50, default='texto')
    orden = models.PositiveIntegerField(default=1)
    es_obligatoria = models.BooleanField(default=True)
    activa = models.BooleanField(default=True)
    editable_por_admin = models.BooleanField(default=True)

    def __str__(self):
        return self.texto 