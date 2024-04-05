from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.loginPage, name="login"),
    path("logout", views.logoutPage, name="logout"),
    path("perfil", views.perfil, name="perfil"),
    path("add", views.addMueble, name="add"),
    path("<int:mueble_id>/post", views.post, name="post"),
]
