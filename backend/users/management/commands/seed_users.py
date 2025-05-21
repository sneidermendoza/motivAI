from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Crea un usuario admin y uno normal para pruebas'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='sneider',
                email='mariasol0304@gmail.com',
                password='Cc1045698090',
                tipo_usuario='admin'
            )
            self.stdout.write(self.style.SUCCESS('Usuario admin creado'))