import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.core.mail import send_mail

send_mail(
    subject='Prueba de email motivAI',
    message='¡Este es un email de prueba desde tu backend motivAI!',
    from_email=None,  # Usará DEFAULT_FROM_EMAIL
    recipient_list=['mariasol0304@gmail.com'],
    fail_silently=False,
)
print("¡Email de prueba enviado (o error mostrado arriba)!")