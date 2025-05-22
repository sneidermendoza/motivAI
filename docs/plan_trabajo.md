# Plan de Trabajo motivAI

Este documento contiene el plan de trabajo detallado, organizado por áreas y tareas, con checklists para marcar el avance del proyecto. Actualiza este archivo conforme avances o completes tareas.

---

## 1. Configuración Inicial
- [x] Configurar entorno virtual y dependencias (Python, Node.js)
- [x] Inicializar proyecto Django (backend)
- [x] Inicializar proyecto Next.js (frontend)
- [x] Configurar base de datos MariaDB/MySQL
- [x] Crear y mantener `.gitignore` adecuado
- [x] Documentar instalación y despliegue local

## 2. Modelado y Backend
### Usuarios
- [x] Modelo de usuario personalizado (campos personales, foto, status)
- [x] Autenticación email/contraseña
- [x] Autenticación social (Google/Facebook)
- [x] Endpoints CRUD de usuario
- [x] Gestión de foto de perfil
- [ ] Endpoint para cambiar contraseña y recuperación de cuenta
- [ ] Endpoint para eliminar cuenta (GDPR)
- [ ] Validación y sanitización de archivos subidos (fotos)
- [ ] Limitar tamaño y tipo de archivos permitidos
- [ ] Políticas de privacidad y manejo de datos personales

### Sistema Conversacional
- [ ] Modelo de conversación (estado, contexto, historial)
- [ ] Modelo de preguntas (tipo: abierta, opción múltiple, numérica)
- [ ] Modelo de respuestas de usuario
- [ ] Endpoint de conversación (/api/conversation/)
- [ ] Sistema de extracción de información de respuestas abiertas
- [ ] Sistema de validación y aclaración de respuestas
- [ ] Panel admin para configurar flujo de conversación
- [ ] Sistema de guardado de contexto de conversación
- [ ] Endpoint para reiniciar conversación
- [ ] Sistema de fallback para respuestas no entendidas

### Planes y Rutinas
- [ ] Modelo de plan de entrenamiento (un plan activo por usuario)
- [ ] Endpoint para generación de plan por IA
- [ ] Endpoint para modificar/adaptar plan
- [ ] Historial de planes (eliminación lógica)
- [ ] Modelo de rutina diaria (cronograma)
- [ ] Modelo de ejercicios en rutina (relación rutina-ejercicio)
- [ ] Endpoint para marcar rutina como realizada

### Ejercicios
- [ ] Modelo de ejercicio (creado por IA)
- [ ] Base de datos inicial vacía (la IA los crea)

### Progreso
- [ ] Modelo de progreso y medidas (peso, medidas, foto)
- [ ] Gestión de fotos de progreso
- [ ] Visualización de progreso y reportes

### Notificaciones y Feedback
- [ ] Implementar notificaciones push
- [ ] Endpoint para mensajes motivacionales (IA)
- [ ] Configuración de frecuencia por usuario
- [ ] Modelo de feedback y sugerencias
- [ ] Endpoint para enviar feedback
- [ ] Panel admin para ver feedback

## 3. Frontend
- [ ] Estructura base Next.js + Tailwind
- [ ] Registro/Login de usuario
- [ ] Interfaz conversacional (chat-like)
- [ ] Componente de chat con IA
- [ ] Visualización de progreso de conversación
- [ ] Visualización y seguimiento de plan/rutina
- [ ] Registro de progreso y subida de fotos
- [ ] Notificaciones push en PWA
- [ ] Panel de feedback y sugerencias
- [ ] Soporte para varios idiomas (i18n)
- [ ] Accesibilidad (contraste, navegación teclado, ARIA)

## 4. Integración IA
- [ ] Integrar modelo open source local (GPT4All, Llama.cpp, etc.)
- [ ] Sistema de procesamiento de lenguaje natural
- [ ] Sistema de extracción de información de respuestas
- [ ] Sistema de generación de preguntas contextuales
- [ ] Sistema de validación de respuestas
- [ ] Documentar prompts y lógica de interacción
- [ ] Sistema de fallback para respuestas no entendidas

## 5. Documentación y Organización
- [ ] Mantener actualizado el backlog (`backlog/motivAI-backlog.csv`)
- [ ] Actualizar README y docs/arquitectura.md
- [ ] Agregar diagrama de flujo conversacional
- [ ] Agregar diagrama de modelo de datos
- [ ] Documentar endpoints principales y ejemplos de uso
- [ ] Crear guía de contribución
- [ ] Separar settings de producción y desarrollo
- [ ] Pruebas automáticas (unitarias y de integración)
- [ ] CI/CD básico (GitHub Actions)
- [ ] Logs y monitoreo básico

## 6. Mejoras Futuras (no MVP)
- [ ] Gamificación (logros, medallas)
- [ ] Integración con dispositivos externos (wearables, apps)
- [ ] Planes de nutrición
- [ ] Comunidad/foro
- [ ] Endpoint para exportar datos del usuario (CSV/JSON)
- [ ] Webhooks para integración con apps externas

---

**¿Cómo marcar tareas?**
- Cambia `[ ]` por `[x]` cuando completes una tarea.
- Agrega comentarios o responsables si es necesario.

**¡Actualiza este archivo con cada avance!**

![MVP Progress](https://img.shields.io/badge/MVP%20Progress-50%25-yellow) 
