# Documentación de Permisos

## Permisos por Endpoint

### Usuarios
- `/api/users/register/` - `AllowAny`
- `/api/users/login/` - `AllowAny`
- `/api/users/profile/` - `IsAuthenticated`
- `/api/users/roles/` - `IsAuthenticated`
- `/api/users/permissions/` - `IsAuthenticated`

### Planes
- `/api/plans/` - `IsAuthenticated`
  - GET: Listar planes (propios o todos si admin)
  - POST: Crear plan (usuario autenticado)
  - PUT/PATCH: Modificar plan (propio o admin)
  - DELETE: Eliminar plan (propio o admin) - Soft delete
- `/api/plans/generate/` - `IsAuthenticated`
- `/api/plans/fitness-profiles/` - `IsAuthenticated, IsAdminOrReadOnly`

### Rutinas
- `/api/routines/` - `IsAuthenticated`
  - GET: Listar rutinas (propias o todas si admin)
  - POST: Crear rutina (usuario autenticado)
  - PUT/PATCH: Modificar rutina (propia o admin)
  - DELETE: Eliminar rutina (propia o admin) - Soft delete
- `/api/routines/{id}/realizar/` - `IsAuthenticated` (propio o admin)

### Ejercicios
- `/api/exercises/` - `IsAuthenticated`
  - GET: Listar ejercicios
  - POST: Crear ejercicio (admin)
  - PUT/PATCH: Modificar ejercicio (admin)
  - DELETE: Eliminar ejercicio (admin) - Soft delete

### Conversación
- `/api/conversation/` - `IsAuthenticated`
- `/api/conversation/extract/` - `IsAuthenticated`
- `/api/conversation/reset/` - `IsAuthenticated`
- `/api/conversation/flows/` - `IsAuthenticated, IsAdminUser`

### Flujos de Conversación

| Endpoint | Método | Permisos Requeridos | Descripción |
|----------|---------|-------------------|-------------|
| `/api/conversation/flows/` | GET | `IsAuthenticated`, `IsAdminUser` | Listar flujos de conversación |
| `/api/conversation/flows/` | POST | `IsAuthenticated`, `IsAdminUser` | Crear flujo de conversación |
| `/api/conversation/flows/{id}/` | GET | `IsAuthenticated`, `IsAdminUser` | Obtener flujo de conversación |
| `/api/conversation/flows/{id}/` | PUT | `IsAuthenticated`, `IsAdminUser` | Actualizar flujo de conversación |
| `/api/conversation/flows/{id}/` | DELETE | `IsAuthenticated`, `IsAdminUser` | Eliminar flujo de conversación |

Notas:
- Solo los administradores pueden gestionar los flujos de conversación
- Los flujos de conversación son configurables desde el panel de administración
- Los flujos activos se utilizan para guiar la conversación con el usuario

## Progreso
- **Listar/Crear/Modificar/Eliminar progreso:**
  - Usuario autenticado: solo puede acceder a sus propios registros
  - Admin: puede acceder a todos los registros
  - Permiso: IsAuthenticated + IsOwnerOrAdmin

## Permisos Personalizados

### IsAdminOrReadOnly
- Permite lectura a cualquier usuario autenticado
- Permite escritura solo a administradores

### IsAdminUser (Plans)
- Permite acceso solo a administradores

### IsOwnerOrAdmin
- Permite acceso al dueño del recurso o a administradores
- Se usa en progreso, planes y rutinas

## Notificaciones Motivacionales
- **Endpoint**: `generar-motivacional`
- **Permisos**: Solo usuarios autenticados pueden generar notificaciones motivacionales.
- **Visualización**: Solo el admin puede ver todas las notificaciones, mientras que los usuarios normales solo ven las suyas con status `enviada`.

## Feedback
- **Enviar feedback (POST):** Cualquier usuario (anónimo o autenticado)
- **Listar feedbacks (GET):** Solo admin
- **Permiso:** IsAdminOrReadOnly

## Notas de Seguridad
1. Todos los endpoints requieren autenticación por defecto (configurado en settings.py)
2. Los endpoints públicos (AllowAny) son solo para registro y login
3. Los usuarios solo pueden acceder a sus propios recursos, excepto administradores
4. La eliminación es lógica (soft delete) por defecto
5. Los archivos subidos (fotos) son validados y sanitizados
6. Se implementa rate limiting en endpoints sensibles
7. Los tokens JWT tienen tiempo de expiración configurado

## Ejemplos de Uso

### 1. Acceso a Planes
```python
# Solo el dueño o admin puede modificar/eliminar
if not (user.is_staff or plan.usuario == user):
    return ResponseStandard.error(
        message="No tienes permiso para modificar este plan.",
        status=status.HTTP_403_FORBIDDEN
    )
```

### 2. Acceso a Progreso
```python
# Solo el dueño o admin puede ver/modificar
def get_queryset(self):
    user = self.request.user
    if user.is_staff:
        return Progreso.objects.all()
    return Progreso.objects.filter(usuario=user)
```

### 3. Acceso a Flujos de Conversación
```python
# Solo admin puede gestionar flujos
permission_classes = [IsAuthenticated, IsAdminUser]
```

## Códigos de Error Comunes
- 401: Unauthorized - Token inválido o expirado
- 403: Forbidden - No tiene permisos para acceder al recurso
- 404: Not Found - Recurso no encontrado
- 429: Too Many Requests - Rate limit excedido 