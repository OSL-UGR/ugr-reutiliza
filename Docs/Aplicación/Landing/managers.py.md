Como se menciona en [[Managers]], el archivo managers.py sirve para proporcionar a Django una interfaz para poder comunicarse con las entidades especiales, en este caso por ejemplo
nos hace falta para poder crear usuarios y superusuarios en el modelo [[models.py#Usuario|User]].
# *Fuente*:
```Python
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)
```

## ***Manager***:
Dentro del manager, aunque no hay mucho que explicar, podemos ver que hay dos funciones, las partes importantes de las funciones son:
```Python
        if not email:
            raise ValueError(_("The Email must be set"))
```
Para confirmar que nuestra clave primaria está definida, y que no vamos a pedir crear un usuario sin la clave primaria.

Después ya normalizamos el email y se lo asignamos a usuario, le ponemos también la contraseña, lo guardamos y lo devolvemos.

Con superuser es lo mismo, pero comprobamos que tienen que ser stapp y activo también.