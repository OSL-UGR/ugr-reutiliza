from django.shortcuts import render
from .models import Mueble


def index(request):
    listaMuebles = Mueble.objects.order_by("-id")
    context = {
            "listaMuebles": listaMuebles,
            }
    return render(request, "index.html", context)


def login(request):
    return render(request, "login.html")


def post(request, mueble_id):
    context = {
            'mueble': Mueble.objects.get(pk=mueble_id),
            }
    return render(request, "index.html", context)
