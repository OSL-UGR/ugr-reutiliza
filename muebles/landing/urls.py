from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:mueble_id>/post", views.post, name="post"),
]
