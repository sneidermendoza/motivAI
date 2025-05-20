from rest_framework.response import Response
from rest_framework import status

class ResponseStandard:
    @staticmethod
    def success(data=None, message="Operación exitosa", status=200):
        return Response({
            "success": True,
            "message": message,
            "data": data
        }, status=status)

    @staticmethod
    def error(message="Ocurrió un error", data=None, status=400):
        return Response({
            "success": False,
            "message": message,
            "data": data
        }, status=status)

class StandardResponseMixin:
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return ResponseStandard.success(data=response.data, message="Listado obtenido correctamente")

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return ResponseStandard.success(data=response.data, message="Detalle obtenido correctamente")

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return ResponseStandard.success(data=response.data, message="Creado correctamente", status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return ResponseStandard.success(data=response.data, message="Actualizado correctamente")

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return ResponseStandard.success(data=None, message="Eliminado correctamente", status=status.HTTP_204_NO_CONTENT) 