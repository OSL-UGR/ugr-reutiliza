El archivo urls.py es en el que definiremos la estructura de nuestras aplicaciones (en este caso "Landing").
# *Fuente*:
```Python
from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

from . import views

urlpatterns = [
        path("", views.index, name="index"),
        path("login", views.loginPage, name="login"),
        path("logout", views.logoutPage, name="logout"),
        path("perfil", views.perfil, name="perfil"),
        path("add", views.addMueble, name="add"),
        path("<int:mueble_id>/post", views.post, name="post"),
        path("<int:mueble_id>/delete", views.deleteMueble, name="delete"),
        path("<int:mueble_id>/modify", views.modifyMueble, name="modify"),
        path("<int:mueble_id>/book", views.bookMueble, name="book"),
        path("<int:mueble_id>/", views.deleteMueble, name="delete"),
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root':
                                                 settings.MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root':
                                                  settings.STATIC_ROOT}),
        ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
```
___
# Imports
```Python
from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

from . import views
```
## path y re_path
Estas funciones sirven para crear las direcciones, una de manera "normal" y la otra usando regex.
## static
Sirve para poder cargar todos los archivos de static, es similar al funcionamiento de [[HTML#Cláusulas static|Las cláusulas static]].
## settings
Importa los valores de settings para poder usar variables del archivo [[settings.py]] del proyecto.

## serve

## views
Como ya dijimos, el archivo [[Views|views]] es en el que especificamos las rutas de las diferentes partes de una aplicación, hay que importarlo para poder usar las funciones definidas en él.
___
# urlpatterns:
En este vector es en el que guardamos nuestras rutas, hay varias formas de definir una ruta:
## Rutas simples:
Tienen el formato:
```Python
path("{Ruta}", {Función}, {Nombre})
```

```Python
path("", views.index, name="index"),
path("login", views.loginPage, name="login"),
path("logout", views.logoutPage, name="logout"),
```
La función que pongamos en el apartado de función será la que se llame al acceder a esa dirección.
## Rutas calculadas:
Dependen de variables de los objetos.
```Python
path("<int:mueble_id>/post", views.post, name="post"),
path("<int:mueble_id>/delete", views.deleteMueble, name="delete"),
path("<int:mueble_id>/modify", views.modifyMueble, name="modify"),
```
Como vemos la primera parte de la ruta será sustituida por el id del mueble, generando así una dirección única para cada uno de nuestros muebles.

## Rutas regex:
```Python
re_path(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),
re_path(r'^static/(?P<path>.*)$', serve, {'document_root':settings.STATIC_ROOT}),
```
Son parecidas a las anteriores pero usamos [regex](https://w3.unpocodetodo.info/utiles/regex-diacriticos.php) para su creación.

Vemos que en este caso los elementos de media y de static tendrán su propia ruta en la web, para poder acceder a ellas posteriormente.