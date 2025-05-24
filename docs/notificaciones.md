# Notificaciones Motivacionales

## Backend

### Lógica Actual
- Las notificaciones motivacionales se generan a través del endpoint `generar-motivacional`.
- Al crear una notificación, se establece su status como `pendiente`.
- Se ha implementado una tarea Celery (`send_scheduled_motivational_notifications`) que se ejecuta cada minuto, busca notificaciones pendientes cuya hora_preferida coincide con la hora actual, y las marca como `enviada`.
- Solo el admin puede ver todas las notificaciones, mientras que los usuarios normales solo ven las suyas con status `enviada`.

### Tarea Celery
- La tarea se encuentra en `notifications/tasks.py`.
- Simula el envío de notificaciones al frontend imprimiendo un log con el mensaje y el usuario al que se le envía.
- Requiere que Redis esté corriendo localmente para las pruebas.

## Frontend (Notas para Futura Implementación)

### Opciones para Recibir Notificaciones
1. **Polling**: El frontend puede hacer peticiones periódicas al backend para verificar si hay nuevas notificaciones.
2. **WebSockets**: Implementar una conexión en tiempo real entre el backend y el frontend (por ejemplo, usando Django Channels o Socket.io).
3. **Push Notifications**: Usar servicios como Firebase Cloud Messaging (FCM) para enviar notificaciones incluso cuando el usuario no está en la aplicación.

### Prioridades
- Por ahora, el backend está listo para generar y enviar notificaciones.
- La implementación del frontend se dejará para más adelante, priorizando otras tareas del proyecto. 