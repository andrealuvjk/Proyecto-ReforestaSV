from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# ==========================================
# MODELO PRINCIPAL ('usuarios')
# ==========================================

class Usuario(AbstractUser):
    class Rol(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        VOLUNTARIO = 'VOLUNTARIO', 'Voluntario'
        RESPONSABLE = 'RESPONSABLE', 'Responsable'

    nombre = models.CharField(max_length=200)
    telefono = models.CharField(max_length=10, blank=True, null=True)
    institucion = models.CharField(max_length=200, blank=True, null=True)
    localidad = models.CharField(max_length=200, blank=True, null=True)
    rol = models.CharField(max_length=20, choices=Rol.choices, default=Rol.VOLUNTARIO)

    class Meta:
        db_table = 'usuarios'

    def __str__(self):
        return f"{self.nombre} ({self.rol})"


# ==========================================
# MANAGERS
# ==========================================

class ResponsableManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(rol=Usuario.Rol.RESPONSABLE)


class VoluntarioManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(rol=Usuario.Rol.VOLUNTARIO)


class AdminManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(rol=Usuario.Rol.ADMIN)

# ==========================================
# MODELOS PROXY
# ==========================================

class Admin(Usuario):
    objects = AdminManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.rol = Usuario.Rol.ADMIN
        super().save(*args, **kwargs)


class Voluntario(Usuario):
    objects = VoluntarioManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.rol = Usuario.Rol.VOLUNTARIO
        super().save(*args, **kwargs)


class Responsable(Usuario):
    objects = ResponsableManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.rol = Usuario.Rol.RESPONSABLE
        super().save(*args, **kwargs)