from rest_framework import serializers
from ..models.notification import Notificacion

class NotificacionSerializer(serializers.ModelSerializer):
    usuario = serializers.SerializerMethodField()

    class Meta:
        model = Notificacion
        fields = [
            'id', 'usuario', 'tipo', 'mensaje', 'fecha_envio', 'hora_preferida', 'contexto', 'status'
        ]
        read_only_fields = ['id', 'usuario', 'fecha_envio', 'status']

    def get_usuario(self, obj):
        return obj.usuario.username if obj.usuario else None 