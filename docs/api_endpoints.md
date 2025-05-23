# motivAI – API Endpoints Documentation

## Tabla de Contenidos
- [Usuarios y Autenticación](#usuarios-y-autenticación)
- [Roles y Permisos](#roles-y-permisos)
- [Planes de Entrenamiento](#planes-de-entrenamiento)
- [Generación de Plan por IA (Groq)](#generación-de-plan-por-ia-groq)
- [Conversación](#conversación)
- [Feedback y Notificaciones](#feedback-y-notificaciones)
- [Resumen de Permisos por Endpoint](#resumen-de-permisos-por-endpoint)
- [Progreso del usuario](#progreso-del-usuario)

---

## Usuarios y Autenticación

### Registro
- **POST** `/api/users/register/`
- **Permiso:** Público
- **Body:**
```json
{
  "username": "usuario1",
  "email": "usuario1@example.com",
  "password": "Testpass123",
  "password2": "Testpass123"
}
```
- **Respuesta exitosa:**
```json
{
  "success": true,
  "message": "Usuario registrado correctamente.",
  "data": { ... }
}
```

### Login (JWT)
- **POST** `/api/token/`
- **Permiso:** Público
- **Body:**
```json
{
  "username": "usuario1",
  "password": "Testpass123"
}
```
- **Respuesta exitosa:**
```json
{
  "refresh": "...",
  "access": "..."
}
```

### Logout
- **POST** `/api/users/logout/`
- **Permiso:** Autenticado
- **Body:**
```json
{
  "refresh": "<refresh_token>"
}
```

### Perfil de usuario
- **GET** `/api/users/profile/me/`
- **Permiso:** Autenticado
- **Respuesta:**
```json
{
  "id": 1,
  "username": "usuario1",
  "email": "usuario1@example.com",
  "roles": ["usuario"]
}
```

---

## Roles y Permisos

### Listar roles
- **GET** `/api/users/roles/`
- **Permiso:** Autenticado

### Listar permisos
- **GET** `/api/users/permissions/`
- **Permiso:** Autenticado

---

## Planes de Entrenamiento

### CRUD de planes
- **GET/POST/PUT/DELETE** `/api/plans/planentrenamiento/`
- **Permiso:**
  - GET/POST: Autenticado (usuarios solo ven/crean sus planes, admin ve todos)
  - PUT/DELETE: Solo dueño o admin
- **Body (POST):**
```json
{
  "objetivo": "Ganar músculo",
  "fecha_inicio": "2024-06-03",
  "dias_entrenar": 3,
  "dias_semana_entrenar": [0,2,4]
}
```
- **Respuesta exitosa:**
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

### Generación de plan por IA (Groq)
- **POST** `/api/plans/planentrenamiento/generate/`
- **Permiso:** Autenticado
- **Body:**
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
- **Respuesta exitosa:**
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

### Marcar rutina como realizada
- **POST** `/api/plans/rutinas/{id}/realizar/`
- **Permiso:** Autenticado (solo dueño del plan o admin)
- **Body (opcional):**
```json
{
  "fecha_realizacion": "2024-06-10"  // Si no se envía, se usa la fecha actual
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

---

## Conversación

### Listar conversaciones
- **GET** `/api/conversation/conversations/`
- **Permiso:** Autenticado (usuario ve solo sus conversaciones)

### Crear conversación
- **POST** `/api/conversation/conversations/`
- **Permiso:** Autenticado

### Responder en conversación
- **POST** `/api/conversation/conversations/{id}/respond/`
- **Permiso:** Autenticado (solo dueño)
- **Body:**
```json
{
  "conversation_id": 1,
  "question_id": 2,
  "raw_text": "Mi motivación es mejorar mi salud."
}
```

### Reiniciar conversación
- **POST** `/api/conversation/conversations/{id}/reset/`
- **Permiso:** Autenticado (solo dueño)

### Extracción y validación conversacional (IA)
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

---

## Feedback y Notificaciones

### Enviar feedback
- **POST** `/api/feedback/feedback/` — Enviar feedback (anónimo o autenticado)
- **GET** `/api/feedback/feedback/` — Listar feedbacks (solo admin)

**Permisos:**
- POST: cualquiera (anónimo o autenticado)
- GET: solo admin

**Ejemplo de request (POST):**
```json
{
  "tipo": "sugerencia",
  "mensaje": "Me gusta la app!"
}
```

**Ejemplo de response (GET):**
```json
{
  "id": 1,
  "usuario": "testuser",
  "fecha": "2024-06-10T12:00:00Z",
  "tipo": "sugerencia",
  "mensaje": "Me gusta la app!",
  "status": "pendiente"
}
```

### Notificaciones (próximamente)
- **GET** `/api/notifications/notification/`
- **Permiso:** Autenticado (solo propias), admin ve todas

---

## Resumen de Permisos por Endpoint

| Endpoint                                         | Usuario | Admin |
|--------------------------------------------------|---------|-------|
| /api/users/register/                             |   ✔     |   ✔   |
| /api/token/                                      |   ✔     |   ✔   |
| /api/users/logout/                               |   ✔     |   ✔   |
| /api/users/profile/me/                           |   ✔     |   ✔   |
| /api/users/roles/                                |   ✔     |   ✔   |
| /api/users/permissions/                          |   ✔     |   ✔   |
| /api/plans/planentrenamiento/                    |   ✔     |   ✔   |
| /api/plans/planentrenamiento/generate/           |   ✔     |   ✔   |
| /api/conversation/conversations/                 |   ✔     |   ✔   |
| /api/conversation/conversations/{id}/respond/    |   ✔     |   ✔   |
| /api/conversation/conversations/{id}/reset/      |   ✔     |   ✔   |
| /api/conversation/extract/                       |   ✔     |   ✔   |
| /api/feedback/feedback/ (POST)                   |   ✔     |   ✔   |
| /api/feedback/feedback/ (GET)                    |         |   ✔   |
| /api/notifications/notification/                 |   ✔     |   ✔   |

- ✔ = acceso permitido
- Usuario: autenticado, solo accede a sus propios datos
- Admin: acceso total

---

**Actualizado a la fecha: 2024-05-23** 

# Documentación de Endpoints motivAI

## Autenticación

### Obtener Token JWT
```http
POST /api/token/
Content-Type: application/json

{
    "username": "usuario@ejemplo.com",
    "password": "contraseña123"
}
```

Respuesta:
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## Usuarios

### Registro
```http
POST /api/users/register/
Content-Type: application/json

{
    "email": "nuevo@ejemplo.com",
    "password": "contraseña123",
    "first_name": "Juan",
    "last_name": "Pérez",
    "role": "user"
}
```

### Perfil
```http
GET /api/users/profile/
Authorization: Bearer <token>
```

## Planes

### Crear Plan
```http
POST /api/plans/
Authorization: Bearer <token>
Content-Type: application/json

{
    "nombre": "Plan de pérdida de peso",
    "objetivo": "perder_peso",
    "fecha_inicio": "2024-03-20",
    "fecha_fin": "2024-06-20",
    "dias_entrenar": 3,
    "dias_semana_entrenar": [0, 2, 4]
}
```

### Generar Plan con IA
```http
POST /api/plans/generate/
Authorization: Bearer <token>
Content-Type: application/json

{
    "edad": 28,
    "peso": 80,
    "altura": 175,
    "objetivo": "perder_peso",
    "nivel": "principiante",
    "restricciones": ["rodilla_derecha"],
    "preferencias": ["cardio", "fuerza"]
}
```

## Rutinas

### Marcar Rutina como Realizada
```http
POST /api/routines/{id}/realizar/
Authorization: Bearer <token>
Content-Type: application/json

{
    "fecha_realizacion": "2024-03-20"
}
```

## Conversación

### Extraer Información
```http
POST /api/conversation/extract/
Authorization: Bearer <token>
Content-Type: application/json

{
    "text": "Quiero perder 5kg en 3 meses, tengo 28 años, peso 80kg y mido 175cm. Soy principiante y tengo una lesión en la rodilla derecha."
}
```

Respuesta:
```json
{
    "edad": 28,
    "peso": 80,
    "altura": 175,
    "objetivo": "perder_peso",
    "meta": "5kg en 3 meses",
    "nivel": "principiante",
    "restricciones": ["rodilla_derecha"]
}
```

## Códigos de Error Comunes

- 400: Bad Request - Datos inválidos
- 401: Unauthorized - Token inválido o expirado
- 403: Forbidden - No tiene permisos
- 404: Not Found - Recurso no encontrado
- 500: Internal Server Error - Error del servidor

## Ejemplos de Uso Común

### Flujo de Creación de Plan
1. Registro/Login
2. Extracción de información conversacional
3. Generación de plan con IA
4. Creación de plan con cronograma
5. Asignación de rutinas y ejercicios

### Flujo de Seguimiento
1. Consulta de plan activo
2. Visualización de rutinas diarias
3. Marcado de rutinas como realizadas
4. Actualización de progreso 

### Progreso del usuario
- **GET** `/api/progress/progreso/` — Lista todos los registros del usuario autenticado (o todos si es admin)
- **POST** `/api/progress/progreso/` — Crea un nuevo registro de progreso (foto opcional)
- **GET** `/api/progress/progreso/{id}/` — Detalle de un registro de progreso
- **PUT/PATCH** `/api/progress/progreso/{id}/` — Actualiza un registro de progreso
- **DELETE** `/api/progress/progreso/{id}/` — Elimina un registro de progreso

**Permisos:** Solo el dueño o admin puede ver/modificar/eliminar cada registro.

**Ejemplo de request (POST):**
```json
{
  "peso": 70.5,
  "medidas": {"cintura": 80, "pecho": 95},
  "imc": 22.5,
  "energia": "Alta",
  "observaciones": "Me siento bien",
  "foto_progreso": "(archivo imagen opcional)"
}
```

**Ejemplo de response (GET):**
```json
{
  "id": 1,
  "usuario": 5,
  "fecha": "2024-06-10",
  "peso": 70.5,
  "medidas": {"cintura": 80, "pecho": 95},
  "imc": 22.5,
  "energia": "Alta",
  "observaciones": "Me siento bien",
  "foto_progreso": "/media/progress_photos/ejemplo.jpg"
}
``` 