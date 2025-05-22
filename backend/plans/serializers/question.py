from rest_framework import serializers
from ..models.question import PreguntaPlan

class PreguntaPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreguntaPlan
        fields = '__all__' 