from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from django.conf import settings 
from .managers import CustomUserManager


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
