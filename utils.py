import sqlite3
import os
import logging
import logging.config
import yaml
import zipfile
from datetime import datetime

def borra_ficheros(directorio):
    """
    Borra todos los ficheros (no subdirectorios) dentro del directorio dado.
    """
    for filename in os.listdir(directorio):
        file_path = os.path.join(directorio, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error borrando {file_path}: {e}")

def agrupar_y_borrar_txt(directorio="files", nombre_zip="agrupados.zip"):
    """Agrupa todos los .txt en el directorio dado en un .zip y luego elimina los .txt."""
    zip_path = os.path.join(directorio, nombre_zip)
    txt_files = [f for f in os.listdir(directorio) if f.endswith(".txt")]

    if not txt_files:
        return None  # Nada que comprimir

    with zipfile.ZipFile(zip_path, "w") as zipf:
        for txt in txt_files:
            file_path = os.path.join(directorio, txt)
            zipf.write(file_path, arcname=txt)
            os.remove(file_path)
    return zip_path

def genera_nombre_zip(name='portal_file_', num=0):
    """
    Genera un nombre de archivo zip con el formato:
    nameDDhhmmnum.zip
    donde:
      - name: string recibido por parámetro
      - DD: día del mes (dos dígitos)
      - hh: hora (dos dígitos, 24h)
      - mm: minutos (dos dígitos)
      - num: número entero recibido por parámetro
    """
    ahora = datetime.now()
    nombre = f"{name}{ahora.day:02d}{ahora.hour:02d}{ahora.minute:02d}{num}.zip"
    return nombre

class FileGenerator():
    '''Clase magistral con métodos relacionados con la creación del fichero de datos.
       La clase crea un objeto que contiene todos los datos estáticos del fichero a
       crear salvo el resultado de la consulta a BBDD que se obtienen de forma dinámica
       con el método de la clase 'execute_query()'. 
     '''

    def __init__(self, literal, title, file_name, datos, criteria, query, obs, bbdd, passPortal=None, passGestiona=None):
        self.literal = literal             # El identificador del caso de prueba
        self.title = title                 # Título del caso de prueba
        self.file_name = file_name         # Nombre del fichero a crear
        self.datos = datos                 # Nombre del fichero a crear
        self.criteria = criteria           # Criterio de busqueda en la BD
        self.query = query                 # La select aplicada
        self.obs = obs                     # Observaciones
        self.BBDD = bbdd                   # Path de la BBDD SQLite a consultar
        self.clavePortal = passPortal      # Pass del usuario para acceso al Portal del Empleado
        self.claveGestiona = passGestiona  # Pass del usuario para acceso a Gestiona

        # Establecer las rutas y ficheros de configuración
        #   Parece un poco liada pero es para que sea agnóstico al
        #   sistema de ficheros.
        #
        paramsConfigFile = os.path.join('.streamlit', 'auth.yaml')

        # Carga parámetros del fichero de configuración
        # usando la librería Yaml.
        #
        with open(paramsConfigFile, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)

        # Establecer parámetros a usar para:
        #   - la base de datos a consultar
        #   - el pass del usuario para el 'Portal del empleado'
        #   - el pass del usuario para GESTIONA
        #
        #self.clavePortal   = config['clavePortal']
        #self.claveGestiona = config['claveGestiona'] TODO: Borra esto cuanto todo este correcto

        # Configuración del log para que use el fichero principal
        #
        self.logger = logging.getLogger("fertanilo_downloader")

    def execute_query(self, query):
        '''Ejecuta el código Select pasado por argumento y devuelve
           el resultado como una lista conteniendo una sola tupla.
        '''
        select = query
        resultado = "NO HAY DATOS"

        try:
            # Conecta a la Base de datos
            sqliteConnection = sqlite3.connect(self.BBDD)
            cursor = sqliteConnection.cursor()

            # Ejecuta la consulta para extrer los datos
            cursor.execute(select)

            # Obtiene el resultado
            datos = cursor.fetchall()

        except sqlite3.Error as error:
            self.logger.error("** ERROR sqlite3 operando con %s: %s", self.BBDD, error)
            raise

        finally:
            if sqliteConnection:
                sqliteConnection.close()
                self.logger.debug("Finalizada conexión SQLite")
            self.logger.debug("Ejecución de la consulta %s terminada", self.literal)

        # Si la consulta devuelve datos los aplicamos al return
        if datos:
            self.logger.debug("La consulta no ha sido vacía")
            resultado = datos

        return resultado

    def compose_data_line(self, tupla):
        '''A partir de dos parámetros y una tupla de datos
        compone una línea con un formato predefinido.
        Transforma con sencillez y elegancia la tupla de entrada
        en un String con el formato adecuado'''

        # Descompone la lista de tuplas en el primer elemento (nif) más el resto (cola).
        # No me pidas que te lo explique, hace una hora lo hice y ya no me acuerdo.
        #
        nif = tupla[0][0]
        cola = "|".join(tupla[0][1:]) + "|" if tupla[0][1:] else " "

        # Compone el string final:
        # 'NIF' + 'Pass1' + 'Pass2' + 'el resto' si lo hay
        #
        return  f"{nif}|{self.clavePortal}|{self.claveGestiona}|{cola}"

    def write_file(self, line):
        '''Crea un fichero de texto con un nombre y contenido
         proporcionados por parametros.'''

        # Abre un fichero en modo escritura (write mode)
        with open('files/' + self.file_name, 'w', encoding='utf-8') as fichero:
          # Escribe en el fichero la línea de datos a usar en los tests
            fichero.write(line + '\n\n')
          # A continuación escribe el resto de líneas:
            fichero.write(f"**** {self.literal}: {self.title} \n\n")
            fichero.write('**** DATOS:\n')
            fichero.write(self.datos + '\n')
            fichero.write('**** CRITERIO DE BUSQUEDA DEL USUARIO:\n')
            fichero.write(self.criteria + '\n')
            fichero.write('\n**** QUERY:\n')
            fichero.write(self.query + '\n')
            if self.obs:
                fichero.write('**** OBSERVACIONES:\n')
                fichero.write(self.obs + '\n')
