# motivAI – Documentación técnica (Backend)

## 1. Autenticación y Usuarios
- **Registro:**  
  `POST /api/users/register/`  
  Registra un nuevo usuario.  
  **Campos:** `username`, `email`, `password`, `password2`

- **Login:**  
  `POST /api/users/login/`  
  Devuelve un token JWT.  
  **Campos:** `username`, `password`  
  **Nota:** El token solo incluye el `username` y claims estándar, **no** roles ni permisos.

- **Logout:**  
  `POST /api/users/logout/`  
  Invalida el refresh token JWT (blacklist).  
  **Campos:** `refresh` (string, obligatorio, el refresh token JWT a invalidar)  
  **Ejemplo de request:**
  ```json
  {
    "refresh": "<refresh_token>"
  }
  ```
  **Respuesta exitosa:**
  ```json
  {
    "success": true,
    "message": "Sesión cerrada correctamente.",
    "data": null
  }
  ```
  Si el token ya fue invalidado o es incorrecto, devuelve un error 400.

- **Perfil de usuario:**  
  `GET /api/users/me/`  
  Devuelve los datos básicos del usuario autenticado, incluyendo el campo `roles` que muestra el nombre del rol asignado al usuario.  
  Ejemplo de respuesta:
  ```json
  {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "",
    "last_name": "",
    "foto_perfil": null,
    "tipo_usuario": "usuario",
    "roles": ["usuario"],
    "status": "activo",
    "autenticacion_social": null,
    "fecha_registro": "2024-06-01T12:00:00Z"
  }
  ```

## 2. Sistema de Roles y Permisos
- **Modelos:**  
  - `Permission`: código, nombre, descripción.
  - `Role`: nombre, descripción, muchos a muchos con permisos.
  - `UserRole`: relación usuario-rol.
- **Seeds:**  
  - Los permisos y roles iniciales se cargan desde `users/fixtures/initial_roles_permissions.json`.
- **Endpoints de consulta (solo lectura, autenticado):**
  - `GET /api/users/roles/`  
    Lista todos los roles y sus permisos asociados.
  - `GET /api/users/permissions/`  
    Lista todos los permisos del sistema.

**Nota:**  
El perfil de usuario ahora incluye el campo `roles` para facilitar la construcción de menús dinámicos.

## 3. Planes y Perfil Fitness
- **Planes:**  
  CRUD completo sobre planes de entrenamiento (`/api/plans/planentrenamiento/`).
- **Perfil fitness:**  
  Asociado a cada plan, editable y consultable por el usuario.
- **Conversación:**  
  El flujo conversacional extrae datos y los guarda en el perfil fitness.

## 4. Permisos y Seguridad
- **Acceso a endpoints:**  
  - Usuarios autenticados pueden consultar y modificar solo sus propios datos.
  - Admins pueden ver y modificar todo.
- **El perfil de usuario incluye el campo `roles` para facilitar la construcción de menús dinámicos.**

## 5. Plan de trabajo actualizado

### Completado
- [x] Modelos de usuario, roles, permisos, perfil fitness, planes, rutinas, ejercicios, preguntas y respuestas.
- [x] Seeds/fixtures de roles y permisos.
- [x] Endpoints de autenticación, registro, login, perfil.
- [x] Endpoints de consulta de roles y permisos (solo lectura).
- [x] Extracción de datos fitness desde la conversación.
- [x] Documentación Swagger y ejemplos de request/response.
- [x] Seguridad: solo datos propios, sin exponer permisos en perfil ni token.
- [x] Inclusión del campo `roles` en el perfil de usuario.

### Pendiente / Próximos pasos
- [ ] Endpoint específico para menús dinámicos (si el frontend lo requiere).
- [ ] Mejorar la gestión de estados conversacionales y lógica de transición.
- [ ] Integración y pruebas con frontend Next.js y app móvil.
- [ ] Documentar casos de uso avanzados (admin, gestión masiva, etc).
- [ ] Mejorar la gestión de fixtures y seeds para ambientes de staging/producción.
- [ ] Pruebas automatizadas de permisos y flujos críticos.

## ¿Qué sigue?
1. **Integración con frontend:**  
   El frontend puede consumir `/api/users/me/` para datos básicos y `/api/users/roles/` o `/api/users/permissions/` si necesita construir menús o mostrar capacidades del usuario.

2. **Menús dinámicos:**  
   Si en el futuro se requiere, se puede crear un endpoint que devuelva solo los permisos/códigos relevantes para el usuario autenticado, optimizado para frontend.

3. **Pruebas y feedback:**  
   Probar el flujo completo en Swagger/Postman y ajustar según feedback de frontend/móvil. 