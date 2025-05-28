# Plan de Trabajo Frontend motivAI (Next.js)

Este documento contiene el plan de trabajo detallado y el backlog inicial para el desarrollo del frontend de motivAI, alineado con el MVP y la integración con el backend. Actualiza este archivo conforme avances o completes tareas.

---

## 1. Configuración Inicial
- [x] Crear proyecto Next.js con TypeScript y Tailwind CSS
- [x] Configurar estructura base de carpetas (pages, components, hooks, utils, services, etc.)
- [x] Configurar ESLint, Prettier y Husky para calidad de código
- [ ] Configurar variables de entorno para endpoints del backend
- [ ] Documentar instalación y despliegue local

## 2. Autenticación y Usuarios
- [ ] Implementar registro y login de usuario (JWT)
- [ ] Implementar login social (Google/Facebook)
- [ ] Gestión de sesión y almacenamiento seguro del token JWT
- [ ] Página de perfil de usuario (ver y editar datos, foto de perfil)
- [ ] Cambio de contraseña (consumir endpoint backend)
- [ ] Recuperación de contraseña (flujo simulado, mostrar token)
- [ ] Eliminación de cuenta
- [ ] Manejo de roles y permisos en la UI (admin/usuario)

## 3. Sistema Conversacional (Core MVP)
- [ ] Interfaz de chat conversacional (UX tipo chat)
- [ ] Mostrar preguntas y opciones según el flujo recibido del backend
- [ ] Enviar respuestas y manejar validaciones, aclaraciones y fallback
- [ ] Mostrar mensajes de error y aclaración del backend
- [ ] Visualizar el estado y contexto de la conversación

## 4. Planes y Rutinas
- [ ] Visualización del plan activo y su cronograma
- [ ] Visualización del historial de planes (soft delete)
- [ ] Visualización y gestión de rutinas diarias
- [ ] Marcar rutina como realizada
- [ ] Visualización de ejercicios y detalles multimedia
- [ ] Adaptar/editar plan activo (si aplica)

## 5. Progreso
- [ ] Visualización del progreso del usuario (peso, medidas, energía, observaciones)
- [ ] Registro de progreso y subida de fotos
- [ ] Visualización de reportes y evolución

## 6. Notificaciones y Feedback
- [ ] Visualización de notificaciones motivacionales
- [ ] Integración futura de notificaciones push (PWA)
- [ ] Envío de feedback y sugerencias
- [ ] Visualización de feedback enviado

## 7. UI/UX y Accesibilidad
- [ ] Diseño responsivo y mobile-first
- [ ] Implementar paleta de colores y branding (docs/branding.md)
- [ ] Accesibilidad: contraste, navegación teclado, ARIA
- [ ] Soporte para varios idiomas (i18n)
- [ ] Animaciones y microinteracciones

## 8. Pruebas y Calidad
- [ ] Pruebas unitarias de componentes (Jest + React Testing Library)
- [ ] Pruebas de integración de flujos principales
- [ ] Pruebas E2E (Cypress o Playwright)
- [ ] Linter y formateo automático

## 9. Documentación y Organización
- [ ] Documentar estructura y flujos principales en README del frontend
- [ ] Documentar ejemplos de uso de endpoints y manejo de errores
- [ ] Mantener actualizado el backlog y el plan de trabajo

## 10. Integración Continua y Despliegue
- [ ] Configurar CI/CD (GitHub Actions o Vercel)
- [ ] Despliegue automático en entorno de pruebas
- [ ] Despliegue en producción

---

## Backlog Inicial (MVP)

| Prioridad | Área                | Tarea                                                      | Estado  |
|-----------|---------------------|------------------------------------------------------------|---------|
| Alta      | Autenticación       | Registro y login JWT                                       | [ ]     |
| Alta      | Conversación        | Interfaz de chat y consumo de flujo conversacional         | [ ]     |
| Alta      | Planes y Rutinas    | Visualización de plan activo y cronograma                  | [ ]     |
| Alta      | Progreso            | Registro y visualización de progreso                       | [ ]     |
| Alta      | Notificaciones      | Visualización de notificaciones motivacionales             | [ ]     |
| Media     | Feedback            | Envío y visualización de feedback                          | [ ]     |
| Media     | UI/UX               | Branding, responsividad y accesibilidad                    | [ ]     |
| Media     | Pruebas             | Pruebas unitarias y de integración                         | [ ]     |
| Media     | Documentación       | Documentar flujos y ejemplos de endpoints                  | [ ]     |
| Baja      | Notificaciones Push | Integración PWA y push real                                | [ ]     |
| Baja      | Gamificación        | Visualización de logros y medallas                         | [ ]     |
| Baja      | Comunidad           | Panel de comunidad/foro                                    | [ ]     |

---

## Mejoras Futuras (no MVP)
- Gamificación avanzada (logros, medallas, ranking)
- Integración con dispositivos externos (wearables, apps)
- Planes de nutrición y recetas
- Comunidad/foro y chat grupal
- Exportación de datos del usuario (CSV/JSON)
- Webhooks para integración con apps externas
- Integración de pagos y suscripciones

---

## Recomendaciones para el equipo
- Seguir la documentación y ejemplos del backend (Swagger, README, docs/backend_frontend_integracion.md)
- Mantener comunicación constante con el equipo backend ante cualquier duda
- Priorizar la experiencia de usuario y la accesibilidad
- Mantener el código modular, documentado y testeado
- Actualizar este plan y el backlog con cada avance

---

**¡Listos para construir el frontend MVP de motivAI! 🚀**
