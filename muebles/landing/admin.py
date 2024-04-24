from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import mark_safe

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Mueble, Usuario, Foto


class Admin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Usuario
    list_display = ("email", "organizacion", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active", "organizacion")
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
    ordering = ("email",)
    readonly_fields = ("email",)


class MuebleAdmin(admin.ModelAdmin):
    list_display = ("nombre", "ofertante", "ubiInicial", "ofer_org")
    search_fields = ("nombre",)
    list_filter = ("ofertante", "ubiInicial", 'ofertante__organizacion')

    @admin.display(description='Organizacion', ordering='ofertante__organizacion')
    def ofer_org(self, obj):
        return obj.ofertante.organizacion

class FotoAdmin(admin.ModelAdmin):
    list_display = ["image_preview", "mueble_name", "ofertante_mail"]
    search_fields = ["mueble__nombre",]
    list_filter = ("mueble__ofertante", "mueble__ofertante__organizacion")

    @admin.display(description='Nombre del mueble', ordering='mueble__nombre')
    def mueble_name(self, obj):
        return obj.mueble.nombre

    @admin.display(description='Mail del ofertante', ordering='ofertante__email')
    def ofertante_mail(self, obj):
        return obj.mueble.ofertante.email

    def image_preview(self, obj):
        return mark_safe('<img src="{url}" max_width=128px height=128px />'.
                         format(url=obj.imagen.url,)
                         )


admin.site.register(Usuario, Admin)
admin.site.register(Mueble, MuebleAdmin)
admin.site.register(Foto, FotoAdmin)
