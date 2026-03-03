from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
import os

# El primer valor es lo que se guarda en la base de datos y el segundo es lo que lee 
# Esta tupla se utiliza para generar en html un <select> de forma automatica con django

categorias = (
        ('Silla', 'Silla'),
        ('Mesa', 'Mesa'),
        ('Armario-Vitrina', 'Armario-Vitrina'),
        ('Pizarra', 'Pizarra'),
        ('Cajonera', 'Cajonera'),
        ('Perchero', 'Perchero'),
        ('Papelera', 'Papelera'),
        ('Estantería', 'Estantería'),
        ('Otro', 'Otro'),
        )

# Almacenará todos los DNIS permitidos por la aplicación. E
class DniAutorizado(models.Model):
    #Tendra 9 caracteres, debe ser único es es la primary_key de la tabla
    dni = models.CharField(max_length=9, unique=True, primary_key=True)

    def __str__(self):

        return self.dni

# La primary key es el email
# TODO Panel de administrador personalizado:
# Al eliminar un Usuario desde el nuevo panel, se borrarán en cascada todos los Muebles que haya ofertado (on_delete=CASCADE en Mueble). 
# Se mostrará en el panel mostramos un aviso de "Se borrarán X muebles" antes de confirmar.
class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), max_length=100,
                              primary_key=True) 
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # Gracias a blank hacemos que el campo es opcional a nivel de validación
    dni = models.CharField(max_length=9, unique=True, null=True, blank=True)

    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=100)
    puesto = models.CharField(max_length=100)
    telefono = models.CharField(max_length=9)
    organizacion = models.CharField(max_length=200)

    # A la hora de un login, el valor del campo "username" es el parámetro que nosotros hemos definido como 
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nombre", "apellidos", "puesto", "telefono",
                       "organizacion", "dni"]

    objects = CustomUserManager()

    # TODO: correo electrónico hardcoreado
    @classmethod
    def get_default_pk(cls):
        user = cls.objects.get(email="alux6mc@gmail.com")
        return user.pk

    def __str__(self):
        return self.email

# Todos los muebles están asociados a un un ofertante (usuario), si este se borrase tambíen se borraría el mueble
class Mueble(models.Model):
    nombre = models.CharField(max_length=100, default="")
    dimensiones = models.CharField(max_length=200, default="")
    descripcion = models.CharField(max_length=4000)
    main_image = models.ImageField(upload_to='images/')
    ofertante = models.ForeignKey(Usuario, related_name="user_email_provider",
                                  on_delete=models.CASCADE,
                                  default=Usuario.get_default_pk)
    ubiInicial = models.CharField(max_length=512, default="")
    ubiFinal = models.CharField(max_length=512, default="")
    cantidad = models.IntegerField(default=1)
    categoria = models.CharField(choices=categorias,
                                 default=categorias[0][0])
    
    # Añadimos una propiedad para que calcule en tiempo real el stock de un determinado mueble en todas las reservas
    @property
    def stock_disponible(self):

        # Busca las reservas que están asociadas a ese mueble, excluyendo las que se encuentren canceladas
        reservas_activas = self.reserva_set.exclude(estado='Cancelada')

        # Sumamos la cantidad total
        total_reservado = sum(reserva.cantidad for reserva in reservas_activas)

        return self.cantidad - total_reservado

    def get_absolute_url(self):
        return f'/{self.id}/post'

# Permite que un mueble tenga fotos adicionales. Cada foto está vinculada a un mueble, obviamente si el mueble se borra sus fotos tb
class Foto(models.Model):
    mueble = models.ForeignKey(Mueble, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='images/')

    def get_absolute_url(self):
        return f'{self.imagen.url}'


class Reserva(models.Model):
    mueble = models.ForeignKey(Mueble, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    demandante = models.ForeignKey(Usuario,
                                   on_delete=models.CASCADE,
                                   null=True)
    
    # Además de esto, hay también un estado "Publicado", pero este se calcula automaticamente como
    # Publicados = (nºunidades total - nºunidades reservado/recodigo/retrasado) > 0
    ESTADOS_RESERVA = (

        ('Reservado', 'Reservado (En curso)'),
        ('Recogido', 'Completada (Recogido)'),
        ('Retrasado', 'Retrasado (+7 días)'),
        ('Cancelada', 'Cancelada'),
    )

    estado = models.CharField(max_length=20, choices=ESTADOS_RESERVA, default='Reservado')

    # Para almacenar cuando se hizo la resreva y cuando se va actualizando el estado
    fecha_reserva = models.DateTimeField(default=timezone.now)
    ultima_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.mueble.nombre} - {self.demandante.nombre} ({self.estado})"


@receiver([pre_delete, pre_save], sender=Foto)
def delete_images_foto(sender, instance, **kwargs):
    # Check if the instance is being deleted or modified
    if kwargs.get('signal') == pre_delete:
        # Delete the associated image when the instance is deleted
        if instance.imagen:
            # Get the path of the image file
            image_path = instance.imagen.path
            # Check if the file exists before attempting to delete it
            if os.path.exists(image_path):
                # Delete the file
                os.remove(image_path)
    elif kwargs.get('signal') == pre_save:
        if instance.pk:
            original_instance = sender.objects.get(pk=instance.pk)
            if original_instance.imagen != instance.imagen:
                # Delete the old image if it has been changed
                if original_instance.imagen:
                    old_image_path = original_instance.imagen.path
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)



@receiver([pre_delete, pre_save], sender=Mueble)
def delete_images_mueble(sender, instance, **kwargs):
    # Check if the instance is being deleted or modified
    if kwargs.get('signal') == pre_delete:
        # Delete the associated image when the instance is deleted
        if instance.main_image:
            # Get the path of the image file
            image_path = instance.main_image.path
            # Check if the file exists before attempting to delete it
            if os.path.exists(image_path):
                # Delete the file
                os.remove(image_path)
    elif kwargs.get('signal') == pre_save:
        # If the instance is being modified, check if the image field has changed
        if instance.pk:
            original_instance = sender.objects.get(pk=instance.pk)
            if original_instance.main_image != instance.main_image:
                # Delete the old image if it has been changed
                if original_instance.main_image:
                    old_image_path = original_instance.main_image.path
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
