from django.db import models
from users.models.user import User
from .question import PreguntaPlan

class RespuestaPlan(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(PreguntaPlan, on_delete=models.CASCADE)
    respuesta = models.TextField()
    fecha_respuesta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.pregunta.texto}" 