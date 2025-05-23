# Arquitectura y Estructura de Carpetas motivAI

## Estructura General
```
motivAI/
├── README.md                # Documentación principal
├── docs/                    # Documentación adicional y recursos
│   ├── branding.md          # Branding, paleta de colores, logo, favicon
│   ├── arquitectura.md      # Arquitectura y estructura de carpetas
│   ├── politicas.md         # Políticas de privacidad y términos (borrador)
│   └── enlaces.md           # Enlaces útiles (incluyendo Google Sheets)
├── backlog/                 # Backlog y gestión de tareas
│   └── motivAI-backlog.csv  # Backlog inicial (para Google Sheets)
├── logo/                    # Recursos visuales (logo, favicon)
├── backend/                 # Proyecto Django (backend)
└── frontend/                # Proyecto Next.js (frontend)
```

## Diagrama de Flujo Conversacional

```ascii
+-------------------+
|   Registro/Login  |
+-------------------+
          |
          v
+-------------------+
|  Inicio Conversación |
+-------------------+
          |
          v
+-------------------+
|  Procesamiento IA  |
+-------------------+
          |
          v
+-------------------+
|  Extracción Datos  |
+-------------------+
          |
          v
+-------------------+
|  Validación/Clarificación |
+-------------------+
          |
          v
+-------------------+
|  Generar Plan     |
+-------------------+
          |
          v
+-------------------+
|  Rutina Diaria    |
+-------------------+
          |
          v
+-------------------+
|  Marcar Progreso  |
+-------------------+
          |
          v
+-------------------+
|  Feedback/Notifs  |
+-------------------+
```

## Sistema Conversacional

### Flujo de Conversación
1. **Inicio**: Usuario se registra/inicia sesión
2. **Conversación Inicial**:
   - IA pregunta sobre motivación y objetivos
   - Usuario responde libremente
   - IA extrae información relevante
3. **Validación y Clarificación**:
   - Si la respuesta no es clara, IA pide aclaración
   - Sistema de fallback para respuestas no entendidas
4. **Recopilación de Datos**:
   - Edad, peso, condiciones médicas, etc.
   - Respuestas abiertas procesadas por IA
   - Validación de datos críticos
5. **Generación de Plan**:
   - IA usa datos recopilados para crear plan
   - Plan se adapta a respuestas y contexto

### Componentes del Sistema
- **ConversationManager**: Gestiona estado y contexto
- **NLPProcessor**: Procesa respuestas abiertas
- **DataExtractor**: Extrae información relevante
- **ValidationSystem**: Valida y clarifica respuestas
- **ContextManager**: Mantiene contexto de conversación

## Modelo de Datos (Resumen)
- Usuario: datos personales, foto, autenticación
- Conversacion: estado, contexto, historial
- Pregunta: tipo (abierta, opción múltiple, numérica)
- Respuesta: texto, datos extraídos, validación
- PlanEntrenamiento: un plan activo por usuario, historial lógico
- Rutina: cronograma diario del plan
- Ejercicio: base de datos creada por IA
- EjercicioRutina: ejercicios asignados a cada rutina
- Progreso: registro de peso, medidas, fotos, energía, observaciones
- Notificación: push y motivacionales
- Feedback: sugerencias, reportes y opiniones de usuarios (anónimos o autenticados), accesible por admin para mejora continua.
- (Futuro) Logros, integración dispositivos, nutrición

## Explicación de Carpetas
- **docs/**: Toda la documentación técnica, branding, políticas y enlaces.
- **backlog/**: Archivo CSV con el backlog de tareas, para importar a Google Sheets.
- **logo/**: Archivos SVG del logo y favicon.
- **backend/**: Proyecto Django, con apps separadas por dominio:
  - users: gestión de usuarios
  - conversation: sistema conversacional
  - plans: planes y rutinas
  - progress: seguimiento de progreso
  - notifications: notificaciones y feedback
  - ai: integración con modelos de IA
- **frontend/**: Proyecto Next.js, estructura modular y escalable.

## Recomendaciones
- Mantener la documentación y el backlog actualizados.
- Documentar cada endpoint, modelo y funcionalidad.
- Usar control de versiones (Git) y ramas para nuevas features.
- Implementar pruebas para el sistema conversacional.
- Monitorear calidad de extracción de datos.
- Mantener logs de conversaciones para mejora continua.

## Endpoints y Accesos (actualizado)

| Endpoint | Método | Descripción | Quién puede usarlo |
|----------|--------|-------------|--------------------|
| /api/users/register/ | POST | Registro de usuario | Público |
| /api/users/login/ | POST | Login de usuario | Público |
| /api/users/ | GET, PUT, PATCH | Ver/editar perfil propio | Usuario autenticado |
| /api/plans/planentrenamiento/ | GET, POST | Listar/crear planes de entrenamiento | Usuario autenticado (solo ve/crea los suyos) |
| /api/plans/planentrenamiento/{id}/ | GET, PUT, PATCH, DELETE | Ver/editar/eliminar plan | Solo admin o dueño |
| /api/plans/fitnessprofile/ | GET | Listar perfiles fitness | Admin ve todos, usuario solo los suyos |
| /api/plans/fitnessprofile/{id}/ | GET, PUT, PATCH, DELETE | Ver/editar/eliminar perfil fitness | Admin todo, usuario solo ver los suyos |
| /api/conversation/ | GET, POST | Listar/iniciar conversación | Usuario autenticado |
| /api/conversation/{id}/respond/ | POST | Responder pregunta en conversación | Usuario autenticado |
| /api/conversation/question/ | GET | Listar preguntas activas | Usuario autenticado |
| /api/conversation/state/ | GET | Listar estados de conversación | Usuario autenticado |
| /api/feedback/ | GET, POST | Ver/enviar feedback | Usuario autenticado |
| /api/notifications/ | GET | Ver notificaciones | Usuario autenticado |
| /admin/ | web | Panel de administración | Solo admin |

**Notas:**
- Los endpoints de edición/eliminación de recursos sensibles solo pueden ser usados por admin o el dueño del recurso.
- Los endpoints de solo lectura pueden ser accedidos por usuarios autenticados, salvo que se indique lo contrario.
- El sistema de permisos se implementa con clases de permisos personalizadas y/o DRF.

## Sistema de Permisos y Roles

- Se implementa un sistema de permisos basado en roles (admin, usuario) usando las clases de permisos de Django REST Framework.
- El usuario admin puede ver, crear, editar y eliminar cualquier recurso.
- El usuario normal solo puede ver y modificar sus propios recursos (planes, perfiles fitness, conversaciones, etc.).
- Los endpoints sensibles (eliminación, edición de otros usuarios, etc.) están protegidos para que solo el admin pueda acceder.
- El sistema de permisos se aplica en los viewsets y se documenta en cada endpoint.
- A futuro, se puede extender para roles adicionales o permisos más granulares.

**Implementación:**
- Se usan clases como `IsAdminOrReadOnly` y métodos `get_queryset` personalizados para filtrar recursos según el usuario.
- Se recomienda mantener y actualizar esta sección conforme se agreguen nuevos endpoints o roles.

## Ejemplos y Documentación de Endpoints Clave

### Registro de usuario
- **POST** `/api/users/register/`
- **Body:**
```json
{
  "username": "usuario1",
  "email": "usuario1@correo.com",
  "password": "Password123",
  "password2": "Password123"
}
```
- **Campos requeridos:** username, email, password, password2
- **Respuesta:** Usuario creado

### Login
- **POST** `/api/users/login/`
- **Body:**
```json
{
  "email": "usuario1@correo.com",
  "password": "Password123"
}
```
- **Campos requeridos:** email, password
- **Respuesta:** Token o sesión

### Crear plan de entrenamiento
- **POST** `/api/plans/planentrenamiento/`
- **Body:**
```json
{
  "fecha_inicio": "2024-05-22",
  "objetivo": "Bajar de peso"
}
```
- **Campos requeridos:** fecha_inicio, objetivo
- **Respuesta:**
```json
{
  "plan": { ... },
  "conversation": { "id": 1, ... }
}
```

### Responder pregunta en conversación
- **POST** `/api/conversation/{id}/respond/`
- **Body:**
```json
{
  "conversation_id": 1,
  "question_id": 1,
  "raw_text": "Quiero sentirme con más energía"
}
```
- **Campos requeridos:** conversation_id, question_id, raw_text
- **Respuesta:** Estado actualizado de la conversación

### Consultar preguntas activas
- **GET** `/api/conversation/question/`
- **Respuesta:** Lista de preguntas

### Consultar perfil fitness
- **GET** `/api/plans/fitnessprofile/`
- **Respuesta:** Lista de perfiles fitness del usuario

---

**Notas:**
- Todos los endpoints requieren autenticación salvo registro/login.
- Los campos requeridos están marcados; los opcionales pueden omitirse.
- Para endpoints personalizados, consulta Swagger para ejemplos y descripciones. 