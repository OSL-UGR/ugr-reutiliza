# Configuración inicial

## Creación del entorno virtual

Dentro 

## Creación del proyecto de Django

[Ampliar:]
- Crear el proyecto
- Crear la app
- Configurar las vistas (urls, views...)


## Instalación de las dependencias
Para instalar las dependencias de python usaremos:
```bash
pip install django psycopg2 
```

En nuestro entorno deberemos instalar las librerías:
- python
- python-dev
- postgresql
- postgresql-dev

# Configuración de la base de datos
Para la configuración de desarrollo se ha usado un contenedor de docker
con postgres  en la última versión (a fecha de este documento es la 16.2)

## Contenedor de docker
`
docker run --name postgres -e POSTGRES_PASSWORD=password
-p 5432:5432 -d postgres
`

Este comando (`docker run ...`) sirve para crear un contenedor de docker.

### Parámetros:
- **--name** define el nombre que tendrá el contenedor.

- **-e** permite definir variables de entorno dentro del contenedor, en nuestro 
caso vamos a poner la variable POSTGRES_PASSWORD que define la contraseña de la
base de datos, a password. **Es muy importante cambiar la contraseña cuando se
quiera desplegar, ya que puede comprometer la seguridad del sistema**.

- **-p** sirve para poder mapear el puerto del contenedor hacia nuestro puerto, 
puede ser al localhost o al servidor que queramos (por defecto es el 
localhost).

- **-d** sirve para elegir la imagen que queremos utilizar, en este caso 
postgres, dado que hemos puesto postgres, por defecto se instalará la última 
imagen.

## Configuración inicial.
Para que la web pueda funcionar, es necesario crear la base de datos en 
postgres, esto lo hacemos ejecutando el comando 
`CREATE DATABASE {nombreDeLaBD};` dentro del postgres.

En docker se haría accediendo al contenedor y llamando a psql:
```bash
docker exec -it postgres bash
```
Este primer comando ejecuta bash dentro del contenedor de postgres.

**A partir de aquí es común a una instalación de postgres local**
```bash
psql -U postgres
```
Con este comando accedemos a la base de datos con el usuario postgres (el 
usuario por defecto) y una vez dentro de postgres ejecutamos el 
`CREATE DATABASE`.

## Configuración de Django

El formato de django para la configuración es el siguiente:

```Python
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

### Opciones:
- **ENGINE:** Esta configuración es la que define qué base de datos vamos a 
utilizar, por defecto django usa mysql pero en nuestro caso como ya se ha
mencionado antes, vamos a usar postgres. (En una intalación con mysql el propio
django se encarga de instalar, configurar y utilizar la base de datos, pero 
con postgres vamos a tener que definir todas las variables que hay despues de
NAME).

- **NAME:** El nombre de la base de datos, debe coincidir con el que hayamos
usado en el `CREATE DATABASE` del apartado anterior.

- **USER:** El usuario con el que vamos a acceder a postgres, dado que por 
defecto es postgres, es el que vamos a poner, pero podríamos configurarlo de
otra manera, sólo habría que cambiar este parámetro por el usuario que hayamos
configurado al crear la base de datos.

- **PASSWORD:** La contraseña de la base de datos, debe ser la misma que 
especifiquemos (En el caso de docker la misma que la variable de entorno 
POSTGRES_PASSWORD).

- **HOST:** La ip mediante a la que acceder a la base de datos, para el testing 
es localhost (127.0.0.1).

- **PORT:** El puerto mediante al que accederemos a la base de datos, el puerto
de postgres por defecto es el 5432, (En nuestro caso hemos mapeado el 5432 del 
contenedor directamente al 5432 del localhost, por lo tanto coinciden).

