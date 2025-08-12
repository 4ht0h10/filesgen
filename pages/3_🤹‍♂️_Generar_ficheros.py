import streamlit as st
import sqlite3
import subprocess
import sys
from utils import borra_ficheros, agrupar_y_borrar_txt, genera_nombre_zip

SUBTITLE = "Desde ésta página se generan los ficheros. Se descargan desde la sección **Descargar Ficheros**. Puede obtenerse tantos conjuntos de datos nuevos como se desee simplemente volviendo a pulsar el botón _'Generar ficheros'_ aquí disponible."
DISCLAMER = "_Por confidencialidad de datos tanto los ficheros generados como la base de datos se eliminan una vez termina la sesión en curso._"


def limpiar_estado(args):  # args es el diccionario que pasa streamlit-authenticator
    """Limpia el estado de la sesión y borra ficheros.
    Útil al cerrar sesión."""
    st.session_state.clear()
    borra_ficheros("db")  # Limpia la base de datos al iniciar sesión
    borra_ficheros("files")
    #print(args)  Quitar para producción
    st.rerun()

def prueba_sqlite():
    """Prueba la conexión a SQLite."""
    try:
        conn = sqlite3.connect("db/test.db")
        cursor = conn.cursor()
        cursor.execute("SELECT sqlite_version();")
        version = cursor.fetchone()
        conn.close()
        return f"SQLite version: {version[0]}"
    except sqlite3.Error as e:
        return f"Error al conectar a SQLite: {e}"

# ---------------------------------------------------------
# Setea pestaña de la página
# ---------------------------------------------------------
st.set_page_config(
    page_title="Genera ficheros",
    page_icon="🤹‍♂️"
)

# ---------------------------------------------------------
# Verificar autenticación antes de mostrar nada
# ---------------------------------------------------------
if "authentication_status" not in st.session_state or st.session_state["authentication_status"] != True:
    st.warning("🔒 Por favor, inicia sesión desde la página **Inicio** del menú lateral.")
    st.stop()
# ---------------------------------------------------------

# Inicializa contador para distinguir los diferentes ficheros .zip
if "zip_counter" not in st.session_state:
    st.session_state.zip_counter = 1
# ---------------------------------------------------------

# ---------------------------------------------------------
# Titulo y menú lateral
# ---------------------------------------------------------
st.title("Genera los ficheros de datos")
st.subheader(SUBTITLE)
st.divider()
# Menú lateral -----------------------------------
with st.sidebar:
    st.success(st.session_state.get('email'))
    if st.button("Cerrar sesión"):
        limpiar_estado("Purga en Generar ficheros")
# ------------------------------------------------

# ---------------------------------------------------------
# Mensaje en función de si ya se habían generado ficheros o no
# ---------------------------------------------------------
# Creamos un placeholder vacío
msg_files_generated = st.empty()

files_generated = st.session_state.get("files_generated")
if files_generated is not None:
    msg_files_generated.info("Ya tienes ficheros generados. Puedes descargártelos o generar nuevos 🎰")
    hay_ficheros = True
else:
    hay_ficheros = False
    msg_files_generated.warning("⚠️ Aún no se han generado ficheros de datos.")

# Determino los parámetros que necesito para la generación de ficheros
db_path = st.session_state.get("db_path")
clavePortal = st.secrets['portal_credentials']['clavePortal']
claveGestiona = st.secrets['portal_credentials']['claveGestiona']
# ---------------------------------------------------------

if db_path is not None:
# ---------------------------------------------------------
# Ya se ha subido una base de datos
# ---------------------------------------------------------

    # ---------------------------------------------------------
    # Mensajes en función de si ya había ficheros creados
    # ---------------------------------------------------------
    # Creamos un placeholder vacío
    msg_gen_button = st.empty()
    st.write(f"Base de datos en uso: {st.session_state['current_db']}")
    if hay_ficheros:
        msg_gen_button.write(" Puedes volver a generar otros ficheros de datos de prueba si quieres.")
    else:
        pass
        #msg_gen_button.write(" Puedes generar los ficheros de datos de prueba pulsando el botón de abajo.")

    if st.button("Generar ficheros"):

        try:
            result = subprocess.run([sys.executable, "fertanilo_downloader.py", db_path, clavePortal, claveGestiona], capture_output=True, text=True, check=True)

            # Mostramos el LOG del proceso de generación de ficheros ----------
            st.write("Salida del proceso de generación de ficheros:")
            if result.stdout:
                st.code(result.stdout)
            if result.stderr:
                st.code(f"RESULTADO DEL PROCESO:\n{result.stderr}")

            # Comprimir en un .ZIP y borrar los .txt -------------------------------------
            zip_name = genera_nombre_zip(name='portal_file_', num=st.session_state.zip_counter)
            zip_path = agrupar_y_borrar_txt("files", zip_name)
            if zip_path:
                st.session_state.zip_counter += 1
                st.success(f"Archivo comprimido disponible para descarga: `{zip_name}`.")
            else:
                st.warning("No se encontraron archivos .txt para comprimir.")

            msg_files_generated.info("Ya tienes ficheros generados. Puedes descargártelos o generar nuevos 🎰")
            msg_gen_button.write("Puedes volver a generar otros ficheros de datos de prueba si quieres.")
            st.balloons()
            if "files_generated" not in st.session_state:
                st.session_state.files_generated = True

        except Exception as e:
            #print("Clicked on 'Generar ficheros'") Quitar para producción
            st.error(f"Error al generar los ficheros: {e}")
            st.stop()

else: # db_path no estaba en la sesión
    # ---------------------------------------------------------
    # Todavía no hay subida ninguna BD
    # ---------------------------------------------------------
    st.warning("Primero debes subir una base de datos en la sección **Subir Base de Datos**")

# Footer -----------------
st.divider()
st.caption(DISCLAMER)
