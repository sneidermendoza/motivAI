from celery import shared_task
from django.utils import timezone
from .models.notification import Notificacion

@shared_task
def send_scheduled_motivational_notifications():
    now = timezone.now()
    current_time = now.time()
    # Buscar notificaciones pendientes cuya hora_preferida coincide con la hora actual
    notifications = Notificacion.objects.filter(
        status='pendiente',
        hora_preferida__hour=current_time.hour,
        hora_preferida__minute=current_time.minute
    )
    for notification in notifications:
        # Aquí se podría agregar lógica para enviar la notificación (por ejemplo, por email, push, etc.)
        # Por ahora, solo marcamos como enviada y simulamos el envío al frontend
        notification.status = 'enviada'
        notification.save()
        print(f"Notificación enviada a {notification.usuario.username}: {notification.mensaje}")
    return f"Procesadas {notifications.count()} notificaciones motivacionales." 