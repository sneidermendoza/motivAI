from django.db import models
from users.models.user import User

class Feedback(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks', null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=30, choices=[('feedback', 'Feedback'), ('sugerencia', 'Sugerencia'), ('reporte', 'Reporte')])
    mensaje = models.TextField()
    status = models.CharField(max_length=20, default='pendiente')

    def __str__(self):
        user_str = self.usuario.username if self.usuario else 'Anónimo'
        return f"Feedback de {user_str} - {self.tipo}" 