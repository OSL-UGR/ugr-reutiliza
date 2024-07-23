# *Introducción*:
Debido a que el archivo views es uno de los más largos del proyecto, vamos a repasar lo que se hace en él:
1. En este archivo definimos lo que queremos que se haga cuando accedamos a las páginas que se enlacen a ellos desde el archivo [[urls.py]].
2. Definimos funciones genéricas que tendremos que usar dentro de estas otras funciones.
3. Recogemos y tratamos los datos de los formularios, las peticiones posts y todo lo que tenga que ver con el envío de datos desde el usuario hacia la página.
## @login_required:
El embellecedor @login_required sirve básicamente para decir que previo a cargar esa página, tenemos que comprobar que la petición venga acompañada de la correspondiente información de sesión, o lo que es lo mismo, que el usuario que quiere acceder a esta página esté registrado.

En caso de no estar registrado, lo que hace es redirigir al usuario hasta el valor que especifique la variable [[settings.py#LOGIN_URL|LOGIN_URL]], definida en el archivo settings.py.
___
# *Fuente*:
```Python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .backends import SettingsBackend
from .models import Mueble, Foto, Usuario

import json
import smtplib


backend = SettingsBackend()


def enviarEmail(demandante):
    smtpObj = smtplib.SMTP()

    sender = 'muebles@ejemplo.com'
    receivers = ['gehibey464@dacgu.com']

    smtpObj.sendmail(sender, receivers, message)


def permisoAñadir(email):
    usuario = Usuario.objects.get(pk=email)
    return (usuario.is_staff or
            usuario.is_superuser)


def permisoModificar(email, mueble_id):
    mueble = Mueble.objects.get(pk=mueble_id)
    usuario = Usuario.objects.get(pk=email)
    return ((usuario.is_staff and usuario == mueble.ofertante) or
            usuario.is_superuser)


@login_required
def index(request):
    listaMuebles = Mueble.objects.order_by("-id")
    context = {
            "listaMuebles": listaMuebles,
            }
    return render(request, "muebles/muebles.html", context)


def loginPage(request):
    if request.user.is_authenticated:
        return render(request, "muebles/muebles.html")

    elif (request.method == "POST"):
        email = request.POST['email']
        psw = request.POST['psw']
        user = backend.authenticate(email=email, password=psw)

        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return redirect("login")

    else:
        return render(request, "muebles/login.html")


@login_required
def bookMueble(request, mueble_id):
    mueble = Mueble.objects.get(pk=mueble_id)
    if (request.method == "POST" and mueble.demandante is None):
        mueble.demandante = request.user
        mueble.save()
        return redirect(f"/{mueble_id}/post")
    else:
        return redirect("/")


@login_required
def modifyMueble(request, mueble_id):
    mueble = Mueble.objects.get(pk=mueble_id)
    fotoData = [mueble.main_image.url]
    fotos = Foto.objects.filter(mueble=mueble)
    for foto in fotos:
        fotoData.append(foto.imagen.url)
    context = {
            "action": 'modify',
            "mueble": mueble,
            "fotos": fotoData,
            }
    if (permisoModificar(request.user, mueble_id)):
        if (request.method == "POST"):
            mueble.nombre = request.POST['nombre']
            Foto.objects.filter(mueble=mueble).delete()
            fotos = request.FILES.getlist('files')
            mueble.main_image = fotos[0]
            mueble.descripcion = request.POST['desc']
            mueble.dimensiones = request.POST['dim']
            mueble.ubiInicial = request.POST['ubiI']
            mueble.save()

            for img in fotos[1:]:
                foto = Foto(mueble=mueble, imagen=img)
                foto.save()
            return redirect(f"/{mueble_id}/post")
        else:
            return render(request, "muebles/addMueble.html", context)
    return redirect("/")


@login_required
def addMueble(request):
    context = {
            'action': 'add',
            'fotos': '[]',
            }
    if (permisoAñadir(request.user)):
        if (request.method == "POST"):
            print(request.FILES)
            nombre = request.POST['nombre']
            fotos = request.FILES.getlist('files')
            main_img = fotos[0]
            dim = request.POST['dim']
            desc = request.POST['desc']
            ubiI = request.POST['ubiI']
            mueble = Mueble(nombre=nombre, main_image=main_img,
                            descripcion=desc, ubiInicial=ubiI,
                            ofertante=request.user, dimensiones=dim)
            mueble.save()
            for img in fotos[1:]:
                foto = Foto(mueble=mueble, imagen=img)
                foto.save()
            return redirect("/")
        else:
            return render(request, "muebles/addMueble.html", context)
    return redirect("/")


@login_required
def deleteMueble(request, mueble_id):
    if (request.method == "POST"):
        if (permisoModificar(request.user, mueble_id)):
            mueble = Mueble.objects.get(pk=mueble_id)
            mueble.delete()
        else:
            return HttpResponse('Unauthorized', status=401)
    return redirect("/")


@login_required
def logoutPage(request):
    logout(request)
    return redirect("/")


@login_required
def perfil(request):
    user = request.user
    listaMuebles = Mueble.objects.filter(ofertante=user)
    context = {
            "user": user,
            "listaMuebles": listaMuebles,
            }
    return render(request, "muebles/perfil.html", context)


@login_required
def post(request, mueble_id):
    mueble = Mueble.objects.get(pk=mueble_id)
    ofertante = mueble.ofertante
    demandante = mueble.demandante
    imagenes = [mueble.main_image]
    fotos = Foto.objects.filter(mueble=mueble)
    usuario = Usuario.objects.get(email=request.user)

    for foto in fotos:
        imagenes.append(foto.imagen)
    context = {
            'mueble': mueble,
            'ofertante': ofertante,
            'demandante': demandante,
            'images': imagenes,
            'user': usuario,
            }
    return render(request, "muebles/muebles.html", context)
```
___
# *Imports*:
## render y redirect:
>[!note] Render VS Redirect
> - **Render** es una función que lo que hace es cargar la página entera, es decir, es el que genera la respuesta http con la web que posteriormente el usuario visualizará, a render le podemos dar contexto y una página html directamente para que la cargue.
> - **Redirect** por el contrario lo que hace es una llamada GET a la página asociada a la url que especifiquemos, por tanto no carga nada, sino que llama a otra función que podría esta vez si cargar la página (es posible que esta otra función también haga un redirect, aunque lo más recomendable es que no vayamos de redirect en redirect).
> - El redirect también cambia la URL, si por ejemplo estuviéramos en login y hacemos un render de index veríamos en la url aún la página de login.
## login y logout:
Son funciones de Django para la autenticación, una registra al usuario y la otra cierra la sesión.
## login_required:
Como se ha explicado en la [[#*Introducción*|introducción]], el login_required sirve para especificar si que hay que estar registrado para acceder a esta página.
___
# *Funciones*:
## enviar_email:
Esta función sirve para poder enviar un mail al servicio propietario de la página, era un requisito de la aplicación.
```Python
def enviarEmail(demandante):
    smtpObj = smtplib.SMTP()

    sender = 'muebles@ejemplo.com'
    receivers = ['gehibey464@dacgu.com']

    smtpObj.sendmail(sender, receivers, message)
```
## permiso_añadir y permiso_modificar:
Estas funciones nos sirven para comprobar si el usuario que está accediendo por ejemplo a una página tiene acceso par añadir muebles, y dentro de los muebles para comprobar si tiene permiso para modificar estos muebles (Si son staff y el mueble es suyo, o si es superusuario).
```Python
def permisoAñadir(email):
    usuario = Usuario.objects.get(pk=email)
    return (usuario.is_staff or
            usuario.is_superuser)


def permisoModificar(email, mueble_id):
    mueble = Mueble.objects.get(pk=mueble_id)
    usuario = Usuario.objects.get(pk=email)
    return ((usuario.is_staff and usuario == mueble.ofertante) or
            usuario.is_superuser)
```
## index:
La página index es la página principal, en ella cargamos la página de muebles/muebles.html, muebles/muebles.html es un archivo html que contiene la vista de los muebles en forma de catálogo.

1. Obtenemos toda la lista de muebles ordenada por id.
2. Modificamos el contexto para enviar listaMuebles como una variable al archivo HTML.
3. Devolvemos la página renderizada con el contexto anteriormente mencionado. 

Aquí nos puede surgir la duda del contexto, qué es y para qué sirve, pues bien:
>[!important] Context
> El contexto es una serie de variables que le mandamos a la página para poder hacerla dinámica, es decir, cambiar los valores que tiene en función de lo que mandemos por la variable contexto.
> 
>  Para más información [[HTML]] contiene todo lo que podemos hacer con estas variables que mandamos, el contexto sólo es el diccionario de variables que va a recibir la página para luego poder usarlas dentro.


```Python
@login_required
def index(request):
    listaMuebles = Mueble.objects.order_by("-id")
    context = {
            "listaMuebles": listaMuebles,
            }
    return render(request, "muebles/muebles.html", context)
```
## login_page
La página login es la primera página que va a ver un usuario, ya que si no está registrado al acceder a index, le va a redirigir hasta esta, por el embellecedor @login_required.

1. Si el usuario está registrado e intenta acceder a login lo redirigimos hasta la página del catálogo.
2. Si no estuviera registrado y la petición es un post (Lo que quiere decir que estamos registrándonos en la página, la petición post la hace el formulario de usuario y contraseña).
	1. Comprobamos si hay un usuario registrado con ese mail y contraseña.
	2. Si lo hubiera (Si no es None el usuario devuelto por el authenticate) lo redirigimos hasta el índice, de nuevo el catálogo.
	3. Si no lo hubiera, lo redirigimos hasta login.
3. En cualquier otro caso volvemos a cargar render
```Python
def loginPage(request):
    if request.user.is_authenticated:
        return render(request, "muebles/muebles.html")

    elif (request.method == "POST"):
        email = request.POST['email']
        psw = request.POST['psw']
        user = backend.authenticate(email=email, password=psw)

        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return redirect("login")

    else:
        return render(request, "muebles/login.html")
```
## book_mueble
En esta función vemos una lógica más simple que en otras, básicamente es una página que hemos creado para poder reservar muebles.

Obtenemos el mueble en cuestión usando `Mueble.objects.get(pk=mueble_id)`, esta línea lo que hace es devolver el mueble cuya clave primaria coincide con la id del mueble que queremos reservar.

Posteriormente comprobamos si el mueble no tiene demandante, si no tuviese y estamos haciendo un "POST" (sinónimo de haber hecho click sobre el botón de reservar mueble).

Finalmente si no hemos hecho un POST o si hay demandante redireccionamos al usuario hacia la página inicial.
>[!note] ¿Error?
> Puede parecer que aquí hay un error en la lógica de la función, porque ¿y si hacemos un post y si tiene demandante? ¿Nos vamos a la página inicial? ¿No sería esto confuso?
>
> La respuesta es si, iríamos a la página principal, la cosa es que en nuestra página **sólo se muestra el botón de reservar si no tiene propietario**, por tanto para hacer un post a bookMueble habría que hacerlo a mano, cosa que un usuario común no haría.
> 
> En caso de que un usuario experimentado en html quisiera hacer un post a bookMueble de manera manual, pues si que lo redirigimos hacia la página principal.
```Python
@login_required
def bookMueble(request, mueble_id):
    mueble = Mueble.objects.get(pk=mueble_id)
    if (request.method == "POST" and mueble.demandante is None):
        mueble.demandante = request.user
        mueble.save()
        return redirect(f"/{mueble_id}/post")
    else:
        return redirect("/")
```
## modify_mueble:
Podemos ver que esta función es algo más larga que las demás, pero es muy sencilla en realidad, sólo tenemos que fijarnos en que la mitad de las líneas son para identificar los diferentes atributos de los muebles, y construir el contexto de la página (Porque vamos a mandar los valores actuales del mueble a la página, para poder usarlos como valor por defecto de los campos del formularios de modificación).
```Python
@login_required
def modifyMueble(request, mueble_id):
    mueble = Mueble.objects.get(pk=mueble_id)
    fotoData = [mueble.main_image.url]
    fotos = Foto.objects.filter(mueble=mueble)
    for foto in fotos:
        fotoData.append(foto.imagen.url)
    context = {
            "action": 'modify',
            "mueble": mueble,
            "fotos": fotoData,
            }
    if (permisoModificar(request.user, mueble_id)):
        if (request.method == "POST"):
            mueble.nombre = request.POST['nombre']
            Foto.objects.filter(mueble=mueble).delete()
            fotos = request.FILES.getlist('files')
            mueble.main_image = fotos[0]
            mueble.descripcion = request.POST['desc']
            mueble.dimensiones = request.POST['dim']
            mueble.ubiInicial = request.POST['ubiI']
            mueble.save()

            for img in fotos[1:]:
                foto = Foto(mueble=mueble, imagen=img)
                foto.save()
            return redirect(f"/{mueble_id}/post")
        else:
            return render(request, "muebles/addMueble.html", context)
    return redirect("/")
```
### Datos y contexto:
1. En esta primera parte, como hemos explicado antes, obtenemos el mueble que queremos modificar y lo guardamos en la variable mueble.
2. Posteriormente creamos fotoData, donde vamos a guardar todas las fotos que tienen que ver con el mueble, para comenzar le introducimos la url de la main_image, que está directamente en el mueble.
3. Obtenemos todas las fotos cuyo mueble es nuestro mueble, la diferencia entre get y filter es que **filter** devuelve **todas las ocurrencias que coinciden**, mientras que **get** se suele usar para obtener **únicamente una**, normalmente la que coincide con una clave primaria.
4. Obtenemos la url de todas las fotos y la vamos metiendo en fotoData.
5. Creamos el contexto a partir de todo lo obtenido anteriormente.
```Python
	mueble = Mueble.objects.get(pk=mueble_id)
    fotoData = [mueble.main_image.url]
    fotos = Foto.objects.filter(mueble=mueble)
    for foto in fotos:
        fotoData.append(foto.imagen.url)
    context = {
            "action": 'modify',
            "mueble": mueble,
            "fotos": fotoData,
   }
```
### Modificación:
1. Comprobamos si el usuario que ha hecho la petición tiene permisos para modificar.
2. Comprobamos si el usuario está haciendo una petición POST (Esto implicaría que ya está pidiendo modificar el mueble).
	1. Vamos modificando los valores de los atributos de mueble.
	2. Vemos que borramos todas las fotos que antes pertenecían al mueble, hacemos esto por si el usuario ha cambiado las fotos, actualizarlas.
	3. Asociamos la primera imagen al main_image del mueble.
	4. Todo lo demás hasta `mueble.save()` es evidente.
	5. Dentro del for lo que estamos haciendo es desde la segunda imagen (porque la primera pertenece al mueble) ir creando fotos y guardándolas en la base de datos.
	6. Finalmente redirigimos a los datos del mueble.
3. Si no fuese una petición POST, que significa que está pidiendo el formulario, no el envío de este, renderizamos la página addMueble con el contexto.
4. En caso de que no tenga permiso para modificar lo redireccionamos al catálogo.
```Python
if (permisoModificar(request.user, mueble_id)):
	if (request.method == "POST"):
		mueble.nombre = request.POST['nombre']
		Foto.objects.filter(mueble=mueble).delete()
		fotos = request.FILES.getlist('files')
		mueble.main_image = fotos[0]
		mueble.descripcion = request.POST['desc']
		mueble.dimensiones = request.POST['dim']
		mueble.ubiInicial = request.POST['ubiI']
		mueble.save()

		for img in fotos[1:]:
			foto = Foto(mueble=mueble, imagen=img)
			foto.save()
		return redirect(f"/{mueble_id}/post")
	else:
		return render(request, "muebles/addMueble.html", context)
return redirect("/")
```

## add_mueble:
Es prácticamente igual que modify, la diferencia está en que para poder reutilizar la página html, algunas partes de la página modify se hacen a partir del contexto, por ejemplo el nombre y los valores por defecto de los campos del formulario.
```Python
@login_required
def addMueble(request):
    context = {
            'action': 'add',
            'fotos': '[]',
            }
    if (permisoAñadir(request.user)):
        if (request.method == "POST"):
            print(request.FILES)
            nombre = request.POST['nombre']
            fotos = request.FILES.getlist('files')
            main_img = fotos[0]
            dim = request.POST['dim']
            desc = request.POST['desc']
            ubiI = request.POST['ubiI']
            mueble = Mueble(nombre=nombre, main_image=main_img,
                            descripcion=desc, ubiInicial=ubiI,
                            ofertante=request.user, dimensiones=dim)
            mueble.save()
            for img in fotos[1:]:
                foto = Foto(mueble=mueble, imagen=img)
                foto.save()
            return redirect("/")
        else:
            return render(request, "muebles/addMueble.html", context)
    return redirect("/")
```
## delete_mueble:
Esta función como su nombre indica sirve para borrar muebles, básicamente comprobamos si el usuario tiene permiso para poder borrar el mueble, y si es así lo borramos.

En caso de no tener permiso devolvemos un 401 (Un error de falta de permisos).

Si no fuese un post, lo reenviamos al catálogo, porque a esta página sólo se debería poder acceder mediante el botón de la página de los muebles.
```Python
@login_required
def deleteMueble(request, mueble_id):
    if (request.method == "POST"):
        if (permisoModificar(request.user, mueble_id)):
            mueble = Mueble.objects.get(pk=mueble_id)
            mueble.delete()
        else:
            return HttpResponse('Unauthorized', status=401)
    return redirect("/")
```
## logoutPage:
Llamamos a logut sobre la request y renderizamos el índex (que al no estar loggeados nos enviará a login).
```Python
@login_required
def logoutPage(request):
    logout(request)
    return redirect("/")
```
## perfil:
Perfil también es bastante básica, presenta la página del usuario y posterior a estos datos muestra un catálogo con todos los muebles del usuario, para poder acceder a ellos más fácilmente.

```Python
@login_required
def perfil(request):
    user = request.user
    listaMuebles = Mueble.objects.filter(ofertante=user)
    context = {
            "user": user,
            "listaMuebles": listaMuebles,
            }
    return render(request, "muebles/perfil.html", context)
```

## post:
Esta función también parece más de lo que es, de un mueble en específico obtenemos todos sus valores y luego cargamos la página de detalles del mueble con estos datos que hemos obtenido.
```Python
def post(request, mueble_id):
    mueble = Mueble.objects.get(pk=mueble_id)
    ofertante = mueble.ofertante
    demandante = mueble.demandante
    imagenes = [mueble.main_image]
    fotos = Foto.objects.filter(mueble=mueble)
    usuario = Usuario.objects.get(email=request.user)

    for foto in fotos:
        imagenes.append(foto.imagen)
    context = {
            'mueble': mueble,
            'ofertante': ofertante,
            'demandante': demandante,
            'images': imagenes,
            'user': usuario,
            }
    return render(request, "muebles/muebles.html", context)
```