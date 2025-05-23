# motivAI – API Endpoints Documentation

## Tabla de Contenidos
- [Usuarios y Autenticación](#usuarios-y-autenticación)
- [Roles y Permisos](#roles-y-permisos)
- [Planes de Entrenamiento](#planes-de-entrenamiento)
- [Generación de Plan por IA (Groq)](#generación-de-plan-por-ia-groq)
- [Conversación](#conversación)
- [Feedback y Notificaciones](#feedback-y-notificaciones)
- [Resumen de Permisos por Endpoint](#resumen-de-permisos-por-endpoint)

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
- **POST** `/api/feedback/feedback/`
- **Permiso:** Autenticado

### Listar feedback (admin)
- **GET** `/api/feedback/feedback/`
- **Permiso:** Solo admin

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