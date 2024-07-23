# Contenido:
## [[urls.py|URL]]:
El archivo [[urls.py|urls.py]] es el archivo en el que guardamos las direcciones relativas de la aplicación.

En este archivo será donde configuremos cómo acceder a las diferentes funcionalidades, cuando añadamos estas URLs a las de la aplicación serán relativas a la dirección que les asignemos.
___
## [[views.py|Views]]:
El archivo [[views.py]] es el archivo en el que podremos definir la mayoría de las funcionalidades de nuestras páginas (La funcionalidad final es una combinación de JavaScript, [[HTML#Lógica de Python|la lógica de Python en HTML]] y otros componentes).

Para poder asignar la funcionalidad a una página, previamente tendremos que haberlas configurado en el archivo [[urls.py|urls.py]], lo que no exista en este archivo, no será asignado de ninguna manera a una web.
___
## [[models.py|Models]]:
El archivo [[models.py]] es donde podemos definir las entidades que posteriormente usaremos en la aplicación.

Para poder tener usuarios, almacenar datos y todo lo que debería hacer una aplicación web funcional, debemos usar modelos (Normalmente tendremos que definir los nuestros propios).
___
## [[managers.py|Managers]]:
El archivo [[managers.py]] sirve para cómo se crean algunas entidades (En nuestro caso usuarios y superusuarios).
___
## [[admin.py|Admin]]:
En el archivo [[admin.py]] definimos la vista de la aplicación admin de Django en relación a nuestras aplicaciones, es decir, podremos definir cómo nuestros modelos se modifican en la aplicación admin, que es una aplicación de control que provee Django.

Es muy necesario si vamos a, por ejemplo, crear usuarios, para poder cambiar sus permisos, poder añadir y borrar usuarios, aunque también otras entidades.
___
## [[sitemaps.py|Sitemaps]]:
En el archivo [[sitemaps.py]] es donde vamos a definir cómo nuestros modelos se crean en la página sitemap, una página que es necesaria para cumplir los estándares de [accesibilidad](https://github.com/Alux6/oaw) (revísa el fork q hice de una aplicación de análisis de accesibilidad ¿no?).

Como en la anterior, definimos cómo nuestros modelos se traducen a enlaces, para poder añadirlos en estos sitemaps.
___
## [[forms.py|Forms]]:
___
## [[Templates]]:
___
## [[styles.css|Styles]]