from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..serializers.notification import NotificacionSerializer
from ..models.notification import Notificacion
from users.models.user import User
from datetime import datetime, time

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or (obj.usuario == request.user)

class NotificacionViewSet(viewsets.ModelViewSet):
    serializer_class = NotificacionSerializer
    queryset = Notificacion.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        # Si es una vista de Swagger, devolver queryset vacío
        if getattr(self, 'swagger_fake_view', False):
            return Notificacion.objects.none()
            
        user = self.request.user
        if user.is_staff:
            return Notificacion.objects.all()
        return Notificacion.objects.filter(usuario=user, status='enviada')

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(usuario=user)

    @action(detail=True, methods=['patch'], url_path='marcar-leido')
    def marcar_leido(self, request, pk=None):
        noti = self.get_object()
        noti.status = 'leido'
        noti.save()
        return Response({'success': True, 'message': 'Notificación marcada como leída.'})

    @action(detail=False, methods=['post'], url_path='generar-motivacional')
    def generar_motivacional(self, request):
        """
        Genera y envía un mensaje motivacional personalizado según el contexto del usuario.
        """
        user = request.user
        contexto = request.data.get('contexto', {})
        rutina_hecha = contexto.get('rutina_hecha', False)
        objetivo = contexto.get('objetivo', 'mejorar tu salud')
        nombre = user.first_name or user.username
        if rutina_hecha:
            mensaje = f"¡Felicidades {nombre}! Has completado tu rutina de hoy. Sigue así para lograr tu objetivo de {objetivo}."
            tipo = 'felicitacion'
        else:
            mensaje = f"¡Hola {nombre}! Recuerda que tu objetivo es {objetivo}. ¡Hoy es un gran día para avanzar en tu rutina!"
            tipo = 'motivacional'
        hora_preferida = contexto.get('hora_preferida')
        if hora_preferida:
            hora = time.fromisoformat(hora_preferida)
        else:
            hora = time(8, 0)  # 8:00 AM por defecto
        noti = Notificacion.objects.create(
            usuario=user,
            tipo=tipo,
            mensaje=mensaje,
            hora_preferida=hora,
            contexto=contexto,
            status='pendiente'
        )
        return Response({'success': True, 'mensaje': mensaje, 'id': noti.id}) 