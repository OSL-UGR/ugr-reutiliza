# In your landing app's sitemaps.py
from django.contrib import sitemaps
from .models import Foto, Mueble


class LandingSitemap(sitemaps.Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return list(Foto.objects.all()) + list(Mueble.objects.all())

    def location(self, obj):
        if isinstance(obj, Foto):
            return obj.get_absolute_url()  # Assuming you have a method to get the URL for a Foto instance
        elif isinstance(obj, Mueble):
            return obj.get_absolute_url()  # Assuming you have a method to get the URL for a Mueble instance
