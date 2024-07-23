En el archivo admin configuramos la vista de la página admin y los diferentes modelos que queremos mostrar en ella.
# *Fuente*:
```Python
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
```
___
# *Imports*:
## Admin:
Este import nos carga la aplicación admin, que es una aplicación separada de Landing, es una aplicación específica de Django que proporciona para facilitar el desarrollo de webs que requieran registro de usuarios.
## UserAdmin:
Es el usuario por defecto que tiene la aplicación Admin, lo importamos para poder modificarlo y ajustarlo a nuestras preferencias.
## mark_safe:
Convierte una string de python en una string de html, sirve para poder usar este valor en cualquier lugar donde se pueda usar un string en html.
## CustomUserCreationForm y CustomUserCreationForm:
Aquí importamos los formularios que previamente hemos creado en [[forms.py]] para poder modificar y crear nuestras entidades en la página admin sin problema (como por defecto usa la configuración que trae la aplicación Admin, es posible que nosotros, al haber creado nuestro propio [[Models#AbstractBaseUser|usuario]], no tengamos las mismas restricciones, atributos y características que el Admin original).
## Mueble, Usuario y Foto
Estos son nuestros [[models.py|modelos]], los importamos para poder modificar las instancias de estas entidades desde nuestra página de admin.
___
# *Admin*:
Nuestra primera clase es la representación del usuario en la página admin.
```Python
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
```
## add_form y form:
Estas variables lo que hacen es especificar dentro de la clase UserAdmin los formularios que usaremos para, respectivamente, añadir y modificar usuarios, como podemos ver les asignamos los formularios que hemos tenido que crear previamente.
## model:
Esta variable enlaza la clase Admin (que es la representación de nuestro usuario en la aplicación Admin), con el modelo que queremos manipular en la base de datos, en nuestro caso es Usuario.

## list_display:
En esta variable guardamos, en forma de lista, las variables que queremos que se muestren en la lista principal de los elementos de nuestro modelo.
![[Pasted image 20240515125521.png]]
## list_filter:
La variable list_filter sirve para poder especificar criterios de filtrado (Aunque parezca obvio) como se muestra en la imagen:
![[Pasted image 20240515125716.png]]
## fieldsets:
Esta variable sirve para especificar los elementos que se nos mostrarán al hacer click sobre la entidad, podemos ver que son iguales.
![[Pasted image 20240515125913.png]]
Sigue la siguiente estructura:
```Python
fieldsets = (None, {
                "fields": ("nombre", "apellidos", "puesto", "telefono",
                           "organizacion", "email")}),
                ("Permissions", {"fields": ("is_staff", "is_active", "groups",
                                            "user_permissions")}),
                )
```
Es muy importante que pongamos el None, básicamente tenemos varias listas que contienen un diccionario "fields", cada una de estas listas es una "sección", son muy fáciles de reconocer porque son una línea celeste de lado a lado (en el estilo por defecto de Admin, ya que el estilo de la página también es modificable).

Podemos ver que tenemos dos, la sección **por defecto**, representada por un **None**, y la sección **Permissions**, representada por el propio nombre de la sección.

Es importante poner el None, porque si no, no hay sección por defecto y Django puede hacer cosas raras.
## add_fieldsets:
Es exactamente igual que el fieldsets pero para añadir usuarios, podemos ver que hay más atributos y que se corresponde con el de la siguiente imagen.
![[Pasted image 20240515131538.png]]
## search_fields:
Estos campos son muy delicados, ya que aunque buscar a un usuario por su email no es ningún problema, si por ejemplo queremos buscar todas las fotos que pertenecen a un usuario, tenemos que hacer un par de cosas.
## ordering:
Define el atributo que vamos a usar para ordenar a los usuarios.
___
# *MuebleAdmin*:
```Python
class MuebleAdmin(admin.ModelAdmin):
    list_display = ("nombre", "ofertante", "ubiInicial", "ofer_org")
    search_fields = ("nombre",)
    list_filter = ("ofertante", "ubiInicial", 'ofertante__organizacion')

    @admin.display(description='Organizacion', ordering='ofertante__organizacion')
    def ofer_org(self, obj):
        return obj.ofertante.organizacion
```
Vemos que en esta tenemos algunos añadidos, lo que está explicado en Admin no lo volveré a explicar, pero profundizaré en lo nuevo.
## list_display y list_filter:
Aunque siguen siendo iguales que antes en cuanto a estructura, vemos que hay unos campo ofer_org y orfetante__organizacion que pueden llamarnos la atención, porque no son como tal atributos de nuestra entidad, sino que son atributos del objeto ofertante, que es una clave externa que contiene Mueble.

Por tanto vemos que algo hay que hacer, no podemos usar elementos que no están en nuestro objeto, así que definimos una función con el embellecedor: 
```Python 
@admin.display(...)
```

## admin.display:
Si bien el embellecedor no es absolutamente necesario, se usa para dos cosas:
1. Poder definir el nombre que tendrá este campo dentro de nuestro display, ya que por defecto usa el nombre de la función en mayúsculas y cambiando las barras bajas por espacios.
2. Poder usarlo para ordenar, si no definimos que el orden debe cogerse del atributo organización de ofertante (se hace con la sintaxis {atributo con clave externa}\_\_{atributo de entidad externa}), aunque puede parecer complicado, es igual que acceder a los atributos de la entidad, pero usando "\_\_" en lugar de "."
```Python
    @admin.display(description='Organizacion', ordering='ofertante__organizacion')
    def ofer_org(self, obj):
        return obj.ofertante.organizacion
```
De esta manera, podemos mostrar y filtrar por la organización en la que se encuentra nuestro mueble, desde la ventana de muebles.
![[Pasted image 20240515132830.png]]
![[Pasted image 20240515132842.png]]
En estas dos imágenes podemos ver que está el campo organización, un campo externo a nuestra entidad mueble.
___
# *FotoAdmin*:
Llegados a este punto conocemos prácticamente todo lo necesario para formar la última entidad, pero puede asustar un poco porque usa todo lo anterior varias veces, y sobre todo por la última parte, en la que cargamos la preview de una imágen.
```Python
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
```
Como hemos explicado antes, estamos accediendo al nombre del mueble asociado a la imagen, y el mail del ofertante.

>[!note]
Vemos que para los filtros no es necesario crear toda la parafernalia anteriormente mencionada (se puede observar en que **no tenemos embellecedor para mueble\_\_ofertante\_\_organización**), ya que el nombre que se pondrá en el filtro será el del último atributo accedido, sin embargo para ordenar los elementos con esto y para poder buscar, si que es necesario, por lo mencionado anteriormente.

## image_preview:
Aunque esta línea puede resultar intimidante de primeras, básicamente lo que estamos haciendo es insertar en la lista de displays, en lugar de un valor, una imágen, esto hará que nuestro Django muestre este elemento en lugar de insertar un valor normal de la tabla.

Podemos ver un ejemplo de esto en el admin:
![[Pasted image 20240515133712.png]]
___
# *Register*:
Por último las cláusulas register sirven para poder añadir estas entidades a la página de admin, junto con sus configuraciones.
![[Pasted image 20240515134438.png]]
