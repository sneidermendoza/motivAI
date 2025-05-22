from rest_framework import serializers
from plans.models.plan import PlanEntrenamiento, UserFitnessProfile

class PlanEntrenamientoSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = PlanEntrenamiento
        fields = '__all__'

class UserFitnessProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFitnessProfile
        fields = '__all__' 