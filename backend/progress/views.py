from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers.progress import ProgresoSerializer
from .models.progress import Progreso
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.usuario == request.user

class ProgresoViewSet(viewsets.ModelViewSet):
    serializer_class = ProgresoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    @swagger_auto_schema(
        operation_description="Lista todos los registros de progreso del usuario autenticado (o todos si es admin)",
        responses={
            200: ProgresoSerializer(many=True),
        },
        tags=["Progreso"],
        examples=[
            {
                "id": 1,
                "usuario": 5,
                "fecha": "2024-06-10",
                "peso": 70.5,
                "medidas": {"cintura": 80, "pecho": 95},
                "imc": 22.5,
                "energia": "Alta",
                "observaciones": "Me siento bien",
                "foto_progreso": "/media/progress_photos/ejemplo.jpg"
            }
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Crea un nuevo registro de progreso. La foto es opcional.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'peso': openapi.Schema(type=openapi.TYPE_NUMBER, example=70.5),
                'medidas': openapi.Schema(type=openapi.TYPE_OBJECT, example={"cintura": 80, "pecho": 95}),
                'imc': openapi.Schema(type=openapi.TYPE_NUMBER, example=22.5),
                'energia': openapi.Schema(type=openapi.TYPE_STRING, example="Alta"),
                'observaciones': openapi.Schema(type=openapi.TYPE_STRING, example="Me siento bien"),
                'foto_progreso': openapi.Schema(type=openapi.TYPE_STRING, format='binary', description='Foto opcional')
            },
            required=['peso']
        ),
        responses={
            201: ProgresoSerializer(),
        },
        tags=["Progreso"]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        # Si es una vista de Swagger, devolver queryset vacío
        if getattr(self, 'swagger_fake_view', False):
            return Progreso.objects.none()
            
        user = self.request.user
        if user.is_staff:
            return Progreso.objects.all()
        return Progreso.objects.filter(usuario=user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
