from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    nombre = models.CharField(max_length=50, default="")
    apellidos = models.CharField(max_length=100, default="")
    email = models.CharField(max_length=100, primary_key=True)
    puesto = models.CharField(max_length=100, default="")
    telefono = models.CharField(max_length=9, default="")
    organizacion = models.CharField(max_length=200, default="")


class Mueble(models.Model):
    nombre = models.CharField(max_length=20, default="")
    # dimensiones = 
    foto = models.CharField(max_length=50, null=True)
    descripcion = models.CharField(max_length=4000)
    # ofertante = 
    # demandantes = 
    ubiInicial = models.CharField(max_length=512, default="")
    # ubiFinal = 
