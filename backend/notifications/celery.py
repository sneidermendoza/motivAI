from celery import Celery
from celery.schedules import crontab

app = Celery('notifications')

# Configuración de Celery
app.conf.update(
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/0',
    timezone='UTC'
)

# Configuración de tareas periódicas
app.conf.beat_schedule = {
    'send-motivational-notifications': {
        'task': 'notifications.tasks.send_scheduled_motivational_notifications',
        'schedule': crontab(minute='*'),  # Se ejecuta cada minuto
    },
} 