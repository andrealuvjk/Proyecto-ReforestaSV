import os
from django.core.management.base import BaseCommand
from usuarios.models import Usuario


class Command(BaseCommand):
    help = 'Crea un usuario Administrador y Superusuario automáticamente desde variables de entorno'

    def handle(self, *args, **kwargs):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        nombre = os.environ.get('DJANGO_SUPERUSER_NOMBRE', 'Administrador General')

        if not username or not password:
            self.stdout.write(self.style.WARNING(
                'Faltan variables DJANGO_SUPERUSER_USERNAME o DJANGO_SUPERUSER_PASSWORD. Omitiendo.'
            ))
            return

        if Usuario.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(f'El usuario "{username}" ya existe.'))
            return

        Usuario.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            nombre=nombre,
            rol=Usuario.Rol.ADMIN
        )
        self.stdout.write(self.style.SUCCESS(f'Administrador "{username}" creado exitosamente.'))