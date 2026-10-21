from django.db import models
from django.conf import settings

class Especie(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'especies'

    def __str__(self):
        return self.nombre

    #metodo propio 
    def total_ejemplares(self):
        """Calcula el número total de árboles de esta especie registrados en todos los inventarios."""
        return sum(item.cantidad for item in self.inventarios.all())


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
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='usuario_id', #se renombro el campo para mayor claridad, pq puede ser voluntario o responsable
        related_name='inventarios_asignados'
    )

    class Meta:
        db_table = 'inventarios'

    def __str__(self):
        return f"Inventario #{self.id} - {self.especie.nombre}"

    #metodo propio 
    def actualizar_cantidad(self, nueva_cantidad):
        """Actualiza la cantidad de árboles disponibles en este lote de inventario."""
        if nueva_cantidad >= 0:
            self.cantidad = nueva_cantidad
            self.save()
            return True
        return False
    
     #metodo devuelve una cantidad de arboles con estado especifico de ese LOTE
    def conteo_por_estado(self, estado_buscado):
        return self.arboles_plantados.filter(estado__iexact=estado_buscado).count()
    
    #devuelve la cantidad de arboles sanos en ese lote
    def arboles_sanos(self):
        """Devuelve la cantidad de árboles sanos en este lote."""
        return self.conteo_por_estado('SANO')
    
     #devuelve la cantidad de arboles deteriorados en ese lote
    def arboles_deteriorados(self):
        """Devuelve la cantidad de árboles deteriorados en este lote."""
        return self.conteo_por_estado('DETERIORADO')