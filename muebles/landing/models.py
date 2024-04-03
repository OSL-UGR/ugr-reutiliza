from django.db import models

"""
class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=100)
    puesto = models.CharField(max_length=100)
    telefono = models.CharField(max_length=9)
    email = models.CharField(max_length=100, primary_key=True)
    organizacion = models.CharField(max_length=200)
    passwordHash = models.CharField(max_length=100)
"""


class Mueble(models.Model):
    nombre = models.CharField(max_length=20, default="")
    # dimensiones = 
    foto = models.CharField(max_length=50, null=True)
    descripcion = models.CharField(max_length=4000)
    # ofertante = 
    # demandantes = 
    ubiInicial = models.CharField(max_length=512, default="")
    # ubiFinal = 
