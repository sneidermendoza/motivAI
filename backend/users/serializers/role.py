from rest_framework import serializers
from users.models.role import Permission, Role

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'code', 'name', 'description')

class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        fields = ('id', 'name', 'description', 'permissions') 