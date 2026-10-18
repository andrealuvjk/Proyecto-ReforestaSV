from django.db import models

class ArbolPlantado(models.Model):
    fecha = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    inventario = models.ForeignKey(
        'inventarios.Inventario',
        on_delete=models.CASCADE,
        db_column='inventario_id',
        related_name='arboles_plantados'
    )

    class Meta:
        db_table = 'arboles_plantados'

    def __str__(self):
        return f"Árbol #{self.id} ({self.estado})"


class Mantenimiento(models.Model):
    fecha = models.DateTimeField()
    descripcion = models.CharField(max_length=250)
    arbol_plantado = models.ForeignKey(
        'ArbolPlantado',
        on_delete=models.CASCADE,
        db_column='arbol_plantado_id',
        related_name='mantenimientos'
    )

    class Meta:
        db_table = 'mantenimientos'

    def __str__(self):
        return f"Mantenimiento #{self.id} - {self.fecha}"