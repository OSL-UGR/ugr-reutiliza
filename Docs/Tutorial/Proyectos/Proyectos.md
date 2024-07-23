El proyecto es la parte central de Django, en él se encuentran la gran mayoría de configuraciones:
- Configuración de la base de datos
- Configuración de aplicaciones
- Configuración de Django
- Rutas absolutas y relativas

Un proyecto en Python consta de varias partes:
___
## [[URLs]]
En esta sección, a diferencia de como se ve en las aplicaciones, únicamente definimos a qué dirección hay que asignar las direcciones de las aplicaciones, por ejemplo:

```Python
urlpatterns = [
    path('', include("landing.urls"), name='landing'),
    path('admin/', admin.site.urls, name='admin'),
]
```

El ejemplo anterior consiste de dos aplicaciones:
1. Landing, que se monta sobre las ruta original, esto quiere decir que el formato de cualquier url de landing será: http://127.0.0.1/
2. Admin, que se monta sobre la ruta admin/, lo que significa que cualquier página de admin comenzará con: http://127.0.0.1/admin/
___
## Settings
En este archivo, lo que hacemos es avisar a Django de las aplicaciones que vamos a usar, de las diferentes rutas que queremos que tenga en cuenta, si está en modo Debug, qué base de datos debe usar y dónde está...