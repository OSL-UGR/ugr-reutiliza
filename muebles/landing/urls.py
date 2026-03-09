from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve


from . import views

urlpatterns = [
    
        # Pantalla de portada de la app, se muestra el nombre junto a los dos botonesde iniciar sesion o crear cuenta
        path("", views.portada, name="portada"),

        # Pantalla de inicio de la app, el tablón de anuncios
        path("catalogo", views.index, name="index"),

        # Pantalla de inicio de sesión y de crear cuenta
        path("login", views.loginPage, name="login"),
        path("registro", views.registroPage, name="registro"),

        # Acción para cerrar sesión
        path("logout", views.logoutPage, name="logout"),

        # Pantalla de perfil. Se muestra la información de el usuario y sus muebles. (posts)
        path("perfil", views.perfil, name="perfil"),

        # Formulario para añadir un nuevo mueble
        path("add", views.addMueble, name="add"),

        # Ver el detalle de un mueble concreto con mueble_id
        path("<int:mueble_id>/post", views.post, name="post"),

        # Borrar un mueble concreto con mueble_id
        path("<int:mueble_id>/delete", views.deleteMueble, name="delete"),

        # Modificar los parámetros de un mueble concreto con mueble_id
        path("<int:mueble_id>/modify", views.modifyMueble, name="modify"),

        # Reserva un mueble concreto con mueble_id
        path("<int:mueble_id>/book", views.bookMueble, name="book"),

        # Cancela una reserva con mueble_id
        path("<int:mueble_id>/unbook", views.unbookMueble, name="unbook"),

        path('<int:reserva_id>/entregado', views.marcar_entregado, name='marcar_entregado'),
        path('<int:reserva_id>/republicar', views.republicar_retrasado, name='republicar_retrasado'),

        # Panel de administrador personalizado:
        path("usuarios", views.gestion_usuarios, name="gestion_usuarios"),
        path("usuarios/delete/<str:email>", views.delete_usuario, name="delete_usuario"),
        path("usuarios/add_user", views.add_user, name = 'add_user'),


        re_path(r'^media/(?P<path>.*)$', serve, {'document_root':
                                                 settings.MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root':
                                                  settings.STATIC_ROOT}),
        ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
