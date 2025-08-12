import os
import streamlit as st
from utils import borra_ficheros

SUBTITLE  = "Desde ésta página pueden descargarse los distintos paquetes de datos que se hayan generado previamente. Cada uno de ellos contiene una colección de ficheros agrupados en un _.zip_"
DISCLAMER = "_Por confidencialidad de datos tanto los ficheros generados como la base de datos se eliminan una vez termina la sesión en curso._"

def limpiar_estado(args):  # args es el diccionario que pasa streamlit-authenticator
    """Limpia el estado de la sesión y borra ficheros.
    Útil al cerrar sesión."""
    st.session_state.clear()
    borra_ficheros("db")  # Limpia la base de datos al iniciar sesión
    borra_ficheros("files")
    #print(args)  Quitar para producción
    st.rerun()

def mostrar_descargas_zip(directorio="files", user="Donusted"):
    """Muestra todos los archivos .zip disponibles para descargar desde
    el directorio especificado. Eliges uno desde un 'select' y luego saca
    un botón que permite descargarlo"""

    # Listar todos los archivos .zip en el directorio
    zips = [f for f in os.listdir(directorio) if f.endswith(".zip")]
    if not zips:
        st.warning("No hay archivos ZIP disponibles para descargar.")
        return

    zip_seleccionado = st.selectbox(f"{user}, selecciona un archivo ZIP para descargar:", zips)
    zip_path = os.path.join(directorio, zip_seleccionado)

    with open(zip_path, "rb") as fp:
        st.download_button(
            label=f"Descargar {zip_seleccionado}",
            data=fp,
            file_name=zip_seleccionado,
            mime="application/zip"
        )


# ---------------------------------------------------------
# Setea pestaña de la página
# ---------------------------------------------------------
st.set_page_config(
    page_title="Descargar ficheros",
    page_icon="📥"
)

# ---------------------------------------------------------
# Verificar autenticación antes de mostrar nada
# ---------------------------------------------------------
if "authentication_status" not in st.session_state or st.session_state["authentication_status"] != True:
    st.warning("🔒 Por favor, inicia sesión desde la página **Inicio** del menú lateral.")
    st.stop()
# ---------------------------------------------------------

# ---------------------------------------------------------
# Titulo y subtitulo
# ---------------------------------------------------------
# Creamos un placeholder vacío
st.title("Descargar los ficheros de datos")
st.subheader(SUBTITLE)
msg_files_generated = st.empty()
st.divider()
# ---------------------------------------------------------


# Mensaje atendiendoa sí existen ficjeros o no. -----------
if (st.session_state.get("files_generated") is None):
    msg_files_generated.warning("Todavía no hay ficheros para descargar")
else:
    msg_files_generated = st.empty()
# ---------------------------------------------------------


# Menú lateral --------------------------------------------
with st.sidebar:
    st.success(st.session_state.get('email'))
    if st.button("Cerrar sesión"):
        limpiar_estado("Purga desde Descargar Ficheros")
# ------------------------------------------------

# Chicha --------------------------------------------------
if (st.session_state.get("files_generated") is not None):
    mostrar_descargas_zip("files", st.session_state.get("name", "Donusted"))  # Nombre de usuario por defecto


# Footer -----------------
st.divider()
st.caption(DISCLAMER)
