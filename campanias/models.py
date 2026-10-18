from django.db import models
from django.conf import settings

class Ubicacion(models.Model):
    zona = models.CharField(max_length=150)
    ubicacion = models.CharField(max_length=250)

    class Meta:
        db_table = "ubicaciones"

    def __str__(self):
        return f"{self.zona} - {self.ubicacion}"


class Campania(models.Model):
    titulo = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='usuario_id',
        related_name='campanias'
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    class Meta:
        db_table = 'campanias'

    def __str__(self):
        return self.titulo