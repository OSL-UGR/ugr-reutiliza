
# Fuente:
```python
from django.contrib import admin
from django.urls import include, path
from django.contrib.sitemaps.views import sitemap
from landing.sitemaps import LandingSitemap

sitemaps = {
    'landing': LandingSitemap,
}

urlpatterns = [
    path('', include("landing.urls"), name='landing'),
    path('admin/', admin.site.urls, name='admin'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
]
```

### Sitemaps:
El sitemap es un añadido de accesibilidad que hay que cumplir, es un archivo xml que nos permite acceder a todos los modelos que hay, en este caso sólo hemos añadido los de landing porque no tenemos más modelos.
### urlpatterns:
Aquí hemos metido las urls de landing en el root, con el nombre landing, las urls de admin en la dirección /admin y el sitemap en sitemap.xml.