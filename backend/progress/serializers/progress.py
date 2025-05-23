from rest_framework import serializers
from ..models.progress import Progreso

class ProgresoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progreso
        fields = [
            'id', 'usuario', 'fecha', 'peso', 'medidas', 'imc', 'energia', 'observaciones', 'foto_progreso'
        ]
        read_only_fields = ['id', 'usuario', 'fecha'] 