from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from plans.models.plan import PlanEntrenamiento, UserFitnessProfile
from plans.serializers.plan import PlanEntrenamientoSerializer, UserFitnessProfileSerializer, PlanEntrenamientoDetailSerializer, RoutineSerializer
from conversation.models import Conversation
from conversation.serializers import ConversationSerializer
from backend.utils import ResponseStandard, StandardResponseMixin
from rest_framework.decorators import action
from plans.ai import generate_training_plan_with_groq
from datetime import timedelta
from plans.models.routine import Routine
from plans.models.exercise_routine import ExerciseRoutine
from plans.models.exercise import Exercise

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class PlanEntrenamientoViewSet(viewsets.ModelViewSet):
    queryset = PlanEntrenamiento.objects.all()
    serializer_class = PlanEntrenamientoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return ResponseStandard.error(message="Datos inválidos", data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        plan = serializer.save(usuario=request.user)
        fecha_inicio = plan.fecha_inicio
        duracion = (plan.fecha_fin - fecha_inicio).days + 1 if plan.fecha_fin else 28
        dias_entrenar = request.data.get('dias_entrenar', 3)
        dias_semana_entrenar = request.data.get('dias_semana_entrenar', [0,2,4])  # 0=Lunes
        # Ejercicios de ejemplo (en el futuro, vendrán de la IA)
        ejercicios_demo = [
            {"nombre": "Sentadillas", "repeticiones": 12, "series": 3},
            {"nombre": "Press de banca", "repeticiones": 10, "series": 3},
            {"nombre": "Remo con barra", "repeticiones": 10, "series": 3}
        ]
        for i in range(duracion):
            fecha = fecha_inicio + timedelta(days=i)
            dia_semana = fecha.weekday()
            tipo = 'entrenamiento' if dia_semana in dias_semana_entrenar else 'descanso'
            rutina = Routine.objects.create(
                plan=plan,
                dia=i+1,
                tipo=tipo,
                fecha=fecha
            )
            # Asociar ejercicios solo si es entrenamiento
            if tipo == 'entrenamiento':
                for idx, ej in enumerate(ejercicios_demo):
                    ejercicio, _ = Exercise.objects.get_or_create(nombre=ej["nombre"])
                    ExerciseRoutine.objects.create(
                        rutina=rutina,
                        ejercicio=ejercicio,
                        repeticiones=ej["repeticiones"],
                        series=ej["series"],
                        orden=idx+1
                    )
        # Crea una conversación asociada automáticamente
        conversation = Conversation.objects.create(
            user=request.user,
            context={"plan_id": plan.id},
            current_state="initial"
        )
        conversation_data = ConversationSerializer(conversation).data
        plan_data = PlanEntrenamientoDetailSerializer(plan).data
        return ResponseStandard.success(
            data={"plan": plan_data, "conversation": conversation_data},
            message="Plan, cronograma y conversación creados correctamente.",
            status=status.HTTP_201_CREATED
        )

    def perform_create(self, serializer):
        # Ya no se usa, la lógica está en create
        pass

    @action(detail=False, methods=['post'], url_path='generate')
    def generate_plan(self, request):
        """
        Genera un plan personalizado usando Groq (Llama-3) a partir de los datos enviados.
        """
        user_data = request.data
        plan_json = generate_training_plan_with_groq(user_data)
        if plan_json and not plan_json.get('error'):
            return ResponseStandard.success(
                data=plan_json,
                message="Plan generado exitosamente por Groq IA.",
                status=status.HTTP_200_OK
            )
        else:
            error_msg = plan_json.get('error', 'No se pudo generar el plan con Groq IA.') if isinstance(plan_json, dict) else 'No se pudo generar el plan con Groq IA.'
            return ResponseStandard.error(
                message=error_msg,
                data=plan_json,
                status=plan_json.get('status_code', status.HTTP_500_INTERNAL_SERVER_ERROR) if isinstance(plan_json, dict) else status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserFitnessProfileViewSet(StandardResponseMixin, viewsets.ModelViewSet):
    queryset = UserFitnessProfile.objects.all()
    serializer_class = UserFitnessProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return UserFitnessProfile.objects.all()
        return UserFitnessProfile.objects.filter(usuario=user)

class RoutineViewSet(viewsets.ModelViewSet):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'], url_path='realizar')
    def marcar_realizada(self, request, pk=None):
        rutina = self.get_object()
        user = request.user
        # Solo dueño del plan o admin
        if not (user.is_staff or rutina.plan.usuario == user):
            return ResponseStandard.error(message="No tienes permiso para modificar esta rutina.", status=status.HTTP_403_FORBIDDEN)
        if rutina.realizada:
            return ResponseStandard.error(message="La rutina ya fue marcada como realizada.", status=status.HTTP_400_BAD_REQUEST)
        fecha_realizacion = request.data.get('fecha_realizacion')
        from datetime import date
        rutina.realizada = True
        rutina.fecha_realizacion = fecha_realizacion or date.today()
        rutina.save()
        return ResponseStandard.success(
            data=RoutineSerializer(rutina).data,
            message="Rutina marcada como realizada.",
            status=status.HTTP_200_OK
        ) 