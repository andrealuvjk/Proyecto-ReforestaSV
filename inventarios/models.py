from django.db import models
from django.conf import settings

class Especie(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'especies'

    def __str__(self):
        return self.nombre


class Inventario(models.Model):
    especie = models.ForeignKey(
        'inventarios.Especie',
        on_delete=models.CASCADE,
        db_column='especie_id',
        related_name='inventarios'
    )
    cantidad = models.IntegerField()
    campania = models.ForeignKey(
        'campanias.Campania',
        on_delete=models.CASCADE,
        db_column='campania_id',
        related_name='inventarios'
    )
    img_url = models.CharField(max_length=250, blank=True, null=True)
    ubicacion = models.ForeignKey(
        'campanias.Ubicacion',
        on_delete=models.CASCADE,
        db_column='ubicacion_id',
        related_name='inventarios'
    )
    responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='responsable_id',
        related_name='inventarios_responsable'
    )

    class Meta:
        db_table = 'Inventarios'

    def __str__(self):
        return f"Inventario #{self.id} - {self.especie.nombre}"