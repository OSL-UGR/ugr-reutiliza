from django.shortcuts import render, redirect
from .models import Mueble, Usuario
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
        foto = request.POST['foto']
        desc = request.POST['desc']
        ubiI = request.POST['ubiI']
        mueble = Mueble(nombre=nombre, foto=foto,
                        descripcion=desc, ubiInicial=ubiI,
                        ofertante=request.user)
        print(request.user.pk)
        mueble.save()
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
    context = {
            'mueble': mueble,
            'ofertante': ofertante,
            }
    return render(request, "muebles/muebles.html", context)
