# *Fuente*:
```Python
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('email', 'nombre', 'apellidos', 'puesto', 'telefono',
                  'organizacion')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Usuario
        fields = ('email', 'nombre', 'apellidos', 'puesto', 'telefono',
                  'organizacion')
```
___
En el archivo Forms lo que hacemos es crear los formularios para la página de Admin, pero en general lo que se hace en un forms en Django es crear los formularios que posteriormente se usarán en las aplicaciones, aunque como [[Forms|ya expliqué en el tutorial]] no me gusta esta manera de hacerlo.