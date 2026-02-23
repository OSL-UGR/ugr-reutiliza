from django.core.management.base import BaseCommand
from django.conf import settings
from landing.models import DniAutorizado
import os

# TODO:Para ejecuttarla hay que hacer lo siguiente:'python manage.py cargar_dnis'
#  Esto hay que explicarlo dentro de la documentación

class Command(BaseCommand):

    # Descripción de ayuda que sale si ejecutamos 'python manage.py help'
    help = 'Carga automáticamente los DNIs, permitidos desde el archivo de dnis.txt'

    # FFunción que se ejecuta al lanzar el comando 'python manage.py cargar_dnis'
    def handle(self, *args, **options):
        
        # Obtenemos la ruta del archivo
        ruta = os.path.join(settings.BASE_DIR, 'dnis.txt')

        # Devolvemos si detectamos que no ha encontrado el archivo
        if not os.path.exists(ruta):
            self.stdout.write('ERROR: No ha encontrado la ruta del archivo dnis.txt')
            return 
        
        # Abrimos la ruta del archivo en modo lectura (r)
        with open(ruta, 'r', encoding='utf-8') as archivo: # with cerrará el archivo automáticamente tras la lectura

            # readlines(): lee el archivo línea por línea
            # strip() borra todos los espacios y saltos de línea que tenga el txt, quedándonos solo con el texto
            dnis = [linea.strip() for linea in archivo.readlines() if linea.strip()]
        
        creados = 0

        for dni in dnis:

            # get_or_create(): busca en la base de datos ee DNI, si no existe lo inserta (created=True), si ya existiese no hace nada (created=False)
            obj, created = DniAutorizado.objects.get_or_create(dni=dni)

            if created:
                creados += 1
        
        self.stdout.write(f'Perfecto, se han leído {len(dnis)} nuevos y se han insertado {creados} nuevos en la base de datos')