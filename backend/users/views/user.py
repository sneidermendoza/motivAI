from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from backend.utils import ResponseStandard, StandardResponseMixin
from django.contrib.auth import get_user_model
from ..serializers.user import UserSerializer, RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.hashers import check_password
from django.utils.crypto import get_random_string

User = get_user_model()

class UserViewSet(StandardResponseMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def update(self, request, *args, **kwargs):
        # Protección extra: solo admin puede cambiar tipo_usuario
        if 'tipo_usuario' in request.data and not request.user.is_superuser:
            return ResponseStandard.error(
                message="Solo un administrador puede cambiar el tipo de usuario.",
                status=403
            )
        return super().update(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return ResponseStandard.success(data=serializer.data, message="Perfil obtenido correctamente")

    @action(detail=False, methods=['post'], url_path='change-password', permission_classes=[permissions.IsAuthenticated])
    def change_password(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        new_password2 = request.data.get('new_password2')
        if not old_password or not new_password or not new_password2:
            return ResponseStandard.error(message="Debes enviar old_password, new_password y new_password2.", status=400)
        if not check_password(old_password, user.password):
            return ResponseStandard.error(message="La contraseña actual es incorrecta.", status=400)
        if new_password != new_password2:
            return ResponseStandard.error(message="Las nuevas contraseñas no coinciden.", status=400)
        if len(new_password) < 8:
            return ResponseStandard.error(message="La nueva contraseña debe tener al menos 8 caracteres.", status=400)
        user.set_password(new_password)
        user.save()
        return ResponseStandard.success(message="Contraseña cambiada correctamente.")

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return ResponseStandard.success(
                data=UserSerializer(user).data,
                message="Usuario registrado correctamente",
                status=status.HTTP_201_CREATED
            )
        return ResponseStandard.error(
            message="Error en el registro",
            data=serializer.errors,
            status=400
        )

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return ResponseStandard.error(message="No se proporcionó refresh token.", status=400)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return ResponseStandard.success(message="Sesión cerrada correctamente.")
        except TokenError:
            return ResponseStandard.error(message="Token inválido o ya fue deshabilitado.", status=400)