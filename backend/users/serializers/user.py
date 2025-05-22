from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField(validators=[validate_email])

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password2': 'Las contraseñas no coinciden.'})
        return data

    def validate_password(self, value):
        # Contraseña fuerte: mínimo 8 caracteres, al menos una letra y un número
        if len(value) < 8:
            raise serializers.ValidationError('La contraseña debe tener al menos 8 caracteres.')
        if not re.search(r'[A-Za-z]', value) or not re.search(r'\d', value):
            raise serializers.ValidationError('La contraseña debe contener letras y números.')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Este correo ya está registrado.')
        return value

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            tipo_usuario='usuario'
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    foto_perfil = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'foto_perfil', 'tipo_usuario',
            'status', 'autenticacion_social', 'fecha_registro'
        )
        read_only_fields = ('id', 'fecha_registro', 'tipo_usuario', 'status')

    def create(self, validated_data):
        # Siempre asigna tipo_usuario='usuario' al crear
        validated_data['tipo_usuario'] = 'usuario'
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        # Solo un superusuario puede cambiar tipo_usuario
        request = self.context.get('request')
        if 'tipo_usuario' in validated_data:
            if not request or not request.user.is_superuser:
                validated_data.pop('tipo_usuario')
        return super().update(instance, validated_data)