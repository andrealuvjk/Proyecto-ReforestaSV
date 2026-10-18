from django.db import models
from django.contrib.auth.models import AbstractUser


#HERENCIA EN USUARIO
# ==========================================
# 1. MODELO PRINCIPAL (Crea la tabla 'usuarios')
# ==========================================

# usuario = Usuario.objects.create_user(
#    email='ana@gmail.com',
 #   password='PasswordSegura123',
#    nombre='Ana Martínez',
 #   telefono='71234567',
 #   rol=Usuario.Rol.VOLUNTARIO  # Especificas el rol explícitamente
 # )  Estructura para crear un usuario

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
# MANAGERS PARA FILTRAR AUTOMÁTICAMENTE
# ==========================================

class AdminManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(rol=Usuario.Rol.ADMIN)


class VoluntarioManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(rol=Usuario.Rol.VOLUNTARIO)


class ResponsableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(rol=Usuario.Rol.RESPONSABLE)


# ==========================================
# 2. MODELOS PROXY (Usan la misma tabla 'usuarios')
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
    

class Ubicacion(models.Model):
  
    zona = models.CharField(max_length=150)
    ubicacion = models.CharField(max_length=250)

    class Meta:
        db_table = "ubicaciones"

    def __str__(self):
        return f"{self.zona} -{self.ubicacion}"


class Especie(models.Model):
  
    nombre = models.CharField(max_length=100) #[cite: 2]

    class Meta:
        db_table = 'especies' #[cite: 2]

    def __str__(self):
        return self.nombre

class Campania(models.Model):

    titulo = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        db_column= 'usuario_id',
        related_name='campanias'
    )
    fecha_inicio= models.DateField()
    fecha_fin= models.DateField()

    class Meta:
        db_table= 'campanias'

    def __str__(self):
        return self.titulo

class Inventario(models.Model):
    especie = models.ForeignKey(
        Especie,
        on_delete=models.CASCADE,
        db_column='especie_id',
        related_name='inventarios'

    )
    cantidad = models.IntegerField()
    campania = models.ForeignKey(
        Campania, 
        on_delete=models.CASCADE, 
        db_column='campania_id', 
        related_name='inventarios'
    )
    img_url = models.CharField(max_length=250, blank=True, null=True)
    ubicacion = models.ForeignKey(
        Ubicacion, 
        on_delete=models.CASCADE, 
        db_column='ubicacion_id', 
        related_name='inventarios'
    )

    responsable = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        db_column='responsable_id', 
        related_name='inventarios_responsable'
    ) 

    class Meta:
        db_table = 'Inventarios'

    def __str__(self):
        return f"Inventario #{self.id} - {self.especie.nombre}"
class ArbolPlantado(models.Model):
    """
    Tabla: arboles_plantados[cite: 2]
    """
    fecha = models.DateField(blank=True, null=True) #[cite: 2]
    estado = models.CharField(max_length=50, blank=True, null=True) #[cite: 2]
    inventario = models.ForeignKey(
        Inventario, 
        on_delete=models.CASCADE, 
        db_column='inventario_id', 
        related_name='arboles_plantados'
    ) #[cite: 2]

    class Meta:
        db_table = 'arboles_plantados' #[cite: 2]

    def __str__(self):
        return f"Árbol #{self.id} ({self.estado})"


class Mantenimiento(models.Model):
    """
    Tabla: mantenimientos[cite: 2]
    """
    fecha = models.DateTimeField() #[cite: 2]
    descripcion = models.CharField(max_length=250) #[cite: 2]
    arbol_plantado = models.ForeignKey(
        ArbolPlantado, 
        on_delete=models.CASCADE, 
        db_column='arbol_plantado_id', 
        related_name='mantenimientos'
    ) #[cite: 2]

    class Meta:
        db_table = 'mantenimientos' #[cite: 2]

    def __str__(self):
        return f"Mantenimiento #{self.id} - {self.fecha}"