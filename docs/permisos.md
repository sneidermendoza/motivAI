# Documentación de Permisos

## Permisos por Endpoint

### Usuarios
- `/api/users/register/` - `AllowAny`
- `/api/users/login/` - `AllowAny`
- `/api/users/profile/` - `IsAuthenticated`
- `/api/users/roles/` - `IsAuthenticated`

### Planes
- `/api/plans/` - `IsAuthenticated`
  - GET: Listar planes (propios o todos si admin)
  - POST: Crear plan (usuario autenticado)
  - PUT/PATCH: Modificar plan (propio o admin)
  - DELETE: Eliminar plan (propio o admin)
- `/api/plans/generate/` - `IsAuthenticated`
- `/api/plans/fitness-profiles/` - `IsAuthenticated, IsAdminOrReadOnly`

### Rutinas
- `/api/routines/` - `IsAuthenticated`
  - GET: Listar rutinas (propias o todas si admin)
  - POST: Crear rutina (usuario autenticado)
  - PUT/PATCH: Modificar rutina (propia o admin)
  - DELETE: Eliminar rutina (propia o admin)
- `/api/routines/{id}/realizar/` - `IsAuthenticated` (propio o admin)

### Ejercicios
- `/api/exercises/` - `IsAuthenticated`
  - GET: Listar ejercicios
  - POST: Crear ejercicio (admin)
  - PUT/PATCH: Modificar ejercicio (admin)
  - DELETE: Eliminar ejercicio (admin)

### Conversación
- `/api/conversation/` - `IsAuthenticated`
- `/api/conversation/extract/` - `IsAuthenticated`
- `/api/conversation/reset/` - `IsAuthenticated`

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

## Notas de Seguridad
1. Todos los endpoints requieren autenticación por defecto (configurado en settings.py)
2. Los endpoints públicos (AllowAny) son solo para registro y login
3. Los usuarios solo pueden acceder a sus propios recursos, excepto administradores
4. La eliminación es lógica (soft delete) por defecto 