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
