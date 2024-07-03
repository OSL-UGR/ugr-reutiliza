from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve


from . import views

urlpatterns = [
        path("", views.index, name="index"),
        path("login", views.loginPage, name="login"),
        path("logout", views.logoutPage, name="logout"),
        path("perfil", views.perfil, name="perfil"),
        path("add", views.addMueble, name="add"),
        path("<int:mueble_id>/post", views.post, name="post"),
        path("<int:mueble_id>/delete", views.deleteMueble, name="delete"),
        path("<int:mueble_id>/modify", views.modifyMueble, name="modify"),
        path("<int:mueble_id>/book", views.bookMueble, name="book"),
        path("<int:mueble_id>/unbook", views.unbookMueble, name="unbook"),
        path("<int:mueble_id>/", views.deleteMueble, name="delete"),
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root':
                                                 settings.MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root':
                                                  settings.STATIC_ROOT}),
        ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
