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
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root':
                                                 settings.MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root':
                                                  settings.STATIC_ROOT}),
        ]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
