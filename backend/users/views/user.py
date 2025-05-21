from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from backend.utils import ResponseStandard, StandardResponseMixin
from django.contrib.auth import get_user_model
from ..serializers.user import UserSerializer

User = get_user_model()

class UserViewSet(StandardResponseMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return ResponseStandard.success(data=serializer.data, message="Perfil obtenido correctamente") 