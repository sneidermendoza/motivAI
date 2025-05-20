from django.contrib import admin
from .models.plan import PlanEntrenamiento
from .models.routine import Routine
from .models.exercise import Exercise
from .models.exercise_routine import ExerciseRoutine
from .models.question import PreguntaPlan
from .models.answer import RespuestaPlan


admin.site.register(PlanEntrenamiento)
admin.site.register(Routine)
admin.site.register(Exercise)
admin.site.register(ExerciseRoutine)
admin.site.register(PreguntaPlan)
admin.site.register(RespuestaPlan)
