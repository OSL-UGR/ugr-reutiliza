from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


# Como hemos definido el mail como primary_key para el usuario, estos dos métodos sobreescriben la instrucciones por defecto de Django
# para enseñarle a crear usuario  superusuarios.


# TODO Panel de administrador personalizado:
# Cuando implementemos la vista para CREAR un nuevo usuario desde el panel, NO debemos usar 'Usuario.objects.create()'. 
# Debemos usar obligatoriamente 'Usuario.objects.create_user(email=..., password=..., **datos)' 
# para asegurarnos de que la contraseña se encripta correctamente usando este Manager.

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
