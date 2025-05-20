from django.db import models
from users.models.user import User

class Feedback(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    fecha = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=30, choices=[('feedback', 'Feedback'), ('sugerencia', 'Sugerencia'), ('reporte', 'Reporte')])
    mensaje = models.TextField()
    status = models.CharField(max_length=20, default='pendiente')

    def __str__(self):
        return f"Feedback de {self.usuario.username} - {self.tipo}" 