from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve


from . import views

urlpatterns = [
    
        # Pantalla de inicio de la app, el tablón de anuncios
        path("", views.index, name="index"),

        # Pantalla de inicio de sesión
        path("login", views.loginPage, name="login"),

        # Acción para cerrar sesión
        path("logout", views.logoutPage, name="logout"),

        # Pantalla de perfil. Se muestra la información de el usuario y sus muebles. (posts)
        path("perfil", views.perfil, name="perfil"),

        # Formulario para añadir un nuevo mueble
        path("add", views.addMueble, name="add"),

        # Ver el detalle de un mueble concreto con mueble_id
        path("<int:mueble_id>/post", views.post, name="post"),

        # Borrar un mueble concreto con mueble_id
        #TODO: Debería comprobar que solo pudes borrar tus propios muebles (a no ser que seas admin)
        path("<int:mueble_id>/delete", views.deleteMueble, name="delete"),

        # Modificar los parámetros de un mueble concreto con mueble_id
        #TODO: debería comprobar que solo puedes modificar tus propios muebles (a no ser que seas admin)
        path("<int:mueble_id>/modify", views.modifyMueble, name="modify"),

        # Reserva un mueble concreto con mueble_id
        #TODO: Debería comprobar que no puedes reservar un mueble propio 
        path("<int:mueble_id>/book", views.bookMueble, name="book"),

        # Cancela una reserva con mueble_id
        #TODO: Debería comprobar que solo puedes cancelar una reserva propia
        path("<int:mueble_id>/unbook", views.unbookMueble, name="unbook"),


        #TODO: encontrar el html o e que caso borraríamos solo escribiendo el id y quitar esto. Debería siempre usarse la anterior ruta
        path("<int:mueble_id>/", views.deleteMueble, name="delete"),

        # TODO Panel de administrador personalizado:
        # Añadir aquí las futuras rutas para gestionar usuarios. 
        # Ejemplo: path("admin-usuarios/", views.lista_usuarios, name="lista_usuarios"),
        # path("admin-usuarios/add", views.add_usuario, name="add_usuario"), etc.


        re_path(r'^media/(?P<path>.*)$', serve, {'document_root':
                                                 settings.MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root':
                                                  settings.STATIC_ROOT}),
        ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
