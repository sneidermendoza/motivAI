# Guía de Integración Backend-Frontend motivAI

## Estado y Alcance del Backend motivAI

### ¡Backend listo y estable!

El backend de motivAI ha alcanzado un punto de madurez funcional y está completamente preparado para integrarse con el frontend. A continuación, se detalla todo lo que se ha implementado, lo que el frontend puede consumir y las responsabilidades/expectativas para la integración.

---

## ¿Qué ofrece el backend?

### 1. Autenticación y Usuarios
- Registro, login y logout (JWT y social: Google/Facebook).
- Gestión de perfil de usuario: ver y editar datos personales, foto de perfil.
- Cambio de contraseña: endpoint seguro para usuarios autenticados.
- Recuperación de contraseña: endpoint simulado (devuelve token, en producción enviará email).
- Eliminación de cuenta (cumpliendo GDPR).
- Validación y sanitización de archivos subidos (fotos de perfil).

### 2. Sistema Conversacional (Core MVP)
- Flujo conversacional automático: al crear un plan, se inicia una conversación guiada por IA.
- Respuestas abiertas, opción múltiple y numéricas: el backend valida y aclara respuestas ambiguas o incompletas.
- Fallback inteligente: si la respuesta no se entiende, se solicita aclaración al usuario.
- Extracción de información fitness: la IA extrae datos clave de las respuestas del usuario.
- Panel admin para configurar flujos de conversación.

### 3. Planes y Rutinas
- Creación y gestión de planes de entrenamiento: cada usuario puede tener un plan activo y un historial de planes (soft delete).
- Generación de plan por IA: el backend puede generar un plan personalizado usando modelos open source.
- Rutinas diarias y ejercicios: cada plan se desglosa en rutinas y ejercicios, con endpoints para marcar rutinas como realizadas.
- Historial de planes: endpoint para consultar planes inactivos/eliminados lógicamente.

### 4. Ejercicios
- Base de datos de ejercicios: creada por IA o manualmente, con detalles y multimedia.
- Gestión de ejercicios y rutinas: endpoints CRUD y soft delete.

### 5. Progreso
- Registro y visualización de progreso: peso, medidas, fotos, energía, observaciones.
- Gestión de fotos de progreso.

### 6. Notificaciones y Feedback
- Sistema de notificaciones motivacionales: backend listo para generar y enviar notificaciones (falta integración push real).
- Feedback de usuario: los usuarios pueden enviar sugerencias y el admin puede verlas.

### 7. Permisos y Seguridad
- Sistema de roles y permisos: admin, usuario, etc.
- Protección de endpoints sensibles.
- Soft delete en recursos críticos.

### 8. Documentación y Ejemplos
- Swagger/OpenAPI: todos los endpoints documentados con ejemplos reales de request/response.
- README y plan de trabajo: actualizados y claros para onboarding y contribución.

---

## ¿Qué debe hacer el frontend?

### Obligaciones y expectativas:
- Consumir los endpoints REST: el frontend debe interactuar con el backend usando los endpoints documentados.
- Manejo de autenticación JWT: guardar y enviar el token en cada request autenticado.
- Flujo conversacional: mostrar preguntas, enviar respuestas, manejar validaciones y mensajes de aclaración/fallback.
- Visualización y gestión de planes/rutinas: mostrar el plan activo, historial, rutinas diarias y permitir marcar rutinas como realizadas.
- Gestión de progreso: permitir al usuario registrar y visualizar su progreso, incluyendo subida de fotos.
- Notificaciones: mostrar notificaciones motivacionales (el backend ya las genera, falta integración push real en frontend).
- Feedback: permitir enviar sugerencias y mostrar confirmación.
- Gestión de errores y validaciones: mostrar mensajes claros al usuario según las respuestas del backend (por ejemplo, campos faltantes, respuestas ambiguas, errores de autenticación, etc.).
- Soporte para roles: mostrar u ocultar funcionalidades según el rol del usuario (admin/usuario).

### Opcional / Futuro:
- Integración de notificaciones push reales (PWA).
- Gamificación, comunidad, integración con dispositivos externos (ya planificado en el backend para el futuro).

---

## ¿Qué NO debe hacer el frontend?
- No debe implementar lógica de negocio compleja: toda la validación, reglas y flujos están en el backend.
- No debe almacenar datos sensibles localmente (solo el token JWT).
- No debe asumir reglas de negocio no documentadas: siempre consultar la documentación Swagger y el README.

---

## ¿Dónde consultar?
- **Swagger UI**: disponible en `/` del backend para probar y ver ejemplos de todos los endpoints.
- **README**: resumen de endpoints clave y ejemplos.
- **docs/plan_trabajo.md**: estado y prioridades del proyecto.
- **Cualquier duda o endpoint no documentado, consultar al equipo de backend.**

---

## Resumen
El backend está listo, probado y documentado. El frontend solo debe consumir los endpoints, manejar la autenticación y mostrar la información y flujos definidos por el backend.  
¡Cualquier validación, mensaje o flujo especial ya está cubierto y documentado!

---

**¡Listos para avanzar con el frontend! 🚀** 