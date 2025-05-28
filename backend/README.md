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

---

## Recuperación de contraseña y emails personalizados

### Flujo de recuperación de contraseña

- **Endpoint:**  
  `POST /api/users/password-reset/`  
  Envía un email con un enlace para restablecer la contraseña del usuario.

- **Requisitos:**  
  - El usuario debe estar registrado y activo.  
  - El email debe ser válido y único.

- **Funcionamiento:**  
  - Al solicitar el reset, se genera un token y se dispara una señal.
  - Un handler personalizado (`users/apps.py`) envía el email usando una plantilla HTML personalizada.

### Personalización del email

- **Plantilla:**  
  El email se genera usando la plantilla HTML ubicada en:  
  `users/templates/registration/password_reset_email.html`

- **Ejemplo de contenido de la plantilla:**
  ```html
  <!DOCTYPE html>
  <html>
    <head>
      <meta charset="utf-8" />
      <title>Recupera tu contraseña - motivAI</title>
      <style>
        body { background: #f0f6ff; font-family: 'Montserrat', Arial, sans-serif; color: #22223b; margin: 0; padding: 0; }
        .container { max-width: 420px; margin: 40px auto; background: #fff; border-radius: 16px; box-shadow: 0 4px 24px rgba(37,99,235,0.08); padding: 32px 24px; text-align: center; }
        .logo { margin-bottom: 16px; }
        .btn { display: inline-block; margin-top: 24px; padding: 12px 32px; background: linear-gradient(90deg, #2563eb 0%, #22d3ee 100%); color: #fff; border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 16px; letter-spacing: 1px; box-shadow: 0 2px 8px rgba(37,99,235,0.10); }
        .footer { margin-top: 32px; font-size: 13px; color: #64748b; }
      </style>
    </head>
    <body>
      <div class="container">
        <div class="logo">
          <!-- Logo SVG motivAI -->
        </div>
        <h2>¿Olvidaste tu contraseña?</h2>
        <p>
          ¡No te preocupes! Haz clic en el botón para restablecer tu contraseña y seguir entrenando con motivAI.
        </p>
        <a href="{{ password_reset_url }}" class="btn">Restablecer contraseña</a>
        <p style="margin-top:24px;">
          Si no solicitaste este cambio, puedes ignorar este correo.
        </p>
        <div class="footer">
          motivAI &copy; {{ current_year }}<br>
          <span style="color:#f59e42;">¡Entrena mejor, vive mejor!</span>
        </div>
      </div>
    </body>
  </html>
  ```

- **Variables disponibles en la plantilla:**
  - `password_reset_url`: Enlace único para restablecer la contraseña.
  - `current_year`: Año actual.

### Handler de señal

- El envío del email se realiza en el handler `password_reset_token_created` en `users/apps.py`:
  ```python
  from django.core.mail import EmailMultiAlternatives
  from django.template.loader import render_to_string
  from django.conf import settings

  def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
      reset_url = f"http://localhost:3000/auth/reset-password?token={reset_password_token.key}&email={reset_password_token.user.email}"
      context = {
          'password_reset_url': reset_url,
          'current_year': 2025,
      }
      subject = "Recupera tu contraseña - motivAI"
      from_email = settings.DEFAULT_FROM_EMAIL
      to_email = [reset_password_token.user.email]
      html_content = render_to_string('registration/password_reset_email.html', context)
      msg = EmailMultiAlternatives(subject, html_content, from_email, to_email)
      msg.attach_alternative(html_content, "text/html")
      msg.send()
  ```

### Configuración de email

- En `settings.py` debes tener configurado el backend de email, por ejemplo para Gmail:
  ```python
  EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
  EMAIL_HOST = 'smtp.gmail.com'
  EMAIL_PORT = 587
  EMAIL_HOST_USER = 'tucorreo@gmail.com'
  EMAIL_HOST_PASSWORD = 'tu_app_password'
  EMAIL_USE_TLS = True
  DEFAULT_FROM_EMAIL = 'motivAI <tucorreo@gmail.com>'
  ```

- Para pruebas, puedes usar el backend de consola:
  ```python
  EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
  ```

---

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
  Al crear un plan, se genera automáticamente un cronograma de rutinas con fechas reales, tipo (entrenamiento/descanso) y ejercicios enriquecidos (con imagen/video si existen).
  **Ejemplo de respuesta:**
  ```json
  {
    "success": true,
    "message": "Plan, cronograma y conversación creados correctamente.",
    "data": {
      "plan": {
        "id": 1,
        "usuario": 2,
        "fecha_inicio": "2024-06-03",
        "fecha_fin": null,
        "objetivo": "Ganar músculo",
        ...
        "rutinas": [
          {
            "id": 10,
            "dia": 1,
            "tipo": "entrenamiento",
            "fecha": "2024-06-03",
            "observaciones": null,
            "ejercicios": [
              {
                "id": 1,
                "ejercicio": {
                  "id": 1,
                  "nombre": "Sentadillas",
                  "grupo_muscular": "Piernas",
                  "descripcion": "Ejercicio básico de piernas",
                  "imagen_url": "https://.../sentadillas.jpg",
                  "video_url": "https://.../sentadillas.mp4",
                  "equipo": "Ninguno",
                  "dificultad": "Fácil"
                },
                "repeticiones": 12,
                "series": 3,
                "peso_sugerido": null,
                "descanso_segundos": 60,
                "orden": 1,
                "observaciones": null
              },
              ...
            ]
          },
          {
            "id": 11,
            "dia": 2,
            "tipo": "descanso",
            "fecha": "2024-06-04",
            "observaciones": null,
            "ejercicios": []
          },
          ...
        ]
      },
      "conversation": { ... }
    }
  }
  ```
- **Perfil fitness:**  
  Asociado a cada plan, editable y consultable por el usuario.
- **Conversación:**  
  El flujo conversacional extrae datos y los guarda en el perfil fitness.

## 4. Permisos y Seguridad
- **Acceso a endpoints:**  
  - Usuarios autenticados pueden consultar y modificar solo sus propios datos (planes, rutinas, ejercicios).
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

## 7. Marcar rutina como realizada
- **POST** `/api/plans/rutinas/{id}/realizar/`
- **Permiso:** Autenticado
- **Body (opcional):**
```json
{
  "fecha_realizacion": "2024-06-10"
}
```
- **Respuesta exitosa:**
```json
{
  "success": true,
  "message": "Rutina marcada como realizada.",
  "data": {
    "id": 10,
    "dia": 1,
    "tipo": "entrenamiento",
    "fecha": "2024-06-03",
    "realizada": true,
    "fecha_realizacion": "2024-06-10",
    ...
  }
}
```
- **Errores comunes:**
  - 403: No tienes permiso para modificar esta rutina.
  - 400: La rutina ya fue marcada como realizada.

## Soft delete y filtrado por estado

Los modelos principales (`PlanEntrenamiento`, `Routine`, `Exercise`, `ExerciseRoutine`) incluyen un campo `status`:
- `activo`: el objeto está disponible y visible en los listados por defecto.
- `inactivo`: el objeto ha sido eliminado lógicamente (soft delete) y no aparece en los listados por defecto.

### Eliminación lógica (soft delete)
- Al eliminar un plan, rutina o ejercicio, el campo `status` se marca como `inactivo` en vez de borrarse físicamente.
- El objeto no desaparece de la base de datos y puede ser consultado filtrando por `status=inactivo`.
- Los endpoints de listado filtran por defecto por `status=activo`.
- Solo el dueño (usuario creador) o admin puede eliminar (soft delete) un plan o rutina.
- Cualquier usuario autenticado puede eliminar (soft delete) un ejercicio.

### Filtrado por estado
- Se puede obtener la lista de objetos inactivos usando el parámetro de query `?status=inactivo`.
- Ejemplo: `/api/plans/planentrenamiento/?status=inactivo`

### Checklist de comportamiento esperado
- [x] Eliminar un objeto no lo borra físicamente, solo cambia su `status` a `inactivo`.
- [x] Los listados solo muestran objetos con `status=activo` por defecto.
- [x] Se puede listar los inactivos con `?status=inactivo`.
- [x] Solo el dueño o admin puede eliminar planes/rutinas.
- [x] Los tests automáticos cubren soft delete y filtrado.

### Permisos
- **Planes/Rutinas:** Solo el dueño o admin puede eliminar (soft delete).
- **Ejercicios:** Cualquier usuario autenticado puede eliminar (soft delete).

### Ejemplo de respuesta de listado
```json
{
  "success": true,
  "message": "Listado obtenido correctamente",
  "data": [
    { "id": 1, "objetivo": "Ganar músculo", "status": "activo", ... },
    ...
  ]
}
```
  