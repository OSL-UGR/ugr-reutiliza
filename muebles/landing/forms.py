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
