# Plan de Trabajo motivAI

Este documento contiene el plan de trabajo detallado, organizado por áreas y tareas, con checklists para marcar el avance del proyecto. Actualiza este archivo conforme avances o completes tareas.

---

## 1. Configuración Inicial
- [x] Configurar entorno virtual y dependencias (Python, Node.js)  # Base para todo el desarrollo
- [x] Inicializar proyecto Django (backend)  # Estructura backend
- [x] Inicializar proyecto Next.js (frontend)  # Estructura frontend
- [x] Configurar base de datos MariaDB/MySQL  # Persistencia de datos
- [x] Crear y mantener `.gitignore` adecuado  # Buenas prácticas
- [x] Documentar instalación y despliegue local  # Facilita onboarding

## 2. Usuarios y Autenticación
- [x] Modelo de usuario personalizado (campos personales, foto, status)  # Identidad y perfil
- [x] Autenticación email/contraseña  # Acceso seguro
- [x] Autenticación social (Google/Facebook)  # Acceso rápido
- [x] Endpoints CRUD de usuario  # Gestión de usuarios
- [x] Gestión de foto de perfil  # Personalización
- [x] Endpoint para cambiar contraseña y recuperación de cuenta  # Seguridad y usabilidad
- [x] Endpoint para eliminar cuenta (GDPR)  # Cumplimiento legal
- [x] Validación y sanitización de archivos subidos (fotos)  # Seguridad
- [x] Limitar tamaño y tipo de archivos permitidos  # Seguridad
- [x] Políticas de privacidad y manejo de datos personales  # Legal

## 3. Sistema Conversacional (Core MVP)
- [x] Modelo de conversación (estado, contexto, historial)  # Base para interacción IA
- [x] Modelo de preguntas (tipo: abierta, opción múltiple, numérica)  # Estructura de diálogo
- [x] Modelo de respuestas de usuario  # Registro de interacción
- [x] Endpoint de conversación (/api/conversation/)  # API para frontend
- [x] Sistema de guardado de contexto de conversación  # Persistencia de la conversación
- [x] Endpoint para reiniciar conversación  # UX: empezar de cero
- [x] Seed/fixture de preguntas iniciales  # Preguntas humanas y relevantes cargadas
- [x] Documentación y ejemplos claros en Swagger y Markdown  # Facilita integración
- [x] Endpoint de responder pregunta bien documentado y funcional
- [x] Flujo conversacional automático al crear plan (conversación ligada a plan)
- [x] Sistema de extracción de información de respuestas abiertas (conversacional/IA)
- [x] Validación y aclaración de respuestas ambiguas o incompletas
- [x] Panel admin para configurar flujo de conversación
- [x] Sistema de validación y aclaración de respuestas  # Mejora la calidad de los datos para la IA
- [x] Sistema de fallback para respuestas no entendidas  # UX: manejo de errores conversacionales

## 4. Planes y Rutinas (Core MVP)
- [x] Modelo de plan de entrenamiento (un plan activo por usuario)  # Estructura para almacenar el plan generado
- [x] Endpoint para crear plan y devolver conversación asociada
- [x] Asociación automática de conversación al crear plan
- [x] Modelo UserFitnessProfile para datos fitness ligados a plan
- [x] Endpoint para consultar perfiles fitness (solo propios o todos si admin)
- [x] Endpoint para generación de plan por IA  # Aquí se integra la IA, usando la info extraída
- [x] Modelo de rutina diaria (cronograma)  # Desglose del plan en acciones diarias
- [x] Modelo de ejercicios en rutina (relación rutina-ejercicio)  # Detalle de cada rutina
- [x] Generación automática de cronograma y ejercicios enriquecidos al crear plan
- [x] Tests automáticos y documentación de cronograma y ejercicios
- [x] Endpoint para marcar rutina como realizada  # Seguimiento del usuario
- [x] Historial de planes (eliminación lógica)  # Permite ver evolución
- [x] Endpoint para modificar/adaptar plan  # Flexibilidad para el usuario

## 5. Ejercicios (Core MVP)
- [x] Modelo de ejercicio (creado por IA o manual)  # Base de datos de ejercicios, necesario para rutinas
- [ ] Base de datos inicial vacía (la IA los crea)  # Se poblará dinámicamente

## 6. Progreso (Core MVP)
- [x] Modelo de progreso y medidas (peso, medidas, foto)  # Seguimiento de resultados
- [x] Gestión de fotos de progreso  # Motivación visual
- [x] Visualización de progreso y reportes  # Feedback al usuario (endpoints listos, visualización depende del frontend)

## 7. Notificaciones y Feedback (Core MVP)
- [x] Modelo de feedback y sugerencias  # Mejorar producto
- [x] Endpoint para enviar feedback  # Recoger opiniones
- [x] Panel admin para ver feedback  # Gestión interna (GET solo admin)
- [x] Implementar sistema de notificaciones motivacionales (backend + Celery + documentación)
- [ ] Endpoint para mensajes motivacionales (IA)  # Mantener motivación
- [ ] Implementar notificaciones push  # Engagement
- [x] Configuración de frecuencia por usuario  # Personalización

## 8. Frontend (Core MVP)
- [ ] Estructura base Next.js + Tailwind  # Base visual
- [ ] Registro/Login de usuario  # Acceso
- [ ] Interfaz conversacional (chat-like)  # Experiencia principal
- [ ] Componente de chat con IA  # Interacción con backend
- [ ] Visualización de progreso de conversación  # UX
- [ ] Visualización y seguimiento de plan/rutina  # UX
- [ ] Registro de progreso y subida de fotos  # Seguimiento
- [ ] Notificaciones push en PWA  # Engagement
- [ ] Panel de feedback y sugerencias  # UX
- [ ] Soporte para varios idiomas (i18n)  # Accesibilidad
- [ ] Accesibilidad (contraste, navegación teclado, ARIA)  # Inclusión

## 9. Integración IA (Core MVP)
- [x] Integrar modelo open source local (GPT4All, Llama.cpp, etc.)  # Motor IA (SIGUIENTE tras endpoints de generación de plan)
- [x] Sistema de procesamiento de lenguaje natural  # Entender respuestas abiertas
- [x] Sistema de extracción de información de respuestas  # Ya cubierto arriba
- [x] Sistema de generación de preguntas contextuales  # Conversación más natural
- [x] Sistema de validación de respuestas  # Mejorar calidad
- [x] Documentar prompts y lógica de interacción  # Mantenibilidad
- [x] Sistema de fallback para respuestas no entendidas  # UX

## 10. Documentación y Organización
- [x] Mantener actualizado el backlog (`backlog/motivAI-backlog.csv`)  # Organización
- [x] Actualizar README y docs/arquitectura.md  # Documentación
- [x] Agregar diagrama de flujo conversacional  # Visualización
- [x] Agregar diagrama de modelo de datos  # Visualización
- [x] Documentar endpoints principales y ejemplos de uso  # Facilita integración
- [ ] Crear guía de contribución  # Comunidad
- [ ] Separar settings de producción y desarrollo  # Buenas prácticas
- [x] Pruebas automáticas (unitarias y de integración)  # Calidad
- [ ] CI/CD básico (GitHub Actions)  # Automatización
- [ ] Logs y monitoreo básico  # Mantenimiento

## 11. Permisos y Roles (nuevo)
- [x] Implementar sistema de permisos extendido y roles personalizados (admin, usuario, empleado, coach, etc.)
- [x] Documentar lógica de permisos y ejemplos de uso
- [x] Proteger endpoints sensibles según rol
- [x] Agregar tests de permisos y acceso
- [x] Crear documentación detallada de permisos por endpoint

## 12. Documentación de API (nuevo)
- [x] Documentar permisos por endpoint
- [x] Agregar ejemplos reales en Swagger/OpenAPI
- [x] Documentar flujos de uso comunes
- [x] Agregar ejemplos de request/response
- [x] Documentar códigos de error y manejo

## 13. Mejoras Futuras (no MVP)
- [ ] Gamificación (logros, medallas)
- [ ] Integración con dispositivos externos (wearables, apps)
- [ ] Planes de nutrición
- [ ] Comunidad/foro
- [ ] Endpoint para exportar datos del usuario (CSV/JSON)
- [ ] Webhooks para integración con apps externas

## Tareas completadas
- [x] Extracción y validación conversacional con IA (Groq)
- [x] Endpoint /api/conversation/extract/ implementado y documentado
- [x] Permisos y respuestas claras
- [x] Tests automáticos para extracción conversacional
- [x] Limpieza de historial y push seguro
- [x] Documentación de permisos por endpoint
- [x] Implementación de roles y permisos personalizados
- [x] Tests automáticos para progreso y MVP flow
- [x] Ejemplos claros en Swagger/OpenAPI para progreso
- [x] Corrección de creación de conversación (user asignado automáticamente)
- [x] Actualización de documentación Swagger con ejemplos reales
- [x] Documentación de flujos de uso comunes
- [x] Documentación de códigos de error y manejo

## Próximos pasos
- Integración frontend con el nuevo endpoint conversacional
- Mejoras en prompts y validación conversacional avanzada
- Feedback de usuario y ajustes UX
- Implementación de frontend MVP
- Pruebas de integración frontend-backend

---

**¿Cómo marcar tareas?**
- Cambia `[ ]` por `[x]` cuando completes una tarea.
- Agrega comentarios o responsables si es necesario.

**¡Actualiza este archivo con cada avance!**

![MVP Progress](https://img.shields.io/badge/MVP%20Progress-85%25-green) 

**Notas del MVP:**
1. El sistema conversacional es el core del MVP
2. La generación de planes y seguimiento son esenciales
3. Las notificaciones y feedback son parte del MVP para mantener al usuario motivado
4. El frontend debe ser intuitivo y fácil de usar
5. La integración con IA es crítica para el funcionamiento del sistema

## Permisos y seguridad
- Todos los endpoints de planes, rutinas y ejercicios están protegidos por permisos de usuario autenticado (y admin para acceso global). Verificado en tests y documentación.
