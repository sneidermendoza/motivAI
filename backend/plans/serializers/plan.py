from rest_framework import serializers
from plans.models.plan import PlanEntrenamiento, UserFitnessProfile
from plans.models.routine import Routine
from plans.models.exercise_routine import ExerciseRoutine
from plans.models.exercise import Exercise

class PlanEntrenamientoSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = PlanEntrenamiento
        fields = '__all__'

class UserFitnessProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFitnessProfile
        fields = '__all__'

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'nombre', 'grupo_muscular', 'descripcion', 'imagen_url', 'video_url', 'equipo', 'dificultad']

class ExerciseRoutineSerializer(serializers.ModelSerializer):
    ejercicio = ExerciseSerializer(read_only=True)
    class Meta:
        model = ExerciseRoutine
        fields = ['id', 'ejercicio', 'repeticiones', 'series', 'peso_sugerido', 'descanso_segundos', 'orden', 'observaciones']

class RoutineSerializer(serializers.ModelSerializer):
    ejercicios = ExerciseRoutineSerializer(many=True, read_only=True)
    class Meta:
        model = Routine
        fields = ['id', 'dia', 'tipo', 'fecha', 'observaciones', 'ejercicios']

class PlanEntrenamientoDetailSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(read_only=True)
    rutinas = RoutineSerializer(many=True, read_only=True)
    class Meta:
        model = PlanEntrenamiento
        fields = '__all__' 