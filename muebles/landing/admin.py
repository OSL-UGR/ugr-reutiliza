from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Mueble, Usuario, Foto


class Admin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Usuario
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
            (None, {
                "fields": ("nombre", "apellidos", "puesto", "telefono",
                           "organizacion", "email")}),
            ("Permissions", {"fields": ("is_staff", "is_active", "groups",
                                        "user_permissions")}),
            )
    add_fieldsets = (
            (None, {
                "classes": ("wide",),
                "fields": ("nombre", "apellidos", "puesto", "telefono",
                           "organizacion", "email", "password1",
                           "password2")}),
            ("Permissions", {"fields": ("is_staff",
                                        "is_active", "groups",
                                        "user_permissions")}

             ),
            )
    search_fields = ("email", "organizacion")
    ordering = ("email", "organizacion")
    readonly_fields = ("email",)


admin.site.register(Usuario, Admin)
admin.site.register(Mueble)
admin.site.register(Foto)
