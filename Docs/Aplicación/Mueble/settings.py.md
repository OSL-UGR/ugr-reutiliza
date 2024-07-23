# *Fuente*:
```python
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!ps7i_pycpqk)@2flqesc7=6xby0r1#vi+*uv%d_jt+v4*nshy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Application definition

INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django_extensions',
        'django.contrib.sitemaps',
        'landing'
        ]

MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ]

ROOT_URLCONF = 'muebles.urls'

TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    ],
                },
            },
        ]

WSGI_APPLICATION = 'muebles.wsgi.application'

ALLOWED_HOSTS = ['127.0.0.1', '172.*.*.*']

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# La base de datos de desarrollo ha sido creada en un container
# El comando sería:
# docker run --name postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres

# Es importante que antes de desplegar la web exista una base de datos con el nombre
# que haya en el campo 'NAME'.

# Se haría con "CREATE DATABASE mueblesitos;" en este caso
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'mueblesitos',
            'USER': 'postgres',
            'PASSWORD': 'password',
            'HOST': '127.0.0.1',
            'PORT': '5432',
            }
        }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
AUTH_USER_MODEL = 'landing.Usuario'
LOGIN_URL = 'login'

AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
            },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
            },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
            },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
            },
        ]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

GRAPH_MODELS = {

        }

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = "/media/"

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'landing/static')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```
___
# *Campos*:
Hay muchos campos dentro de este archivo, así que este archivo hay que leerlo con calma.
## BASE_DIR:
El campo base_dir que viene por defecto en los proyectos de Django es el que especifica la dirección por defecto, suele ser dos directorios por encima del directorio que contiene las aplicaciones.
## SECRET_KEY:
La variable secret_key se usa para hacer [hashings](https://stackoverflow.com/a/7382198), es muy importante ocultar esta clave al publicar la aplicación, en este caso la hemos dejado expuesta porque es un proyecto en producción, que no ha sido desplegado aún.

En caso de desplegarlo lo más seguro sería guardarlo en un archivo externo y acceder a ese archivo desde el código, guardando el código en una zona que no se publicaría en el repositorio público.
## DEBUG:
En Django se usa el Debug para que en lugar de romperse y ya, dé información importante durante el período de desarrollo, por ejemplo otras páginas a las que si se puede acceder, el código de error.
## INSTALLED_APPS:
En installed apps listamos las aplicaciones que queremos usar, algunas vienen por defecto y otras como **landing** y **sitemaps** las hemos añadido.
```Python
INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django_extensions',
        'django.contrib.sitemaps',
        'landing'
        ]
```
## MIDDLEWARE:
La variable middleware provee de diferentes funcionalidades a los programas, por poner un ejemplo sacado de la página de la [documentación](https://docs.djangoproject.com/en/5.0/topics/http/middleware/) dedicada a esto, AuthenticationMiddleware permite asociar la sesión con las peticiones a la página.
```Python
MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ]
```
## ROOT_URLCONF:
Esta variable especifica dónde están las urls raíz, es decir, dónde está la configuración de urls que definirá la relación de todas las demás aplicaciones con la web.
## TEMPLATES:
Este archivo es el que nos proporciona toda la funcionalidad descrita anteriormente en [[HTML]].

Básicamente es el archivo que provee de todas las partes dinámicas a las aplicaciones Django (como poder escribir variables, usar for y este tipo de cosas dentro del propio html).
```Python
TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    ],
                },
            },
        ]
```
## WSGI_APPLICATION:
Es una configuración necesaria, se asigna de manera automática, se puede obviar.
```Python
WSGI_APPLICATION = 'muebles.wsgi.application'
```
## ALLOWED_HOSTS:
Define los hosts a los que el servidor dará servicio.
```Python
ALLOWED_HOSTS = ['127.0.0.1', '172.*.*.*']
```
## DATABASES:
Esta configuración sirve para definir la base de datos que queremos usar en la web de Django, en el caso del ejemplo usamos postgres.
```Python
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'mueblesitos',
            'USER': 'postgres',
            'PASSWORD': 'password',
            'HOST': '127.0.0.1',
            'PORT': '5432',
            }
        }
```
## AUTH_USER_MODEL:
Esta variable define qué modelo va a ser el que se use para la autenticación.
## LOGIN_URL:
Esta variable define en qué url se hace el login.
## AUTH_PASSWORD_VALIDATORS:
El auth password validator es el que implementa toda la funcionalidad de Django sobre el tema de las contraseñas, si son demasiado comunes, demasiado cortas, si sólo son numéricas...
```Python
AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
            },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
            },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
            },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
            },
]
```
## Configuraciones comunes:
### Idioma y regiones.
Sirve para compatibilizar la página.
``` Python
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

GRAPH_MODELS = {

        }
```
### Fotos, estilos...
Estas configuraciones sirven para especificar dónde guardamos las imágenes (La carpeta media es la carpeta que se suele usar para guardar archivos en general que no son permanentes, por ejemplo los que suben los usuarios).

El directorio [[HTML#Cláusulas static|static]] es en el que guardamos estilos, imágenes propias de la página, archivos de javascript...
```Python
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = "/media/"

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'landing/static')
```
### DEFAULT_AUTO_FIELD
Este, como se puede entender por su nombre, define el campo por defecto que tendrán los modelos.
```Python
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```