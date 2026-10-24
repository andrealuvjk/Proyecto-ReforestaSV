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
    def obtener_ultimo_mantenimiento(self):
        """Devuelve el registro de mantenimiento más reciente de este árbol."""
        return self.mantenimientos.order_by('-fecha').first()

    def cambiar_estado(self, nuevo_estado):
        """Modifica y guarda el estado actual de este árbol (ej: 'SANO', 'DETERIORADO', 'PERDIDO')."""
        if nuevo_estado:
            self.estado = nuevo_estado
            self.save()

    def actualizar_datos(self, nuevo_estado=None, nueva_fecha=None):
        """Actualiza los datos generales de este árbol sembrado."""
        if nuevo_estado:
            self.estado = nuevo_estado
        if nueva_fecha:
            self.fecha = nueva_fecha
        self.save()

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

    def actualizar_datos(self, nueva_fecha=None, nueva_descripcion=None):
        """Permite editar la fecha o la descripción del registro de mantenimiento."""
        if nueva_fecha:
            self.fecha = nueva_fecha
        if nueva_descripcion:
            self.descripcion = nueva_descripcion
        self.save()