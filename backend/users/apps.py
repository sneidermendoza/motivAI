from django.apps import AppConfig
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    reset_url = f"http://localhost:3000/auth/reset-password?token={reset_password_token.key}&email={reset_password_token.user.email}"
    context = {
        'password_reset_url': reset_url,
        'current_year': 2025,
    }
    subject = "Recupera tu contraseña - motivAI"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [reset_password_token.user.email]
    html_content = render_to_string('registration/password_reset_email.html', context)
    msg = EmailMultiAlternatives(subject, html_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from django_rest_passwordreset.signals import reset_password_token_created
        from django.dispatch import receiver
        receiver(reset_password_token_created)(password_reset_token_created)
