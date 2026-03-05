from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from .backends import SettingsBackend
from .models import Mueble, Foto, Usuario, Reserva, DniAutorizado, categorias as cat
from threading import Thread
import smtplib
from email.mime.text import MIMEText
from django.utils import timezone
from datetime import timedelta


URL = ''
backend = SettingsBackend()

port = 587
smtp_server = "smtp.ugr.es"

file = open(str(settings.BASE_DIR) + "/credentials.txt", "r")

# Estos 3 parámetros son los que hemos rellenado dentro de credentials.txt
email = file.readline().strip('\n')
password = file.readline().strip('\n')
inventoryEmail = file.readline().strip('\n')

# /*************************************************************************************************/
# /********************* COMIENZO DE FUNCIONES DERIVADAS AL CORREO ELECTRÓNICO *********************/
# /*************************************************************************************************/


# Correo para el ofertante al realizar una reserva sobre uno de sus artículos
def mensajeReservaOfertante(nombre, cantidad, demandante, correo_demandante, receptor, restantes):
    text = f"""\
¡Hola!

¡Buenas noticias! Alguien está interesado en un mueble que has ofertado en UGR Recicla.

DETALLES DE LA RESERVA:
- Mueble: {nombre}
- Unidades solicitadas: {cantidad}
- Tu stock restante: {restantes}

DATOS DEL CONTACTO:
El usuario {demandante} ha realizado esta solicitud. 
Por favor, PONTE EN CONTACTO DIRECTAMENTE CON ÉL a través de su correo electrónico ({correo_demandante}) para acordar la fecha, hora y lugar de recogida.

IMPORTANTE: Cuando entregues el material, no olvides entrar a tu perfil de UGR Recicla y marcar la reserva como 'Recogida'. Tienes 7 días naturales antes de que el sistema la marque como retrasada.

Un saludo,
El equipo de UGR Recicla.
    """
    message = MIMEText(text, "plain")
    message["Subject"] = f"[UGR Recicla] ¡Nueva reserva de tu anuncio: {nombre}!"
    message["From"] = email
    message["To"] = receptor
    return message

# Correo para el demandante al realizar una reserva sobre un artículo
def mensajeReservaDemandante(nombre, cantidad, ofertante, correo_ofertante, receptor):
    text = f"""\
¡Hola!

Has reservado con éxito un artículo en UGR Recicla.

DETALLES DE TU RESERVA:
- Mueble: {nombre}
- Unidades reservadas: {cantidad}

¿QUÉ DEBES HACER AHORA?
Por favor, contacta directamente con {ofertante} a través de su correo electrónico ({correo_ofertante}) para organizar la recogida del material.

IMPORTANTE: Dispones de un plazo máximo de 7 días naturales desde hoy para efectuar la recogida. Pasado ese tiempo, el ofertante tendrá derecho a cancelar tu reserva y volver a publicar el artículo.

Un saludo,
El equipo de UGR Recicla.
    """
    message = MIMEText(text, "plain")
    message["Subject"] = f"[UGR Recicla] Confirmación de tu reserva: {nombre}"
    message["From"] = email
    message["To"] = receptor
    return message


# Correo tras la cancelación de una reserva por parte de un ofertante
def mensajeLiberacion(nombre, cantidad, demandante, correo, receptor, restantes):
    text = f"""\
Hola,

Te informamos de que el usuario {demandante} ha CANCELADO su reserva de tu anuncio en UGR Recicla.

DETALLES DE LA CANCELACIÓN:
- Mueble: {nombre}
- Unidades liberadas: {cantidad}
- Tu stock actual disponible: {restantes} unidades

El anuncio vuelve a estar disponible para otros usuarios en el catálogo.

Un saludo,
El equipo de UGR Recicla.
    """
    message = MIMEText(text, "plain")
    message["Subject"] = f"[UGR Recicla] Reserva cancelada - {nombre}"
    message["From"] = email
    message["To"] = receptor
    return message

# Correo trás el retraso (7 días) al ofertante de anuncio
def mensajeRetrasoOfertante(nombre, cantidad, demandante, correo_demandante, receptor):
    text = f"""\
Hola,

Te informamos de que una reserva de tu anuncio "{nombre}" ha superado el plazo máximo de recogida de 7 días y ha sido marcada automáticamente como RETRASADA.

DATOS DE LA RESERVA:
- Unidades: {cantidad}
- Solicitante: {demandante} ({correo_demandante})

¿QUÉ PUEDES HACER AHORA?
Accede a tu perfil de UGR Recicla. Tienes dos opciones:
1. Si ya se lo entregaste y olvidaste registrarlo en la app, por favor, márcalo como 'Recogido' para cerrar el proceso.
2. Si el solicitante no ha aparecido, puedes cancelar la reserva pulsando en 'Volver a publicar' para que el artículo regrese al catálogo.

Aun así, si sigues interesado en la entrega, siempre puedes escribirle directamente a su correo.

Un saludo,
El equipo de UGR Recicla.
    """
    message = MIMEText(text, "plain")
    message["Subject"] = f"[UGR Recicla] AVISO: Reserva retrasada - {nombre}"
    message["From"] = email
    message["To"] = receptor
    return message

# Correo trás el retraso (7 días) al demandante del anuncio.
def mensajeRetrasoDemandante(nombre, cantidad, ofertante, correo_ofertante, receptor):
    text = f"""\
Hola,

Nos ponemos en contacto contigo para avisarte de que ha expirado el plazo de 7 días para recoger tu reserva en UGR Recicla.

DATOS DE LA RESERVA:
- Mueble: {nombre} ({cantidad} unidades)
- Ofertante: {ofertante} ({correo_ofertante})

¿QUÉ HA PASADO?
La reserva ha sido marcada como RETRASADA. El dueño del artículo ahora tiene la opción de cancelar tu solicitud y volver a publicarlo.

- Si sigues interesado en el material, por favor, contacta urgentemente con {ofertante} en su correo electrónico.
- Si ya has recogido el material pero sigue saliendo en curso, avisa al ofertante para que lo marque como 'Recogido' en su perfil de la aplicación.

Un saludo,
El equipo de UGR Recicla.
    """
    message = MIMEText(text, "plain")
    message["Subject"] = f"[UGR Recicla] URGENTE: Plazo de recogida expirado - {nombre}"
    message["From"] = email
    message["To"] = receptor
    return message

# Envía un email, los mensajes base son las funciones anteriores a esta.
def sendMail(email, password, message, receptor):
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        server.starttls()
        server.login(email, password)
        server.sendmail(email, receptor, message.as_string())
        server.close()


# /********************************************************************************************/
# /********************* FIN DE FUNCIONES DERIVADAS AL CORREO ELECTRÓNICO *********************/
# /********************************************************************************************/


# Busca todas las reservas en estado 'Reservado' que tengan más de 7 días, y las pasa automáticamente a estado 'Retrasado'
def actualizar_reservas_retrasadas():

    # Calculamos el límite de tiempo de 7 días con respecto al día actual (la fecha inicial límite)
    # Ej: (5 de marzo de 2026 a las 10:00:00) - 7 días = (26 de febrero de 2026 a las 10:00:00)
    limite = timezone.now() - timedelta(days=1)

    # Vemos que reservas se hicieron antes de esa fecha límite 
    reservas_retrasadas = Reserva.objects.filter(estado='Reservado', fecha_reserva__lt=limite)

    if reservas_retrasadas.exists():
        # Recorremos todas las reservas

        for reserva in reservas_retrasadas:

            ofertante = reserva.mueble.ofertante
            nombre_ofer = f"{ofertante.nombre} {ofertante.apellidos}"

            demandante = reserva.demandante
            nombre_deman = f"{demandante.nombre} {demandante.apellidos}"

            # Envíamos los correos con toda la información
            msg_ofer = mensajeRetrasoOfertante(reserva.mueble.nombre, reserva.cantidad, nombre_deman, demandante.email,ofertante.email)
            Thread(target=sendMail, args=(email, password, msg_ofer, ofertante.email)).start()

            msg_deman = mensajeRetrasoDemandante(reserva.mueble.nombre, reserva.cantidad, nombre_ofer, ofertante.email, demandante.email)
            Thread(target=sendMail, args=(email, password, msg_deman, correo_deman)).start()

            # Realizamos el cambio de estado
            reserva.estado =  'Retrasado'
            reserva.save()



def mueblesCat(listaCat):
    muebles = Mueble.objects.filter(categoria__in=listaCat)

    return muebles

# Solo el personal de administración (is_staff o is_superuser) pueden modificar muebles
def permisoAñadir(email):
    usuario = Usuario.objects.get(pk=email)
    return (usuario.is_staff or
            usuario.is_superuser)

# Puedes modificar un anuncio si: eres "is_superuser" o eres "is_staff" y el anuncio es tuyo.
def permisoModificar(email, mueble_id):
    mueble = Mueble.objects.get(pk=mueble_id)
    usuario = Usuario.objects.get(pk=email)
    return ((usuario.is_staff and usuario == mueble.ofertante) or
            usuario.is_superuser)

# Tablón principal.
@login_required
def index(request):

    actualizar_reservas_retrasadas() # Actualiza posibles reservas retrasadas por tiempo

    listaMuebles = Mueble.objects.order_by("-id") # El -id devuelve los muebles del ás nuevo al más antiguo.
    categorias = [] 

    # Contamos cuántos muebles hay de cada categoría
    for i in range(len(cat)):
        muebles = Mueble.objects.filter(categoria=cat[i][0])
        categorias.insert(i, {"muebles": muebles,
                              "text": cat[i][0],
                              "num": len(muebles)})

    # Comprueba si el usuario ha realizado algún check para filtrar solo los muebles de x categoría 
    seleccionadas = request.GET.getlist('checks')

    # Si ha filtrado, solo devolvemos esos muebles
    if (len(seleccionadas) != 0):
        print(seleccionadas)
        listaMuebles = mueblesCat(seleccionadas)

    # Si no ha filtrado, mostramos todos los muebles de todas las categorías
    else:
        seleccionadas = categorias

    context = {
            "listaMuebles": listaMuebles,
            "categorias": categorias,
            "selected": seleccionadas,
            "URL": URL
            }
    
    # Envíamos los muebles a muebles.html
    return render(request, "muebles/muebles.html", context)

# Página de inicio de sesión
def loginPage(request):
    context = {
            "URL": URL,
            }
    # Si ya está loqueado e intenta acceder a /login, le redirigimos la página de inicio para que no pueda 
    if request.user.is_authenticated:

        return redirect("index")    

    # Si lanzamos un POST (iniciamos la comprobación de   de sesión)
    elif (request.method == "POST"):
        email = request.POST['email']
        psw = request.POST['psw']

        # Comprobamos que el usuario ya se encuentre registrado enl la base de datos
        if not Usuario.objects.filter(email=email).exists():
            context['error'] = "No existe ninguna cuenta registrada con este correo electrónico, por favor registrese. Si piensa que es un error contacte con un administrador"
            return render(request, "muebles/login.html", context)

        user = backend.authenticate(email=email, password=psw)
        # Si la combinación de correo y contraseña es correcta, iniciamos sesión
        if user is not None:
            login(request, user)
            return redirect("index")
        
        # Si no, envíamos un error
        else:
            context['error'] = "La contraseña introducida es incorrecta. Por favor, inténtalo de nuevo."
            return render(request, "muebles/login.html", context)

    # Lanzamos un GET (se muestra el html de login base)
    else:
        return render(request, "muebles/login.html", context)

@login_required
def unbookMueble(request, mueble_id):
    mueble = Mueble.objects.get(pk=mueble_id)
    usuario = Usuario.objects.get(email=request.user)

    # Recuperamos la reserva activa del usuario
    reserva = Reserva.objects.filter(mueble=mueble, demandante=usuario).exclude(estado='Cancelada').first()
    
    if request.method == "POST" and reserva:
        demandante = reserva.demandante
        
        # El nuevo stock disponible será el actual más lo que estamos liberando
        nuevo_stock = mueble.stock_disponible + reserva.cantidad

        mensaje = mensajeLiberacion(mueble.nombre, reserva.cantidad, demandante.nombre + " " + demandante.apellidos, demandante.email, mueble.ofertante.email, nuevo_stock)
        Thread(target=sendMail, args=(email, password, mensaje, mueble.ofertante.email)).start()
        
        reserva.estado = 'Cancelada'
        reserva.save()
        
        return redirect(f"/{URL}{mueble_id}/post")
    else:
        return redirect("index")
# Función que reserva un mueble
@login_required
def bookMueble(request, mueble_id):
    mueble = Mueble.objects.get(pk=mueble_id)
    peticion = int(request.POST['cantRes'])
    restantes = mueble.stock_disponible 
    demandante = Usuario.objects.get(email=request.user)

    if request.method == "POST" and (restantes - peticion) >= 0:
        
        reserva = Reserva.objects.filter(mueble=mueble, demandante=demandante).exclude(estado='Cancelada').first()        
        if reserva:
            reserva.cantidad += peticion
        else:
            reserva = Reserva(mueble=mueble, cantidad=peticion, demandante=request.user)
            
        nombreDemandante = f"{demandante.nombre} {demandante.apellidos}"

        # Correo al ofertante
        mensaje = mensajeReservaOfertante(mueble.nombre, peticion, nombreDemandante, demandante.email, mueble.ofertante.email, restantes - peticion)
        Thread(target=sendMail, args=(email, password, mensaje, mueble.ofertante.email)).start()
        
        # Correo al demandante 
        mensaje_inv = mensajeReservaDemandante(mueble.nombre, peticion, nombreDemandante, demandante.puesto, demandante.organizacion, demandante.email, inventoryEmail)
        Thread(target=sendMail, args=(email, password, mensaje_inv, inventoryEmail)).start()
        
        reserva.save()
        return redirect(f"/{URL}{mueble_id}/post")
    else:
        return redirect("index")


@login_required
def modifyMueble(request, mueble_id):
    mueble = Mueble.objects.get(pk=mueble_id)
    fotoData = [mueble.main_image.url]
    fotos = Foto.objects.filter(mueble=mueble)
    for foto in fotos:
        fotoData.append(foto.imagen.url)

    categorias = []
    for i in range(len(cat)):
        categorias.insert(i, cat[i][0])

    context = {
            "action": 'modify',
            "categorias": categorias,
            "mueble": mueble,
            "fotos": fotoData,
            "URL": URL
            }
    if (permisoModificar(request.user, mueble_id)):
        if (request.method == "POST"):
            mueble.nombre = request.POST['nombre']
            Foto.objects.filter(mueble=mueble).delete()
            fotos = request.FILES.getlist('files')
            mueble.main_image = fotos[0]
            mueble.descripcion = request.POST['desc']
            mueble.dimensiones = request.POST['dim']
            mueble.ubiInicial = request.POST['ubiI']
            mueble.cantidad = request.POST['cant']
            mueble.categoria = request.POST['cat']
            mueble.save()

            for img in fotos[1:]:
                foto = Foto(mueble=mueble, imagen=img)
                foto.save()
            return redirect(f"/{URL}{mueble_id}/post")
        else:
            return render(request, "muebles/addMueble.html", context)
    return redirect("index")


@login_required
def addMueble(request):
    categorias = []

    for i in range(len(cat)):
        categorias.insert(i, cat[i][0])
    context = {
            'action': 'add',
            'fotos': '[]',
            'categorias': categorias,
            'URL': URL
            }
    
    # Limitamos el acceso de añadir un mueble dentro de permisoAñadir(...)
    if (permisoAñadir(request.user)):
        #Identificamos los datos obtenidos del fortmulario y los recogemos
        if (request.method == "POST"):
            print(request.FILES)
            nombre = request.POST['nombre']
            fotos = request.FILES.getlist('files')
            main_img = fotos[0] # La primera foto del listado de fotos será la portada del anuncio
            dim = request.POST['dim']
            desc = request.POST['desc']
            ubiI = request.POST['ubiI']
            cant = request.POST['cant']
            categ = request.POST['cat']
            mueble = Mueble(nombre=nombre, main_image=main_img,
                            descripcion=desc, ubiInicial=ubiI,
                            ofertante=request.user, dimensiones=dim,
                            cantidad=cant, categoria=categ)
            mueble.save()
            # Guardamos el resto de fotos tb
            for img in fotos[1:]:
                foto = Foto(mueble=mueble, imagen=img)
                foto.save()
            return redirect("index")
        else:
            # Lanzamos un GET para mostrar el formulario de añadir mueble vacío
            return render(request, "muebles/addMueble.html", context)
    return redirect("index")

@login_required
def deleteMueble(request, mueble_id):
    if (request.method == "POST"):
        if (permisoModificar(request.user, mueble_id)):
            mueble = Mueble.objects.get(pk=mueble_id)
            mueble.delete()
        else:
            return HttpResponse('Unauthorized', status=401)
    return redirect("index")

# Destruye la cookie de sesión y redirijimos a index
@login_required
def logoutPage(request):
    logout(request)
    return redirect("portada")

# Pantalla de perfil (solo puedes ver tu perfil)
@login_required
def perfil(request):

    actualizar_reservas_retrasadas() # Actualiza posibles reservas retrasadas por tiempo

    usuario = Usuario.objects.get(email=request.user)

    # Pasamos las dos listas, la de mis artículos y las de mis solicitudes
    mis_muebles = Mueble.objects.filter(ofertante=usuario).order_by('-id')
    mis_solicitudes = Reserva.objects.filter(demandante=usuario).order_by('-fecha_reserva')

    context = {
            "user": usuario,
            "mis_muebles": mis_muebles,
            "mis_solicitudes": mis_solicitudes,
            "URL": URL
            }
    return render(request, "muebles/perfil.html", context)

# Prepara todos los atributos de información sobre un mueble para mostrarlos, dado el id de un mueble
@login_required
def post(request, mueble_id):

    actualizar_reservas_retrasadas() # Actualiza posibles reservas retrasadas por tiempo


    # Obtenemos el mueble, quien es el ofertante y cuantas reservas tiene (filtrando solo las que no estan canceladas)
    mueble = Mueble.objects.get(pk=mueble_id)
    ofertante = mueble.ofertante

    usuario = Usuario.objects.get(email=request.user)

    reservas_activas = Reserva.objects.filter(mueble=mueble).exclude(estado='Cancelada')
    demandantes = [reserva.demandante for reserva in reservas_activas]

    reserva = reservas_activas.filter(demandante=usuario).first()

    # Crea la lista de imágenes definiendo la primera como la portada
    imagenes = [mueble.main_image]
    fotos = Foto.objects.filter(mueble=mueble)

    for foto in fotos:
        imagenes.append(foto.imagen)

    # Pasamos los atributos al html
    context = {
            'restantes':  mueble.stock_disponible, # Lo cojemos directamente del calculo que hace el modelo
            'mueble': mueble,
            'ofertante': ofertante,
            'reservas': reservas_activas,
            'reserva': reserva,
            'demandantes': demandantes,
            'images': imagenes,
            'user': usuario,
            "URL": URL
            }
    return render(request, "muebles/muebles.html", context)


# Función que comprueba si el usuario es un super usuario
def es_superusuario(user):
    return user.is_superuser

@login_required
@user_passes_test(es_superusuario, login_url='index') # Si no es superuser, lo manda al index
def gestion_usuarios(request):

    # Obtenemos la lista de los usuarios
    lista_usuarios = Usuario.objects.all().order_by('email')
    
    context = {
        "lista_usuarios": lista_usuarios,
        "URL": URL
    }
    
    return render(request, "muebles/gestion_usuarios.html", context)


#TODO: queda por implementar
@login_required
@user_passes_test(es_superusuario, login_url='index')
def delete_usuario(request, email):

    return redirect("gestion_usuarios")

# Función que carga la portada (pantalla principal) de la app
def portada(request):

    #Si el usuario ya guarda la sesión, lo mandamos directamente al catálogo
    if request.user.is_authenticated:

        return redirect("index")

    #Si no, le mostramos la portada

    return render(request,"muebles/portada.html", {"URL": URL}) 

# Función que maneja y redirecciona la pantalla de registro de la app
def registroPage(request):
    context = {"URL": URL}

    # Si el usuario ya guarda la sesión, lo mandamos directamente al catálogo
    if request.user.is_authenticated:

        return redirect("index")

    # Se solicita un registro en la base de datos
    if request.method == "POST":
        # Recogemos todos los datos (y limpiamos si es necesario)
        dni = request.POST.get('dni','').strip().upper()
        email = request.POST.get('email','').strip()
        psw = request.POST.get('psw','')
        nombre = request.POST.get('nombre','')
        apellidos = request.POST.get('apellidos','')
        puesto = request.POST.get('puesto','')
        telefono = request.POST.get('telefono','')
        organización = request.POST.get('organizacion','')

        # Comprobamos que el dni esté en la lista de dnis aptos
        if not DniAutorizado.objects.filter(dni=dni).exists():
            context['error'] = "Dados tu datos, no tienes acceso a la aplicación. Si piensas que es un error contacta con un administrador."
            return render(request, "muebles/registro.html", context)
        
        # Comprobamos que ese usuario con ese dni no se encuentre ya registrado
        if Usuario.objects.filter(dni=dni).exists():
            context['error'] = "El usuario con los datos dados ya se encuentra registrado. Por favor inicie sesión"
            return render(request,'muebles/registro.html',context)
        
        # Comprobamos que ese usuario no intente registrarse con un email ya registrado
        if Usuario.objects.filter(email=email).exists():
            context['error'] = "Ese correo electrónico ya está en uso, por favor ingrese otro"
            return render(request,"muebles/registro.html",context)
        
        # Si ha superado todas las comprobaciones, creamos el usuario
        try:
            new_user = Usuario(
                email = email,
                dni = dni,
                nombre = nombre,
                apellidos = apellidos,
                puesto = puesto,
                telefono = telefono,
                organización=organización
            )

            new_user.set_password(psw)    #Para que la contraseña se encripte a la hora de la inserción
            new_user.save()

            # Autologeamos en la app si se ha realizado el registro de manera correcta
            user = backend.authenticate(email=email, password=psw)
            if user is not None:
                login(request, user)
                
            return redirect("index")

        except Exception as e:
            context['error'] = f"Error al crear el usuario: {e}"
            return render(request, "muebles/registro.html", context)
    # Si es un get simplemente mostramos el formulario de registro
    else:

        return render(request, "muebles/registro.html", context)

