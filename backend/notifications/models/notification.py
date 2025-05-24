from django.db import models
from users.models.user import User

class Notificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones', null=True, blank=True)
    tipo = models.CharField(max_length=30, choices=[('push', 'Push'), ('motivacional', 'Motivacional'), ('recordatorio', 'Recordatorio'), ('felicitacion', 'Felicitación')], default='motivacional')
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    hora_preferida = models.TimeField(null=True, blank=True)
    contexto = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=20, default='pendiente')  # pendiente, enviado, leido

    def __str__(self):
        user_str = self.usuario.username if self.usuario else 'Global'
        return f"Notificación para {user_str} - {self.tipo}" 