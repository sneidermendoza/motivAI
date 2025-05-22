from rest_framework import viewsets, permissions
from ..models.question import PreguntaPlan
from ..serializers.question import PreguntaPlanSerializer

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class PreguntaPlanViewSet(viewsets.ModelViewSet):
    queryset = PreguntaPlan.objects.all()
    serializer_class = PreguntaPlanSerializer
    permission_classes = [IsAdminUser] 