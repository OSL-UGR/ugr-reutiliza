El archivo views es el que se encarga de dar toda la funcionalidad a las páginas, de las [[URLs]]
que definimos en el archivo del mismo nombre, aquí es donde se define lo que van a hacer cada una.

Por ejemplo:

```Python
def index(request):
    listaMuebles = Mueble.objects.order_by("-id")
    context = {
            "listaMuebles": listaMuebles,
            }
    return render(request, "muebles/muebles.html", context)
```

Esta función, a la que apunta la dirección / (Porque así lo definimos en URLs), es la función Index, podemos ver varias cosas.

1. Estamos obteniendo todos los objetos muebles ordenados por el atributo id.
2. Lo mandamos como contexto a la petición de carga de muebles.
3. Devolvemos la renderización de muebles.html con el contexto "context".

Básicamente la función render crea una respuesta http que contiene la página muebles.html pero pasándole listaMuebles como contexto para cargarla.

Esto se puede entender mejor en la sección [[HTML]].

Todo lo relacionado con la autenticación se puede ver más en profundidad en las [[settings.py|cláusulas del archivo settings]] y en las [[views.py|funciones del archivo views]], que está explicado con ejemplos y es mucho más fácil de entender así.