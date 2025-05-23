from rest_framework import serializers
from ..models.feedback import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    usuario = serializers.SerializerMethodField()

    class Meta:
        model = Feedback
        fields = ['id', 'usuario', 'fecha', 'tipo', 'mensaje', 'status']
        read_only_fields = ['id', 'usuario', 'fecha', 'status']

    def get_usuario(self, obj):
        return obj.usuario.username if obj.usuario else None 