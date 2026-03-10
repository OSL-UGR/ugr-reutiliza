- Este documento es un documento de ayuda para cualquier modificación real que se tenga que hacer dentro de el código o cualquier archivo de la aplicación. 

- Durante toda esta documentación si tenemos que realizar alguna modificación en el despiegue, se asume que estaremos conectados por ssh al servidor actual en el que está lanzado (un ordenador aquí abajo de una mesa en las oficinas jajajaja). Para acceder a este siempre que el servicio ssh esté activo en tu maquina, ejecuta el siguiente comando:

``` bash
ssh oslugr@ceprudwdat06.ugr.es
```

## Como acceder a la aplicación:

Actualmente la aplicación está accesible y desplegada dentro de la siguiente url:
- https://ceprudwdat06.ugr.es

Para acceder a ella como administradores, hay generado en la base de datos un usuario **super_admin** con las credenciales de la Oficina Software libre, es decir, su correo y contraseña respectivos. Actualmente (a no ser que se haya modificado) esos datos son los mismos que se encuentran en el fichero oculto que NUNCA debe subirse al github **credentials.txt**. 

El super_admin es el único rol de usuario que puede acceder al panel de administración. Dentro de la aplicación encontramos los siguientes roles:

1. **active_user:** Este tipo de usuario es el usuario activo o usuario normal. Es el rol que se le asigna por defecto a cualquier usuario que re registre en la aplicación o que se añada desde la pantalla de gestión de usuarios. Tiene acceso a todas las funcionalidades principales de la aplicación a **excepción** de las relacionadas con la gestión (panel de admin de Django o listado de usuarios de la aplicación)
2. **staff_user**: Este tipo de usuarios en un usuario con funcionalidades de gestión. Tiene el poder de añadir nuevos usuarios, eliminar usuarios existentes (a excepción de los super_ admin) y consultar los datos básicos de cualquier usuario registrado en la aplicación. La **única manera** de delegar a un usuario activo el rol de staff, es que un administrados se lo asigne a través de la página de Admin de Django.
3. **super_admin:** Este usuario puede hacer de todo basicamente, lo más esencial acceder a el panel de administrador de Djando para cualquier gestión directa con la base de datos.

## Archivos que nunca se deben subir a GITHUB

La aplicación depende de varios archivos que contienen contraseñas reales y satos sensibles, sin estos la web colapsaría. Nunca deben publicarse, hay que extremar la preocupación en cuanto a estos:

- **credentials.txt:** contiene el correo electrónico y contraseña de la cuenta de correo que envía los correos electrónicos automáticamente a todos los usuarios de la aplicación. Actualmente esta cuenta es la principal de la Oficina: osl@ugr.es
- **secret_key.txt:** contiene la llave criptográfica de Django para proteger todas als contraseñas de los usuarios y de las sesiones.
- **dnis.txt:** contiene en texto plano todo el listado de dnis de los usuarios que tienen acceso a registrarse en la aplicación. Estos dnis ya están cargados en la base de datos, así que aunque se borrase el archivo no habría ningún problema. Sin embargo es interesante mantenerlos por si en un futuro tuviésemos que cargarlos otra vez por culpa de algún error o reseteo de la base de datos.
## Modificaciones en caliente:

El servidor está desplegado con Apache, el cual carga el codigo Python en la RAM. Si editamos algun archivo .py los cambios NO SE APLICAN AUTOMÁTICAMENTE en la web.

Trás cualquier cambio es muy importante tocar el archivo WGSI para avisar a Apache de que hay código nuevo. Así que para recargar la página deberemos ejecutar lo siguiente:

```bash
touch /opt/ugr-reutiliza/muebles/muebles/wsgi.py
```

## Cambios en cliente (css, Javascript)

Si modificamos parte del cliente, asa exactamente lo mismo Apache no lo verá hasta que sea el propio Djando el que los recompile. Despues de guardar cambios en el css o en JavaScript, deberemos ejecutar la siguiente secuencia de comandos: 

```bash
cd /opt/ugr-reutiliza/muebles
source ../env/bin/activate
python manage.py collectstatic

```


## Cambios en la base de datos

Si añadimos alguna tabla nueva o bien modificamos el archivo models.py de Django es muy importante actualizar las migraciones de la base de datos.

``` bash

cd /opt/ugr-reutiliza/muebles
source ../env/bin/activate
python manage.py makemigrations
python manage.py migrate

```

En complementación con esto, para cargar los dnis del documento dnis.txt comentado anteriormente, ya está implementado un script dentro de los archivos de la aplicación que lee este archivo y lo carga directamente en la base de datos. Para ello tendremos que ejecutar:

``` bash
python manage.py cargar_dnis
```

Que no se nos olvide actualizar las migraciones de vuelta como hemos echo anteriormente.

## Cuidado con el editor nano!!

Aunque el código está sincronizado con github y podamos cargarlo con git pull, para cambios más específicos es recomendable utilizar un editor de texto nano por eficacia. 

Durante unas de estas modificaciones, por culpa de este editor estube debuggeando el código casi una hora ya que no encontraba el error. Por lo visto, si estamos dentro de un archivo python y tabulamos, aunque dentro del editor nosotros no lo veamos, en el archivo de texto se **pone una referencia del estilo "\t"indicando la tabulación**. Lo que nos lanzará un error 500 por culpa de la sintaxis. Todo esto sabiendo ya lo pesado que se pone python con las tabulaciones ajajjaj.

Por esta razón siempre que queramos tabular en un fichero .py **es recomendable tabular usando 4 espacios**, por esa razón RECUEDA SIEMPRE:

- 1 tabulación = 4 espacios.
- 2 tabulaciones = 8 espacios.
- 3 tabulaciones = 12 espacios...

## Que hacer si la web explota (error 500)

Si al realizar algún cambio la web nos devuelve un mensaje con un mensaje de **error con id 500** significa que la hemos liado en nuestro código y tenemos algún error. Por lo que para acceder a los arhivos logs de error que nos lanzala web, podemos ejecutar el siguiente comando para ver la información que nos muestra el servidor:

``` bash
sudo tail -n 50 /var/log/apache2/error.log
```

