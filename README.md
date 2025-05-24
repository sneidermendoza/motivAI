# motivAI

Tu motivación, potenciada por IA

---

## Visión
Aplicación web para crear, seguir y adaptar planes de entrenamiento personalizados, con ayuda de inteligencia artificial. Pensada para quienes buscan salud, motivación y progreso, especialmente quienes trabajan muchas horas sentados.

## Stack Tecnológico
- **Backend:** Django (Python)
- **Frontend:** Next.js (PWA, React)
- **Base de datos:** MariaDB/MySQL (desarrollo), migrable a PostgreSQL
- **IA:** Modelos open source (GPT4All, Llama.cpp, HuggingFace)
- **Notificaciones:** Push API (PWA)

## Estructura del Proyecto
```
motivAI/
├── README.md
├── docs/
├── backlog/
├── logo/
├── backend/
│   ├── manage.py
│   ├── backend/         # Configuración principal de Django (settings.py, urls.py, etc.)
│   ├── users/           # App de usuarios (incluye modelos de gamificación)
│   ├── plans/
│   ├── progress/
│   ├── notifications/
│   ├── feedback/
│   └── ... (otras apps)
└── frontend/
```

## Login Social (Google y Facebook)
Para iniciar sesión con Google o Facebook desde el frontend, redirige al usuario a las siguientes URLs:

- **Login con Google:**
  ```
  http://localhost:8000/auth/login/google-oauth2/
  ```
- **Login con Facebook:**
  ```
  http://localhost:8000/auth/login/facebook/
  ```

> **Descripción:**
> Estas URLs inician el flujo de autenticación social. El usuario será redirigido a Google o Facebook para autorizar el acceso y, tras aceptar, volverá a la app con la sesión iniciada. El backend maneja la creación y autenticación del usuario automáticamente.

Si tienes ambientes de producción, recuerda actualizar las URLs según el dominio correspondiente.

## Plan de Trabajo
El plan de trabajo y las prioridades del proyecto están documentados en:
- [`docs/plan_trabajo.md`](docs/plan_trabajo.md) (checklist editable y seguimiento)
- [`backlog/motivAI-backlog.csv`](backlog/motivAI-backlog.csv) (tareas y prioridades)

Aquí encontrarás todas las tareas, subtareas y mejoras futuras, ordenadas por prioridad y área.

- **Tareas principales:** Desarrollo de modelos, endpoints, integración IA, seguimiento de usuario, notificaciones, feedback y documentación.
- **Mejoras futuras:** Gamificación, integración con dispositivos externos, planes de nutrición, comunidad.

Consulta estos archivos para ver el estado y responsables de cada tarea.

## Cómo contribuir
1. Revisa el backlog, el plan de trabajo y el README para entender el estado actual del proyecto.
2. Consulta la documentación técnica en `docs/`.
3. Si quieres colaborar, abre un issue o haz un fork y pull request.
4. Mantén la documentación y el backlog actualizados con cada cambio.

## Branding
- Nombre: **motivAI**
- Paleta de colores, logo y favicon en `docs/branding.md` y `logo/`

## Enlaces útiles
- [Plan de trabajo (checklist)](docs/plan_trabajo.md)
- [Backlog de tareas](backlog/motivAI-backlog.csv)
- [Documentación técnica](docs/arquitectura.md)

## Endpoints útiles

### Cambio de contraseña
- `POST /api/users/profile/change-password/`
  - Requiere autenticación.
  - Body: `{ "old_password": "actual", "new_password": "nueva", "new_password2": "nueva" }`
  - Cambia la contraseña del usuario.

### Recuperación de contraseña
- `POST /api/users/profile/reset-password/`
  - Body: `{ "email": "usuario@correo.com" }`
  - Simula el envío de un token de recuperación (en producción se enviará por correo electrónico).

### Historial de planes
- `GET /api/plans/planentrenamiento/historial/`
  - Requiere autenticación.
  - Devuelve los planes inactivos (eliminados lógicamente) del usuario. Los administradores ven todos los planes inactivos.

> **Nota:** El endpoint de recuperación de contraseña actualmente solo simula el flujo y devuelve el token en la respuesta. En producción, este token se enviará por correo electrónico al usuario.

---

> Proyecto personal, código abierto y en constante evolución. ¡Súmate o aporta ideas!

- Modelos principales: Usuario, Plan, Rutina, Ejercicio, Progreso, Notificación, Feedback, PreguntaPlan, RespuestaPlan
- Gamificación: Logro, UsuarioLogro 


implementar test,
implementar permisos y actualizar la documentacion y el archivo donde estan los datos que vana poblar la bd cuanda la corra desde 0
actualizar y marcar en el plan de trabjo las tareas hechas
documentar en swagger los enpoint como se viene haciendo con ejempl;os reales 
documentar los  enpoint
si es nececsario agregar algo al readme 
si se me pasa algo por favor revisa lo que tienes que hacer y lo haces 
por ultimo corre los test completos a ver si todo sigue igual aun despues de los cambios realizados
