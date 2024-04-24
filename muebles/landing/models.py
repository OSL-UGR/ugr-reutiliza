from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from .managers import CustomUserManager
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
import os


@deconstructible
class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), max_length=100,
                              primary_key=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=100)
    puesto = models.CharField(max_length=100)
    telefono = models.CharField(max_length=9)
    organizacion = models.CharField(max_length=200)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nombre", "apellidos", "puesto", "telefono",
                       "organizacion"]

    objects = CustomUserManager()

    @classmethod
    def get_default_pk(cls):
        user = cls.objects.get(email="alux6mc@gmail.com")
        return user.pk

    def __str__(self):
        return self.email


class Mueble(models.Model):
    nombre = models.CharField(max_length=20, default="")
    dimensiones = models.CharField(max_length=200, default="")
    descripcion = models.CharField(max_length=4000)
    main_image = models.ImageField(upload_to='images/')
    ofertante = models.ForeignKey(Usuario, related_name="user_email_provider",
                                  on_delete=models.CASCADE,
                                  default=Usuario.get_default_pk)
    demandante = models.ForeignKey(Usuario,
                                   related_name="user_email_requester",
                                   on_delete=models.DO_NOTHING, null=True)
    ubiInicial = models.CharField(max_length=512, default="")
    ubiFinal = models.CharField(max_length=512, default="")


class Foto(models.Model):
    mueble = models.ForeignKey(Mueble, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='images/')


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
        # If the instance is being modified, check if the image field has changed
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
