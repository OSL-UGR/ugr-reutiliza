En Django hay varias maneras de utilizar los formularios, la que ellos utilizan es creando objetos del tipo Form, que posteriormente pasan a la página para que se muestre dentro.

Otra forma, que es por ejemplo la que yo he tomado en la aplicación de Landing, ha sido crear formularios en los archivos HTML y posteriormente extraer la información de las peticiones POST que se le hacen a la vista.

Un ejemplo del primer modo sería:
```Python
from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label="Your name", max_length=100)
```
En este ejemplo de la documentación de Django, creamos un formulario con un sólo atributo.

___
```html
<form action="/your-name/" method="post">
    {% csrf_token %}
    {{ form }}
    <input type="submit" value="Submit">
</form>
```
Aquí vemos una página html donde el formulario está incompleto, esta nomenclatura se puede entender mejor en [[HTML#Lógica de Python]], donde se ve cómo usar bucles, condicionales y variables dentro del HTML.

Es importante darse cuenta de la segunda línea, `{% csrf_token %}`, que sirve para [poder evitar exploits csrf](https://www.stackhawk.com/blog/django-csrf-protection-guide/) al cambiar de una página a otra.

>[!important] CSRF Tokens
> Django no te permite enviar un formulario sin un token csrf, por seguridad. 



```Python
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import NameForm


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect("/thanks/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, "name.html", {"form": form})
```
Y por último vemos que lo que se hace es pasarle como contexto a la petición de renderizado de la página que queremos cargar, el formulario que queremos usar.

De esta manera donde antes ponía form, se meterá el formulario que hemos creado previamente.

Personalmente esta manera no me gusta mucho, porque es más complicado aplicarle estilos, pero es la manera oficial de Django, por tanto está bien explicarla.
___

>[!note] Más sobre formularios
> Para aprender más sobre la manera alternativa de creación de formularios, visitar [[Landing]].
