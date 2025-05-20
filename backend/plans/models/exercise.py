from django.db import models

class Exercise(models.Model):
    nombre = models.CharField(max_length=100)
    grupo_muscular = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    imagen_url = models.URLField(null=True, blank=True)
    equipo = models.CharField(max_length=100, null=True, blank=True)
    dificultad = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=20, default='activo')
    creado_por_ia = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre 