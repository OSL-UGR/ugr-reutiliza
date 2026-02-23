from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from .backends import SettingsBackend
from .models import Mueble, Foto, Usuario, Reserva, categorias as cat
from threading import Thread
import smtplib
from email.mime.text import MIMEText


URL = ''
backend = SettingsBackend()

port = 587
smtp_server = "smtp.ugr.es"

file = open(str(settings.BASE_DIR) + "/credentials.txt", "r")

# Estos 3 parámetros son los que hemos rellenado dentro de credentials.txt
email = file.readline().strip('\n')
password = file.readline().strip('\n')
inventoryEmail = file.readline().strip('\n')
file.close()

# Prepara el mensaje del correo de inventarioReserva
def mensajeInventarioReserva(nombreMueble, cantidad,
                             demandante, puesto, organizacion, correo,
                             correoInventario):

    text = f"""\
    {demandante}, {puesto}, de {organizacion} con correo {correo}
    solicita {cantidad} del mueble {nombreMueble}.
    """

    message = MIMEText(text, "plain")
    message["Subject"] = f"Reserva {nombreMueble}"
    message["From"] = email
    message["To"] = correoInventario
    return message

# Prepara el mensaje del correo de inventarioReserva
def mensajeLiberacion(nombre, cantidad, demandante, correo, receptor,
                      restantes):
    text = f"""\
    El usuario {demandante} con correo {correo} ha liberado
    {cantidad} elementos de este mueble.

    Ahora quedan {restantes}.
    """

    # Create MIMEText object
    message = MIMEText(text, "plain")
    message["Subject"] = f"Liberacion reserva {nombre}"
    message["From"] = email
    message["To"] = receptor

    return message

# Prepara el mensaje del correo de mensajeReserva
def mensajeReserva(nombre, cantidad, demandante, correo, receptor,
                   restantes):
    text = f"""\
    El usuario {demandante} con correo {correo} ha reservado
    {cantidad} elementos de este mueble.

    Ahora quedan {restantes}.
    """

    # Create MIMEText object
    message = MIMEText(text, "plain")
    message["Subject"] = f"Nueva reserva {nombre}"
    message["From"] = email
    message["To"] = receptor

    return message


# Envía un email, los mensajes base son las funciones anteriores a esta.
def sendMail(email, password, message, receptor):
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        server.starttls()
        server.login(email, password)
        server.sendmail(email, receptor, message.as_string())
        server.close()


def mueblesCat(listaCat):
    muebles = Mueble.objects.filter(categoria__in=listaCat)

    return muebles

# Solo el personal de administración (is_staff o is_superuser) pueden modificar muebles
def permisoAñadir(email):
    usuario = Usuario.objects.get(pk=email)
    return (usuario.is_staff or
            usuario.is_superuser)

# Puedes modificar un anuncio si: eres "is_superuser" o eres "is_staff" y el anuncio es tuyo.
def permisoModificar(email, mueble_id):
    mueble = Mueble.objects.get(pk=mueble_id)
    usuario = Usuario.objects.get(pk=email)
    return ((usuario.is_staff and usuario == mueble.ofertante) or
            usuario.is_superuser)

# Tablón principal.
@login_required
def index(request):

    listaMuebles = Mueble.objects.order_by("-id") # El -id devuelve los muebles del ás nuevo al más antiguo.
    categorias = [] 

    # Contamos cuántos muebles hay de cada categoría
    for i in range(len(cat)):
        muebles = Mueble.objects.filter(categoria=cat[i][0])
        categorias.insert(i, {"muebles": muebles,
                              "text": cat[i][0],
                              "num": len(muebles)})

    # Comprueba si el usuario ha realizado algún check para filtrar solo los muebles de x categoría 
    seleccionadas = request.GET.getlist('checks')

    # Si ha filtrado, solo devolvemos esos muebles
    if (len(seleccionadas) != 0):
        print(seleccionadas)
        listaMuebles = mueblesCat(seleccionadas)

    # Si no ha filtrado, mostramos todos los muebles de todas las categorías
    else:
        seleccionadas = categorias

    context = {
            "listaMuebles": listaMuebles,
            "categorias": categorias,
            "selected": seleccionadas,
            "URL": URL
            }
    
    # Envíamos los muebles a muebles.html
    return render(request, "muebles/muebles.html", context)

# Página de inicio de sesión
def loginPage(request):
    context = {
            "URL": URL,
            }
    # Si ya está loqueado e intenta acceder a /login, le redirigimos la página de inicio para que no pueda 
    if request.user.is_authenticated:

        return redirect("index")    

    # Si lanzamos un POST (iniciamos la comprobación de inicio de sesión)
    elif (request.method == "POST"):
        email = request.POST['email']
        psw = request.POST['psw']
        user = backend.authenticate(email=email, password=psw)

        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return redirect("login")

    # Lanzamos un GET (se muestra el html de login base)
    else:
        return render(request, "muebles/login.html", context)


@login_required
def unbookMueble(request, mueble_id):
    mueble = Mueble.objects.get(pk=mueble_id)
    reservas = Reserva.objects.filter(mueble=mueble)
    reserva = Reserva.objects.get(mueble=mueble, demandante=request.user)

    total = 0
    for res in reservas:
        total += res.cantidad

    restantes = mueble.cantidad - total
    demandante = reserva.demandante

    if (request.method == "POST"):
        mensaje = mensajeLiberacion(mueble.nombre, reserva.cantidad,
                                    demandante.nombre + " " +
                                    demandante.apellidos,
                                    demandante.email, mueble.ofertante.email,
                                    restantes + reserva.cantidad)

        Thread(target=sendMail,
               args=(email, password, mensaje, mueble.ofertante.email)).start()
        reserva.delete()
        return redirect(f"/{URL}{mueble_id}/post")
    else:
        return redirect("index")

# Función que reserva un mueble
@login_required
def bookMueble(request, mueble_id):
    # Cargamos el mueble y todas las reservas que exixten para este
    mueble = Mueble.objects.get(pk=mueble_id)
    reservas = Reserva.objects.filter(mueble=mueble)

    #Obtenemos cuantos items quiere el usuario
    peticion = int(request.POST['cantRes'])
    existente = False

    total = 0
    # Recorremos todas las reservas para contabilizar cuantas unidades están ocupadas.  
    for reserva in reservas:
        #Identifica si el usuario ya había reservado anteriormente de ese mueble
        if (reserva.demandante == request.user):
            reservaUser = reserva
            existente = True
        total += reserva.cantidad

    # Vemos cuantos quedan libres
    restantes = mueble.cantidad - total
    demandante = Usuario.objects.get(pk=request.user)

    # Si hay stock disponible gestionamos la reserva
    if (request.method == "POST" and restantes - peticion >= 0):
        #Si ya tenía una reserva, simplemente sumamos la nueva cantidad solicitada
        if (existente):
            reserva = reservaUser
            reserva.cantidad += peticion
        else:
            #Definimos la reserva
            reserva = Reserva(mueble=mueble, cantidad=peticion,
                              demandante=request.user)
            
        # Obtenemos el nombre del demandante
        nombreDemandante = demandante.nombre + " " + demandante.apellidos

        #Definimos ellos mensajes de la reserva y envíamos el email corespondiente
        mensaje = mensajeReserva(mueble.nombre, peticion,
                                 nombreDemandante, demandante.email,
                                 mueble.ofertante.email, restantes - peticion)

        Thread(target=sendMail,
               args=(email, password, mensaje, mueble.ofertante.email)).start()
        
        mensaje = mensajeInventarioReserva(mueble.nombre, peticion,
                                           nombreDemandante,
                                           demandante.puesto,
                                           demandante.organizacion,
                                           demandante.email, inventoryEmail)
        Thread(target=sendMail,
               args=(email, password, mensaje, inventoryEmail)).start()
        reserva.save()

        return redirect(f"/{URL}{mueble_id}/post")
    
    #No gestionamos la reserva, no hay stock suficiente y redirigimos a index
    #TODO: mostrar mensaje de advertencia de que no se ha podido gestionar la reserva por falta de stock
    else:
        return redirect("index")


@login_required
def modifyMueble(request, mueble_id):
    mueble = Mueble.objects.get(pk=mueble_id)
    fotoData = [mueble.main_image.url]
    fotos = Foto.objects.filter(mueble=mueble)
    for foto in fotos:
        fotoData.append(foto.imagen.url)

    categorias = []
    for i in range(len(cat)):
        categorias.insert(i, cat[i][0])

    context = {
            "action": 'modify',
            "categorias": categorias,
            "mueble": mueble,
            "fotos": fotoData,
            "URL": URL
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
            mueble.cantidad = request.POST['cant']
            mueble.categoria = request.POST['cat']
            mueble.save()

            for img in fotos[1:]:
                foto = Foto(mueble=mueble, imagen=img)
                foto.save()
            return redirect(f"/{URL}{mueble_id}/post")
        else:
            return render(request, "muebles/addMueble.html", context)
    return redirect("index")


@login_required
def addMueble(request):
    categorias = []

    for i in range(len(cat)):
        categorias.insert(i, cat[i][0])
    context = {
            'action': 'add',
            'fotos': '[]',
            'categorias': categorias,
            'URL': URL
            }
    
    # Limitamos el acceso de añadir un mueble dentro de permisoAñadir(...)
    if (permisoAñadir(request.user)):
        #Identificamos los datos obtenidos del fortmulario y los recogemos
        if (request.method == "POST"):
            print(request.FILES)
            nombre = request.POST['nombre']
            fotos = request.FILES.getlist('files')
            main_img = fotos[0] # La primera foto del listado de fotos será la portada del anuncio
            dim = request.POST['dim']
            desc = request.POST['desc']
            ubiI = request.POST['ubiI']
            cant = request.POST['cant']
            categ = request.POST['cat']
            mueble = Mueble(nombre=nombre, main_image=main_img,
                            descripcion=desc, ubiInicial=ubiI,
                            ofertante=request.user, dimensiones=dim,
                            cantidad=cant, categoria=categ)
            mueble.save()
            # Guardamos el resto de fotos tb
            for img in fotos[1:]:
                foto = Foto(mueble=mueble, imagen=img)
                foto.save()
            return redirect("index")
        else:
            # Lanzamos un GET para mostrar el formulario de añadir mueble vacío
            return render(request, "muebles/addMueble.html", context)
    return redirect("index")


# TODO: muy importante, ahora mismo no se puede eliminar un mueble que alguien ya ha reservado ya que PostgreS evitará lanzar un IntegrityError
@login_required
def deleteMueble(request, mueble_id):
    if (request.method == "POST"):
        if (permisoModificar(request.user, mueble_id)):
            mueble = Mueble.objects.get(pk=mueble_id)
            mueble.delete()
        else:
            return HttpResponse('Unauthorized', status=401)
    return redirect("index")

# Destruye la cookie de sesión y redirijimos a index
@login_required
def logoutPage(request):
    logout(request)
    return redirect("index")

# Pantalla de perfil (solo puedes ver tu perfil)
@login_required
def perfil(request):
    user = request.user
    listaMuebles = Mueble.objects.filter(ofertante=user)
    context = {
            "user": user,
            "listaMuebles": listaMuebles,
            "URL": URL
            }
    return render(request, "muebles/perfil.html", context)

# Prepara todos los atributos de información sobre un mueble para mostrarlos, dado el id de un mueble
@login_required
def post(request, mueble_id):

    # Obtenemos el mueble, quien es el ofertante y cuantas reservas tiene
    mueble = Mueble.objects.get(pk=mueble_id)
    ofertante = mueble.ofertante
    reservas = Reserva.objects.filter(mueble=mueble)

    # Calculamos la disponibilidad de el mueble
    total = 0
    demandantes = []
    for reserva in reservas:
        demandantes.append(reserva.demandante) # Para ver quienes han demandado el mueble
        total += reserva.cantidad

    # Vemos si el usuario logueado, tiene ya una reserva o no. Para definir una acción en el html.
    try:
        reserva = Reserva.objects.get(mueble=mueble, demandante=request.user)
    except:
        reserva = None


    # Crea la lista de imágenes definiendo la primera como la portada
    imagenes = [mueble.main_image]
    fotos = Foto.objects.filter(mueble=mueble)
    usuario = Usuario.objects.get(email=request.user)

    for foto in fotos:
        imagenes.append(foto.imagen)

    # Pasamos los atributos al html
    context = {
            'restantes': mueble.cantidad - total,
            'mueble': mueble,
            'ofertante': ofertante,
            'reservas': reservas,
            'reserva': reserva,
            'demandantes': demandantes,
            'images': imagenes,
            'user': usuario,
            "URL": URL
            }
    return render(request, "muebles/muebles.html", context)


# Función que comprueba si el usuario es un super usuario
def es_superusuario(user):
    return user.is_superuser

@login_required
@user_passes_test(es_superusuario, login_url='index') # Si no es superuser, lo manda al index
def gestion_usuarios(request):

    # Obtenemos la lista de los usuarios
    lista_usuarios = Usuario.objects.all().order_by('email')
    
    context = {
        "lista_usuarios": lista_usuarios,
        "URL": URL
    }
    
    return render(request, "muebles/gestion_usuarios.html", context)


#TODO: queda por implementar
@login_required
@user_passes_test(es_superusuario, login_url='index')
def delete_usuario(request, email):

    return redirect("gestion_usuarios")
