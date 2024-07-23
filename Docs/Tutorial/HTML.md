En Django los HTML funcionan de una manera un poco diferente, hay tres características clave:
## Cláusulas static
En Django, cuando usamos un HTML, normalmente usamos lo siguiente:
```html
		{% load static %}
		<link rel="stylesheet" type="text/css" href="{% static 'styles/styles.css' %}"/>
```

Aunque parezca raro al principio, pronto nos damos cuenta de que es muchísimo más cómodo que la forma tradicional de hacerlo.

En este caso lo que tenemos básicamente es una aplicación que necesita su archivo de estilos, styles.css, en una aplicación normal tendríamos que importar ya sea el camino absoluto o relativo, lo cual puede dar muchos problemas a la hora de exportar el proyecto a otros dispositivos, sin tener en cuenta lo tedioso que es escribir tantas palabras para una sola ruta.

Aquí es donde entra en acción el static, static es una carpeta que debemos crear en nuestras aplicaciones, dentro de la cual estarán todos los elementos de la aplicación que tengan que ver con html, excluyendo el propio archivo html (Estos van en una carpeta llamada template).

Cuando nostros hacemos {% load static %} estamos informado a Django de que habrá lugares donde encuentre cláusulas como: 
```
	href="{% static 'styles/styles.css' %}"
```

De esta manera, cuando Django encuentra esta línea, lo que hace es buscar en la dirección static (Que podemos cambiar y definir a mano) el archivo styles.css, evitando así que tengamos que poner la dirección completa cada vez que queramos acceder a estos archivos.

También se usa para los archivos de JavaScript, imágenes...
___
## Lógica de Python:
Django nos permite, en html al igual que en python, utilizar bucles, ifs y la mayoría de lógicas en general, esto sirve para crear páginas que cambien dependiendo del contexto por ejemplo.

Si queremos que sólo se muestre un botón si tenemos permiso, o que se cambien valores en función del usuario, o para mostrar varias instancias de un objeto...
```html
	{% if elección == 1 %}
		<div>Código {{ variable }}</div>
	{% elif elección == 2 %}
		{% for elemento in elementos %}
			<p>{{ elementos.texto }}</p>
		{% endfor %}
		<div>Código html</div>
	{% else %}
		<div>Código html</div>
	{% endif %}
```
En el ejemplo anterior crearemos en función del valor de la variable "elección", escribiremos algo diferente dependiendo del valor de la variable "variable", y dependiendo de los elementos de elemento, escribiremos un texto diferente.

Es un ejemplo un poco complejo, pero básicamente es igual que programar en python, pero utilizando la nomenclatura anterior.
___
## Herencia:
Básicamente definimos en un html bloques, que luego extenderemos para sustituir esos bloques por código html más adelante, esto nos sirve por ejemplo para crear una página base e ir cambiando sólo la zona del contenido, manteniendo así footers y menús comunes.

En el html inicial pondremos.
### Página padre:
```html
<html lang="es-es">
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<title>Display Page</title>
		<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
		{% load static %}
		<link rel="stylesheet" type="text/css" href="{% static 'styles/styles.css' %}"/>
	</head>

	<body>
		{% block content %}

		{% endblock %}
		<a href="/sitemap.xml">Sitemap</a>
	</body>

</html>
```

Como vemos tenemos un bloque llamado content, pues en la página hija lo que haríamos sería extender el index, definiendo lo que hay dentro del content.

### Página hija:
```html
{% extends 'index.html' %}

{% block content %}
<p>Hola!</p>
{% endblock %}
```
Extendemos el index, y dentro del bloque content escribimos Hola!, que sería equivalente a tener la siguiente página:
### Resultado:
```html
<html lang="es-es">
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<title>Display Page</title>
		<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
		{% load static %}
		<link rel="stylesheet" type="text/css" href="{% static 'styles/styles.css' %}"/>
	</head>

	<body>
		<p>Hola!</p>
		<a href="/sitemap.xml">Sitemap</a>
	</body>

</html>
```
Y vemos que queda como una página entera, sin tener que repetir todo el código de la página índice, y podemos definir lo que se va a mostrar en la parte de contenido dependiendo de lo que busquemos.
___
