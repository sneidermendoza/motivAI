from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers.feedback import FeedbackSerializer
from .models.feedback import Feedback
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_staff
        return True

class FeedbackViewSet(viewsets.ModelViewSet):
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    @swagger_auto_schema(
        operation_description="Lista todos los feedbacks (solo admin)",
        responses={200: FeedbackSerializer(many=True)},
        tags=["Feedback"],
        examples=[
            {
                "id": 1,
                "usuario": "testuser",
                "fecha": "2024-06-10T12:00:00Z",
                "tipo": "sugerencia",
                "mensaje": "Me gusta la app!",
                "status": "pendiente"
            }
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Envía feedback (anónimo o autenticado)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'tipo': openapi.Schema(type=openapi.TYPE_STRING, enum=["feedback", "sugerencia", "reporte"], example="sugerencia"),
                'mensaje': openapi.Schema(type=openapi.TYPE_STRING, example="Me gusta la app!")
            },
            required=['tipo', 'mensaje']
        ),
        responses={201: FeedbackSerializer()},
        tags=["Feedback"]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(usuario=user)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Feedback.objects.all()
        # Un usuario solo puede ver sus propios feedbacks (opcional, o solo permitir POST)
        return Feedback.objects.filter(usuario=user)
