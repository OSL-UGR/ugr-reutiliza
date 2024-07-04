from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .backends import SettingsBackend
from .models import Mueble, Foto, Usuario, Reserva, categorias as cat
from threading import Thread
import smtplib
from email.mime.text import MIMEText


URL = 'muebles/'
backend = SettingsBackend()

port = 587
smtp_server = "smtp.ugr.es"

file = open(str(settings.BASE_DIR) + "/credentials.txt", "r")
email = file.readline().strip('\n')
password = file.readline().strip('\n')
inventoryEmail = file.readline().strip('\n')
file.close()


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
    categorias = []
    for i in range(len(cat)):
        muebles = Mueble.objects.filter(categoria=cat[i][0])
        categorias.insert(i, {"muebles": muebles,
                              "text": cat[i][0],
                              "num": len(muebles)})

    seleccionadas = request.GET.getlist('checks')
    if (len(seleccionadas) != 0):
        print(seleccionadas)
        listaMuebles = mueblesCat(seleccionadas)
    else:
        seleccionadas = categorias

    context = {
            "listaMuebles": listaMuebles,
            "categorias": categorias,
            "selected": seleccionadas,
            "URL": URL
            }
    return render(request, "muebles/muebles.html", context)


def loginPage(request):
    context = {
            "URL": URL,
            }
    if request.user.is_authenticated:
        return render(request, "muebles/muebles.html", context)

    elif (request.method == "POST"):
        email = request.POST['email']
        psw = request.POST['psw']
        user = backend.authenticate(email=email, password=psw)

        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return redirect("login")

    else:
        return render(request, "muebles/login.html", context)


@login_required
def unbookMueble(request, mueble_id):
    mueble = Mueble.objects.get(pk=mueble_id)
    reservas = Reserva.objects.filter(mueble=mueble)
    reserva = Reserva.objects.get(mueble=mueble, demandante=request.user)

    total = 0
    for reserva in reservas:
        total += reserva.cantidad

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


@login_required
def bookMueble(request, mueble_id):
    mueble = Mueble.objects.get(pk=mueble_id)
    reservas = Reserva.objects.filter(mueble=mueble)

    peticion = int(request.POST['cantRes'])
    existente = False

    total = 0
    for reserva in reservas:
        if (reserva.demandante == request.user):
            reservaUser = reserva
            existente = True
        total += reserva.cantidad

    restantes = mueble.cantidad - total
    demandante = Usuario.objects.get(pk=request.user)

    if (request.method == "POST" and restantes - peticion >= 0):
        if (existente):
            reserva = reservaUser
            reserva.cantidad += peticion
        else:
            reserva = Reserva(mueble=mueble, cantidad=peticion,
                              demandante=request.user)
        nombreDemandante = demandante.nombre + " " + demandante.apellidos
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
    if (permisoAñadir(request.user)):
        if (request.method == "POST"):
            print(request.FILES)
            nombre = request.POST['nombre']
            fotos = request.FILES.getlist('files')
            main_img = fotos[0]
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
            for img in fotos[1:]:
                foto = Foto(mueble=mueble, imagen=img)
                foto.save()
            return redirect("index")
        else:
            return render(request, "muebles/addMueble.html", context)
    return redirect("index")


@login_required
def deleteMueble(request, mueble_id):
    if (request.method == "POST"):
        if (permisoModificar(request.user, mueble_id)):
            mueble = Mueble.objects.get(pk=mueble_id)
            mueble.delete()
        else:
            return HttpResponse('Unauthorized', status=401)
    return redirect("index")


@login_required
def logoutPage(request):
    logout(request)
    return redirect("index")


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


@login_required
def post(request, mueble_id):
    mueble = Mueble.objects.get(pk=mueble_id)
    ofertante = mueble.ofertante
    reservas = Reserva.objects.filter(mueble=mueble)

    total = 0
    demandantes = []
    for reserva in reservas:
        demandantes.append(reserva.demandante)
        total += reserva.cantidad

    try:
        reserva = Reserva.objects.get(mueble=mueble, demandante=request.user)
    except:
        reserva = None

    imagenes = [mueble.main_image]
    fotos = Foto.objects.filter(mueble=mueble)
    usuario = Usuario.objects.get(email=request.user)

    for foto in fotos:
        imagenes.append(foto.imagen)
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
