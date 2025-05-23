# motivAI – Documentación técnica (Backend)

## 1. Autenticación y Usuarios
- **Registro:**  
  `POST /api/users/register/`  
  Registra un nuevo usuario.  
  **Campos:** `username`, `email`, `password`, `password2`

- **Login:**  
  `POST /api/token/`  
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
  `GET /api/users/profile/me/`  
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
- **Generación de plan por IA:**  
  Endpoint: `POST /api/plans/planentrenamiento/generate/`  
  Utiliza Groq (Llama-3) para generar un plan personalizado a partir de los datos del usuario.  
  **Ejemplo de request:**
  ```json
  {
    "age": 28,
    "gender": "male",
    "weight": 80,
    "height": 175,
    "motivation": "Quiero bajar de peso y sentirme con más energía.",
    "medical_conditions": "Ninguna",
    "injuries": "Ninguna",
    "exercise_frequency": "2 veces por semana",
    "experience_level": "principiante",
    "specific_goals": "Bajar 5kg en 3 meses",
    "timeline": "3 meses",
    "additional_info": "Trabajo muchas horas sentado y me gustaría mejorar mi postura."
  }
  ```
  **Respuesta exitosa:**
  ```json
  {
    "success": true,
    "message": "Plan generado exitosamente por Groq IA.",
    "data": {
      "plan": [ ... ],
      "recommendations": [ ... ]
    }
  }
  ```
- **Perfil fitness:**  
  Asociado a cada plan, editable y consultable por el usuario.
- **Conversación:**  
  El flujo conversacional extrae datos y los guarda en el perfil fitness.

## 4. Permisos y Seguridad
- **Acceso a endpoints:**  
  - Usuarios autenticados pueden consultar y modificar solo sus propios datos.
  - Admins pueden ver y modificar todo.
- **El perfil de usuario incluye el campo `roles` para facilitar la construcción de menús dinámicos.**

## 5. Testing automatizado y buenas prácticas

### Ejecución de tests
- Para correr **todos los tests** del backend y validar el flujo MVP:
  ```bash
  python manage.py test
  ```
- Los tests cubren:
  - Registro, login, perfil, logout
  - Creación de plan y perfil fitness
  - Conversación y respuestas
  - Permisos y errores comunes

### Buenas prácticas para desarrolladores
- **Siempre agregar tests** para nuevos endpoints o cambios en lógica crítica.
- **Si agregas un modelo con campos ForeignKey que se asignan automáticamente en la vista (ej: user, usuario), márcalos como `read_only=True` en el serializer.**
- **No expongas campos sensibles ni permisos en el token JWT.**
- **Usa `ResponseStandard` para respuestas claras y estructuradas.**
- **Documenta endpoints y ejemplos en Swagger y en este README.**
- **Antes de hacer merge o deploy, corre siempre los tests.**

## 6. Plan de trabajo actualizado

### Completado
- [x] Modelos de usuario, roles, permisos, perfil fitness, planes, rutinas, ejercicios, preguntas y respuestas.
- [x] Seeds/fixtures de roles y permisos.
- [x] Endpoints de autenticación, registro, login, perfil, logout.
- [x] Endpoints de consulta de roles y permisos (solo lectura).
- [x] Extracción de datos fitness desde la conversación.
- [x] Documentación Swagger y ejemplos de request/response.
- [x] Seguridad: solo datos propios, sin exponer permisos en perfil ni token.
- [x] Inclusión del campo `roles` en el perfil de usuario.
- [x] Pruebas automatizadas de todo el flujo MVP.
- [x] Robustez y estandarización de respuestas API.
- [x] Mejorar la gestión de estados conversacionales y lógica de transición.

### Pendiente / Próximos pasos
- [ ] Integración y pruebas con frontend Next.js y app móvil.
- [ ] Documentar casos de uso avanzados (admin, gestión masiva, etc).
- [ ] Mejorar la gestión de fixtures y seeds para ambientes de staging/producción.
- [ ] Pruebas automatizadas de permisos y flujos críticos adicionales.
- [ ] Endpoint específico para menús dinámicos (si el frontend lo requiere).

## 6. Extracción y validación conversacional (IA)
- **POST** `/api/conversation/extract/`
- **Permiso:** Autenticado
- **Body:**
```json
{
  "message": "Tengo 30 años, peso 75kg, mido 180cm, soy hombre, quiero ganar músculo, entreno 4 veces por semana en gimnasio, no tengo lesiones."
}
```
- **Respuesta exitosa:**
```json
{
  "success": true,
  "message": "Datos extraídos correctamente",
  "data": {
    "edad": 30,
    "sexo": "masculino",
    "peso": 75,
    "altura": 180,
    "objetivo": "ganar músculo",
    "motivacion": "",
    "nivel_actividad": "",
    "restricciones": "no tengo lesiones",
    "frecuencia_ejercicio": "4 veces por semana",
    "nivel_experiencia": null,
    "dias_entrenar": 4,
    "lugar_entrenamiento": "gimnasio",
    "otros": null,
    "missing_fields": []
  }
}
```
- **Respuesta con campos faltantes:**
```json
{
  "success": false,
  "message": "Faltan campos",
  "data": {
    "missing_fields": ["edad", "peso", "altura", "sexo", "objetivo"]
  }
}
```

## ¿Qué sigue?
1. **Integración con frontend:**
   - Coordinar con el equipo frontend para que consuman los endpoints y reporten cualquier ajuste necesario.

2. **Pruebas y feedback:**
   - Probar el flujo completo en Swagger/Postman y ajustar según feedback de frontend/móvil. 