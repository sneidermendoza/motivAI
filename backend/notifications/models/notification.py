from django.db import models
from users.models.user import User

class Notificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones')
    tipo = models.CharField(max_length=30, choices=[('push', 'Push'), ('motivacional', 'Motivacional')])
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pendiente')

    def __str__(self):
        return f"Notificación para {self.usuario.username} - {self.tipo}" 