
# *Fuente*:
```Python
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
import os


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

    def get_absolute_url(self):
        return f'/{self.id}/post'


class Foto(models.Model):
    mueble = models.ForeignKey(Mueble, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='images/')

    def get_absolute_url(self):
        return f'{self.imagen.url}'


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
```
# *Imports*
```Python
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
import os
```
## models:
La librería models nos permite crear modelos en Django, es la librería base para cualquier entidad que queramos crear en la base de datos.
## AbstractBaseUser:
Como ya se explica en el [[Models|tutorial]], esta clase consiste de lo más básico de una entidad usuario (Normalmente sólo la contraseña), sirve para crear usuarios totalmente desde cero, para poder poner nuestra propia estructura.
## PermissionsMixin:
Siguiendo con lo que también se explica en el tutorial, el PermissionsMixin incluye el campo is_superuser, que nos sirve para poder asignar niveles de permiso a los diferentes usuarios que podríamos crear.
## gettext_lazy:
Es una librería para compatibilizar los idiomas con la web.
## timezone:
Es una librería para varias funcionalidades de tiempos.
## CustomUserManager:
Esto se explica en [[managers.py]].

## pre_delete, pre_save:
Son dos señales de Django, sirven para ejecutar funciones en determinados momentos, por ejemplo antes de borrar o guardar, como estos.
## reciever:
Es el decorador encargado de recibir las señales, se pone antes de la función junto a la señal que se quiere recuperar y el emisor.
___
# *Modelos*:

## Usuario:
La definición completa de la clase usuario es:
```Python
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

```
Los atributos son muy simples, puede encontrarse una explicación de los modelos en [[Models]]. 

### Manager:
En este caso hemos tenido que crear nuestro propio manager, un manager básicamente es la interfaz que hay entre la entidad y Django.
### Métodos:
- El primer método que vemos es el siguiente:
```Python
    @classmethod
    def get_default_pk(cls):
        user = cls.objects.get(email="alux6mc@gmail.com")
        return user.pk
```
Básicamente decimos que para esta entidad, el mail por defecto es alux6mc@gmail.com (El mío, dado que lo estoy desarrollando actualmente), esto sirve más tarde.

- El segundo método es para asociar a la entidad con un string:
```Python
    def __str__(self):
        return self.email
```
___
## Mueble:
```Python
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

    def get_absolute_url(self):
        return f'/{self.id}/post'

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

```
### Métodos:
En este caso tenemos únicamente un método como tal:
```Python
    def get_absolute_url(self):
        return f'/{self.id}/post'
```
Básicamente sirve para poder obtener la url asociada a nuestro Mueble.
### Señales:
Vemos que, como se ha explicado antes, tenemos un receiver, para poder detectar las señales, que hace un trigger antes de borrar o guardar (o modificar, porque también se envía un pre_save) a una instancia de Mueble.
```Python
@receiver([pre_delete, pre_save], sender=Mueble)
def delete_images_mueble(sender, instance, **kwargs):
	...
```
Cuando detectamos cualquiera de estas señales ejecutamos la función delete_images_mueble.

Podemos dividir esta función en dos:
#### pre_delete:
Antes de borrar comprobamos si la imágen asociada al modelo existe, si existiese entonces guardamos la ruta en la que está guardada.

Si en nuestro sistema existe el archivo asociado a la ruta, lo borramos.

De esta manera lo que hacemos es borrar las fotos cuando borremos un mueble, para no ocupar memoria de manera tonta.
```Python
    if kwargs.get('signal') == pre_delete:
        # Delete the associated image when the instance is deleted
        if instance.main_image:
            # Get the path of the image file
            image_path = instance.main_image.path
            # Check if the file exists before attempting to delete it
            if os.path.exists(image_path):
                # Delete the file
                os.remove(image_path)
```
#### pre_save:
Antes de guardar, de manera similar al anterior vamos a hacer varias comprobaciones:
1. Comprobamos si el objeto tiene clave primaria (Normalmente lo tendrá, pero lo comprobamos para hacer el código más robusto), si la tuviese obtenemos la instancia asociada a esa clave primaria.
2. Si la imagen de la instancia original (La que estamos viendo si vamos a borrar) es igual que la de la nueva instancia, no hacemos nada, porque si la imagen no ha cambiado, no tendría sentido borrarla para guardarla de nuevo.
3. Finalmente repetimos lo del delete, comprobamos si existe la imagen, luego la ruta asociada a esta y finalmente la borramos.
```Python
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
```
___
## *Foto*:
Este modelo es muy parecido al anterior, básicamente lo usamos para guardar en la base de datos la relación de las fotos con los muebles, cuando estos muebles se borren borraremos todas las fotos asociadas a ellos (Esto significa lo que hay como valor del on_delete)
```Python
class Foto(models.Model):
    mueble = models.ForeignKey(Mueble, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='images/')
    
    def get_absolute_url(self):
        return f'{self.imagen.url}'
        
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
```

### Métodos:
De nuevo el único método que tenemos es para obtener la url de nuestra imágen.
```Python
    def get_absolute_url(self):
        return f'{self.imagen.url}'
```
___
### Señales:
Esta estructura es idéntica a la de las fotos de Muebles (Básicamente porque queremos hacer lo mismo, borrar las fotos asociadas a nuestra entidad foto cuando las cambiemos o borremos).

Las únicas diferencias es que en este caso el sender es Foto, y que el nombre del atributo de imagen es ***imagen*** y no ***main_image*** como en la anterior.
```Python
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
```