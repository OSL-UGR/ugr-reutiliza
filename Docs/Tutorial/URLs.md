Los archivos URL constan de dos partes, diferenciaremos entre el archivo URL de proyecto y URL de aplicaciones.
___
## URLs de Proyecto
Los archivos URL de proyecto tienen la estructura:
```Python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include("landing.urls"), name='landing'),
    path('admin/', admin.site.urls, name='admin'),
]
```

Podemos ver que son bastante simples, importamos todas las aplicaciones que queramos usar, y posteriormente les asignamos una dirección en nuestra web.

Por ejemplo landing tiene la dirección por defecto, lo cual nos indica que es una aplicación principal, y seguramente sea donde los usuarios comunes pasen más tiempo.

Sin embargo, admin tiene la dirección /admin, lo cual quiere decir que para acceder a ella debemos escribir /admin/ delante de cada ruta a la que queramos acceder.

En este archivo también pueden escribirse los [[Sitemaps]].
___
## URLs de Aplicaciones
Los archivos URL de aplicación tienen la estructura:
```Python
from django.urls import path
from . import views

urlpatterns = [
        path("", views.index, name="index"),
        path("login", views.loginPage, name="login")
]
```

En este caso podemos ver que hacemos referencia a [[Views]], esto significa que toda la lógica detrás de las URLs que escribimos aquí debe ser definida en en archivo "views.py".