from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from plans.models.plan import PlanEntrenamiento, UserFitnessProfile
from plans.serializers.plan import PlanEntrenamientoSerializer, UserFitnessProfileSerializer
from conversation.models import Conversation
from conversation.serializers import ConversationSerializer

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
        serializer.is_valid(raise_exception=True)
        plan = serializer.save(usuario=request.user)
        # Crea una conversación asociada automáticamente
        conversation = Conversation.objects.create(
            user=request.user,
            context={"plan_id": plan.id},
            current_state="initial"
        )
        conversation_data = ConversationSerializer(conversation).data
        plan_data = PlanEntrenamientoSerializer(plan).data
        return Response({"plan": plan_data, "conversation": conversation_data}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        # Ya no se usa, la lógica está en create
        pass

class UserFitnessProfileViewSet(viewsets.ModelViewSet):
    queryset = UserFitnessProfile.objects.all()
    serializer_class = UserFitnessProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return UserFitnessProfile.objects.all()
        return UserFitnessProfile.objects.filter(usuario=user) 