from django.shortcuts import render, redirect
from .models import Mueble, Foto
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .backends import SettingsBackend


backend = SettingsBackend()


@login_required
def index(request):
    listaMuebles = Mueble.objects.order_by("-id")
    context = {
            "listaMuebles": listaMuebles,
            }
    print(context)
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
def addMueble(request):
    context = {}
    if (request.method == "POST"):
        nombre = request.POST['nombre']
        fotos = request.FILES.getlist('fotos')
        main_img = fotos[0]
        desc = request.POST['desc']
        ubiI = request.POST['ubiI']
        mueble = Mueble(nombre=nombre, main_image=main_img,
                        descripcion=desc, ubiInicial=ubiI,
                        ofertante=request.user)
        mueble.save()
        for img in fotos[1:]:
            foto = Foto(mueble=mueble, imagen=img)
            foto.save()
        print(request.user.pk)
        context = {'a': "a"}
    return render(request, "muebles/addMueble.html", context)


@login_required
def logoutPage(request):
    logout(request)
    return redirect("/")


@login_required
def perfil(request):
    user = request.user
    context = {
            "user": user,
            }
    return render(request, "muebles/perfil.html", context)


@login_required
def post(request, mueble_id):
    mueble = Mueble.objects.get(pk=mueble_id)
    ofertante = mueble.ofertante
    imagenes = [mueble.main_image]
    fotos = Foto.objects.filter(mueble=mueble)
    for foto in fotos:
        imagenes.append(foto.imagen)
    print(imagenes)
    context = {
            'mueble': mueble,
            'ofertante': ofertante,
            'images': imagenes,
            }
    return render(request, "muebles/muebles.html", context)
