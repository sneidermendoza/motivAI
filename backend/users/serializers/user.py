from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    foto_perfil = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'edad', 'sexo', 'peso', 'altura', 'objetivo', 'ocupacion',
            'nivel_actividad', 'motivacion', 'foto_perfil', 'tipo_usuario',
            'status', 'autenticacion_social', 'fecha_registro'
        )
        read_only_fields = ('id', 'fecha_registro', 'tipo_usuario', 'status')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user 