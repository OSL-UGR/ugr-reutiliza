from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Mueble, Usuario


class Admin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Usuario
    list_display = ['email', 'username', 'telefono']
    fieldsets = (
            (None, {'fields': ('username', 'password')}), 
            ('Personal info', {'fields': ('email', 'telefono')}), 
            ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}), 
            ('Important dates', {'fields': ('last_login', 'date_joined')})
            )
    """(
            ({
                    'fields': ('email', 'password', 'username', 'telefono' )
            }),
    )
    """
    readonly_fields = ('email',)


admin.site.register(Usuario, Admin)
admin.site.register(Mueble)
# Register your models here.
