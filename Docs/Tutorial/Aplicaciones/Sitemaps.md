En un archivo sitemap, lo que configuramos es cómo nuestros modelos se "traducen" por decirlo así, a URLs.

Esto lo podemos hacer de la siguiente forma:
```Python
class LandingSitemap(sitemaps.Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return list(Foto.objects.all()) + list(Mueble.objects.all())

    def location(self, obj):
        if isinstance(obj, Foto):
            return obj.get_absolute_url()
        elif isinstance(obj, Mueble):
            return obj.get_absolute_url()  
```

Podemos ver que nuestro sitemap va a ser actualizado semanalmente, que para devolver los items del sitemap devolvemos una lista con todos los objetos de nuestros dos modelos principales, y que location devuelve, en función del tipo de objeto, una URL u otra (En nuestro caso las funciones tienen el mismo nombre, y hemos tenido que definirlas previamente).

Por tanto lo que conseguiremos es tener una lista de enlaces a todos nuestros modelos que no son tan accesibles de otra manera.