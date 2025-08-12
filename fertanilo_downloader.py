import logging
import logging.config
import sqlite3
import os
import sys
import yaml
from utils import FileGenerator as fg

##########################################################
#                                                        #
#      Script que crea los ficheros de datos de          #
#      prueba a partir la información almacenada en      #
#      la base de datos.                                 #
#                                                        #
##########################################################

# Establecer las rutas y ficheros de configuración
#   Parece un poco liada pero es para que sea agnóstico al
#   sistema de ficheros.
#
ruta_params_config = os.path.join('.streamlit', 'auth.yaml')
ruta_fichero_log   = os.path.join('logs', 'files_creation.log')

# Carga parámetros del fichero de configuración
# usando la librería Yaml.
#
with open(ruta_params_config, 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

# Configuración de los ficheros de log
#
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s-%(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(ruta_fichero_log, encoding='utf-8'),  # Saca a fichero
        logging.StreamHandler()                 # Saca a terminal TODO: Quitar con ejecución desasistida
    ]
)
logger = logging.getLogger(__file__)

# Establecer valor de la BBDD SQLite a consultar que
# se ha pasado como primer parámetro del script
# y también las pass secretas del Portal del Empleado y
# de GESTIONA que se han pasado como segundo y tercer
# argumentos respectivamente
#
if len(sys.argv) > 3:
    BBDD = sys.argv[1]
    passPortal = sys.argv[2]
    passGestiona = sys.argv[3]
else:
    logger.error(" ** [ERROR] No se ha recibido el nombre de la BBDD SQLite a consultar o los pass de acceso al Portal del Empleado y GESTIONA")
    sys.exit(1)

# Query de consulta que se traerá todos los metadatos
# para casos de uso definidos como activos.
#
SELECT = '''
         SELECT * FROM FILE_METADATA fm 
         WHERE fm.fm_activo = 1;
         '''

def get_file_metadata_from_db():
    ''' Obtiene todas las queries y demás datos necesarios
        en la creación de los distintos ficheros, y que está
        todo almacenado en la BBDD.
    '''

    try:
        #######################################################
        #      Conecta a la Base de datos                     #
        #######################################################

        sqliteConnection = sqlite3.connect(BBDD)
        cursor = sqliteConnection.cursor()
        logger.debug("Conectado con la base de datos %s", BBDD)

    except sqlite3.Error as error:
        logger.error(" ** ERROR conectando a %s: %s", BBDD, error)
        raise

    try:
        #######################################################
        #  Ejecutar la consulta para obtener toda la info     #
        #  necesaria para crear ficheros.                     #
        #######################################################
        cursor.execute(SELECT)

        # Obtener los resultados
        data = cursor.fetchall()

    except sqlite3.OperationalError as error:
        logger.error("** ERROR ejecutando el script BBDD %s: %s", BBDD, error)
        raise

    except sqlite3.IntegrityError as error:
        logger.error("** ERROR de integridad referencial al ejecutar %s: %s", BBDD, error)
        raise

    except sqlite3.Error as error:
        logger.error( "** ERROR trabajando con la BBDD SQLite; %s", error)
        raise

    except Exception as error:
        logger.error( '** ERROR en el fetch de la tabla FILE_METADATA: %s', error)
        raise

    else:
        logger.debug("Script de creación de la BBDD terminado con éxito")

    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            logger.debug("Cerrada la conexión SQLite")


    logger.info( "Obtenidos de la BBDD todos los datos necesarios" )
    return data

def _procesa_tupla(item):
    '''Método privado que procesa cada tupla usando la clase
       'FileGenerator' para crear un fichero de datos a partir
       de ella.
    '''

    fichero = fg(item[1], item[2], item[3], item[4], item[5], item[6], item[7], BBDD, passPortal=passPortal, passGestiona=passGestiona )
    result = fichero.execute_query(item[6])
    if (result != 'NO HAY DATOS'):
        linea = fichero.compose_data_line(result)
        fichero.write_file(linea)
        logger.info("Creado el fichero '%s'", item[1])
    else:
        logger.warning("** No se ha encontrado datos para '%s' - Fichero no creado", item[1])

def write_them_all(file_data_list):
    '''Procedimiento que partiendo de todoslos metadatos contenidos en una 
       lista de tuplas procede a componer y escribir uno a uno cada fichero
       de datos.
    '''

    for tupla in file_data_list:
        _procesa_tupla(tupla)

if __name__ == '__main__':

    metadatos = get_file_metadata_from_db()
    if metadatos:
        write_them_all(metadatos)
    else:
        logger.warning('** No ha encontrado nada en la tabla FILE_METADATA!')
