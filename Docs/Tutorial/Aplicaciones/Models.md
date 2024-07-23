El archivo models.py de Django es el que nos permite abstraernos de todo el tema de tratar con bases de datos.
___
## ¿Cómo crear un modelo?
Un ejemplo de modelo es el siguiente:
```Python
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

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

Vamos por partes, porque hay mucho que diseccionar aquí.
___
### Imports:
Desde las primeras líneas ya hay cosas que explicar:
```Python
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
```
Básicamente lo que hacemos aquí es importar models (La librería de Django que nos permitirá crear las partes que necesitarán nuestros modelos).

PermissionsMixin es una clase que nos permitirá saber si un usuario tiene permiso para acceder a una página o no, esto nos ayuda a diferenciar entre **Administradores y Usuarios corrientes** por ejemplo

Estamos importando también el modelo "AbstractBaseUser", hay dos modelos de usuario, el AbstractBaseUser y el AbstractUser.
#### AbtractUser:
El modelo AbstractUser contiene varios campos que suelen ser necesarios para los usuarios en las bases de datos, sin embargo es posible que queramos un usuario limpio, sin prácticamente ningún atributo, para esto sirve el AbstractBaseUser.
#### AbstractBaseUser:
El modelo AbstractBase user es un usuario con los campos mínimos, que Django tratará para poder usarlo como usuario, pero podremos especificar la clave primaria, que en el AbstractUser viene predefinida.
___
### Declaración:
```Python
	class Usuario(AbstractBaseUser, PermissionsMixin):
```
Al hacer que usuario herede de AbstractBaseUser y PermissionsMixin nuestro Usuario tendría los atributos:
- Password (Heredado de AbstractBaseUser)
- is_superuser (Heredado de PermissionMixin)
Y no contiene clave primaria, que es necesaria para identificar entidades en una base de datos.

>[!important] Clave primaria por defecto
> En una base de datos no puede no haber una clave primaria, son parte de las entidades y debe existir una manera de diferenciarlas, cuando **no especifiquemos** una clave primaria, **Django creará la clave primaria "id"**, un elemento numérico que servirá como identificador para las entidades.

Si bien no es absolutamente necesario crear una clave primaria explícita en Django, es bastante recomendable para un usuario, ya que por ejemplo no queremos tener varios usuarios con el mismo email.
___
### Atributos:
```Python
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
```

La manera en Django de crear un atributo para un modelo es la mostrada arriba, consta de varias partes:

- Nombre: El texto que pongamos a la izquierda del igual va a ser como se llame el atributo en nuestra base de datos.
- Tipo: La manera es cogiendo de models el tipo de Campo que necesitemos, en nuestro caso hemos cogido por ejemplo EmailField, BooleanField, CharField y DateTimeField. 

>[!info] Campos
> Una lista completa de campos se puede encontrar [Aquí](https://docs.djangoproject.com/en/5.0/ref/models/fields/).

___
Cada tipo puede tener varios atributos que hay que especificar, pero los más importantes son:
- Default: Define el valor por defecto del atributo.
- Unique: Especifica que el valor de este atributo no puede repetirse.
- Null: Es un booleano que indica si se puede crear la entidad con un valor nulo para ese campo.
- Primary_key: Es un booleano que indica si es clave primara (En comportamiento es como poner Unique y Null a true).
- 
Un tipo importante es el **ForeignKey**:
```Python
    ofertante = models.ForeignKey(Usuario, related_name="user_email_provider",
                                  on_delete=models.CASCADE,
                                  default=Usuario.get_default_pk)
    demandante = models.ForeignKey(Usuario,
                                   related_name="user_email_requester",
                                   on_delete=models.DO_NOTHING, null=True)
```
Básicamente en las bases de datos una ForeignKey es una clave externa, lo que quiere decir que ese atributo es la clave primaria de otra entidad, por decirlo así que "Apunta" a esa otra entidad mediante este atributo.

Por ejemplo en el anterior ofertante es un Usuario.

Los atributos del constructor son:
 - Nombre de la entidad superior.
 - Nombre de la relación: Django lo suele crear sólo, pero en este ejemplo hay dos elementos del mismo tipo que se relacionan con el nuestro, por lo tanto el nombre que genera Django se repetiría, por tanto lo creamos a mano y así nos quitamos de problemas.
 - on_delete: Con este atributo definimos lo que se hará al borrar la entidad de nivel superior a la que apuntamos, models.CASCADE borra todos los atributos que pertenecen a la entidad borrada.

Por último queremos especificar qué elemento es el username, y cuáles son obligatorios.
```Python
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nombre", "apellidos", "puesto", "telefono",
                       "organizacion"]
```
___
### Otras configuraciones:
```Python
    objects = CustomUserManager()

	@classmethod
    def get_default_pk(cls):
        user = cls.objects.get(email="alux6mc@gmail.com")
        return user.pk

    def __str__(self):
        return self.email
```

Vemos tres definiciones:
#### objects
```Python
objects = CustomUserManager()
```
Bien, esta declaración es obligatoria cuando especificamos nuestro propio usuario, por defecto los modelos suelen traer los métodos ya definidos, pero al usar el AbstractBaseUser, esto no existe.

Se define en el archivo [[Managers]]

Y por último
- get_default_pk, en la que especificamos el mail por defecto.
-  \_\_str\_\_, donde decimos qué devolveremos al llamar al str de este objeto.