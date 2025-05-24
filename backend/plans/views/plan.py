from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from plans.models.plan import PlanEntrenamiento, UserFitnessProfile
from plans.serializers.plan import PlanEntrenamientoSerializer, UserFitnessProfileSerializer, PlanEntrenamientoDetailSerializer, RoutineSerializer, ExerciseSerializer
from conversation.models import Conversation
from conversation.serializers import ConversationSerializer
from backend.utils import ResponseStandard, StandardResponseMixin
from rest_framework.decorators import action
from plans.ai import generate_training_plan_with_groq
from datetime import timedelta
from plans.models.routine import Routine
from plans.models.exercise_routine import ExerciseRoutine
from plans.models.exercise import Exercise
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class PlanEntrenamientoViewSet(StandardResponseMixin, viewsets.ModelViewSet):
    """
    API endpoint para gestionar planes de entrenamiento
    """
    queryset = PlanEntrenamiento.objects.all()
    serializer_class = PlanEntrenamientoSerializer
    permission_classes = [permissions.IsAuthenticated]
    swagger_tags = ['Planes']

    @swagger_auto_schema(
        operation_description="Crea un nuevo plan de entrenamiento",
        request_body=PlanEntrenamientoSerializer,
        responses={201: PlanEntrenamientoDetailSerializer()}
    )
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

    @swagger_auto_schema(
        operation_description="Genera un plan personalizado usando IA",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['edad', 'peso', 'altura', 'objetivo'],
            properties={
                'edad': openapi.Schema(type=openapi.TYPE_INTEGER),
                'peso': openapi.Schema(type=openapi.TYPE_NUMBER),
                'altura': openapi.Schema(type=openapi.TYPE_INTEGER),
                'objetivo': openapi.Schema(type=openapi.TYPE_STRING),
                'nivel': openapi.Schema(type=openapi.TYPE_STRING),
                'restricciones': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                'preferencias': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING))
            }
        ),
        responses={200: openapi.Response(description="Plan generado exitosamente")}
    )
    @action(detail=False, methods=['post'], url_path='generate')
    def generate_plan(self, request):
        """
        Genera un plan personalizado usando Groq (Llama-3) a partir de los datos enviados.
        """
        user_data = request.data
        # Validación: si no hay datos requeridos, devolver 400
        required_fields = ['age', 'gender', 'weight', 'height', 'motivation', 'medical_conditions', 'injuries', 'exercise_frequency', 'experience_level', 'specific_goals', 'timeline']
        if not any(user_data.get(f) for f in required_fields):
            return ResponseStandard.error(
                message="Faltan datos requeridos para generar el plan.",
                data={"missing_fields": required_fields},
                status=status.HTTP_400_BAD_REQUEST
            )
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

    @swagger_auto_schema(
        operation_description="Lista el historial de planes inactivos (eliminados lógicamente) del usuario autenticado. Los administradores ven todos los planes inactivos. Ejemplo de respuesta: \n\n{\n  'success': true,\n  'message': 'Historial de planes inactivos.',\n  'data': [\n    {\n      'id': 1,\n      'usuario': 2,\n      'fecha_inicio': '2024-06-01',\n      'fecha_fin': null,\n      'objetivo': 'Bajar de peso',\n      'status': 'inactivo',\n      ...\n    }\n  ]\n}",
        responses={200: PlanEntrenamientoSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='historial', permission_classes=[permissions.IsAuthenticated])
    def historial(self, request):
        user = request.user
        qs = PlanEntrenamiento.objects.filter(status='inactivo')
        if not user.is_staff:
            qs = qs.filter(usuario=user)
        serializer = self.get_serializer(qs, many=True)
        return ResponseStandard.success(data=serializer.data, message="Historial de planes inactivos.")

    def get_queryset(self):
        user = self.request.user
        status_param = self.request.query_params.get('status', 'activo')
        qs = PlanEntrenamiento.objects.all()
        if not user.is_staff:
            qs = qs.filter(usuario=user)
        if status_param:
            qs = qs.filter(status=status_param)
        return qs

    def destroy(self, request, *args, **kwargs):
        plan = self.get_object()
        user = request.user
        if not (user.is_staff or plan.usuario == user):
            return ResponseStandard.error(message="No tienes permiso para eliminar este plan.", status=status.HTTP_403_FORBIDDEN)
        if plan.status == 'inactivo':
            return ResponseStandard.error(message="El plan ya está inactivo.", status=status.HTTP_400_BAD_REQUEST)
        plan.status = 'inactivo'
        plan.save()
        return ResponseStandard.success(message="Plan marcado como inactivo (eliminación lógica).", data=None, status=status.HTTP_200_OK)

class UserFitnessProfileViewSet(StandardResponseMixin, viewsets.ModelViewSet):
    """
    API endpoint para gestionar perfiles de fitness
    """
    queryset = UserFitnessProfile.objects.all()
    serializer_class = UserFitnessProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    swagger_tags = ['Planes']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return UserFitnessProfile.objects.all()
        return UserFitnessProfile.objects.filter(usuario=user)

class RoutineViewSet(StandardResponseMixin, viewsets.ModelViewSet):
    """
    API endpoint para gestionar rutinas
    """
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer
    permission_classes = [permissions.IsAuthenticated]
    swagger_tags = ['Ejercicios']

    @swagger_auto_schema(
        operation_description="Marca una rutina como realizada",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'fecha_realizacion': openapi.Schema(type=openapi.TYPE_STRING, format='date')
            }
        ),
        responses={200: RoutineSerializer()}
    )
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

    def get_queryset(self):
        status_param = self.request.query_params.get('status', 'activo')
        qs = Routine.objects.all()
        if status_param:
            qs = qs.filter(status=status_param)
        return qs

    def destroy(self, request, *args, **kwargs):
        rutina = self.get_object()
        user = request.user
        if not (user.is_staff or rutina.plan.usuario == user):
            return ResponseStandard.error(message="No tienes permiso para eliminar esta rutina.", status=status.HTTP_403_FORBIDDEN)
        if rutina.status == 'inactivo':
            return ResponseStandard.error(message="La rutina ya está inactiva.", status=status.HTTP_400_BAD_REQUEST)
        rutina.status = 'inactivo'
        rutina.save()
        return ResponseStandard.success(message="Rutina marcada como inactiva (eliminación lógica).", data=None, status=status.HTTP_200_OK)

class ExerciseViewSet(StandardResponseMixin, viewsets.ModelViewSet):
    """
    API endpoint para gestionar ejercicios
    """
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticated]
    swagger_tags = ['Ejercicios']

    def get_queryset(self):
        status_param = self.request.query_params.get('status', 'activo')
        qs = Exercise.objects.all()
        if status_param:
            qs = qs.filter(status=status_param)
        return qs

    def destroy(self, request, *args, **kwargs):
        ejercicio = self.get_object()
        if ejercicio.status == 'inactivo':
            return ResponseStandard.error(message="El ejercicio ya está inactivo.", status=status.HTTP_400_BAD_REQUEST)
        ejercicio.status = 'inactivo'
        ejercicio.save()
        return ResponseStandard.success(message="Ejercicio marcado como inactivo (eliminación lógica).", data=None, status=status.HTTP_200_OK) 