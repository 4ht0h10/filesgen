import os
import streamlit as st
from utils import borra_ficheros

SUBTITLE  = "En esta sección se puede subir un fichero _SQLite_ que contiene la base de datos de trabajo. Este archivo constituirá la fuente de datos para generar los ficheros."
NOFILEYET = "⚠️ Pendiente de subir un fichero _SQLite_ para su posterior tratamiento."
DISCLAMER = "_Por confidencialidad de datos tanto los ficheros generados como la base de datos se eliminan una vez termina la sesión en curso._"
uploaded_file = None

def limpiar_estado(args):  # args es el diccionario que pasa streamlit-authenticator
    """Limpia el estado de la sesión y borra ficheros.
    Útil al cerrar sesión."""
    st.session_state.clear()
    borra_ficheros("db")  # Limpia la base de datos al iniciar sesión
    borra_ficheros("files")
    #print(args) Quitar para Producción
    st.rerun()

# Verificar sesión antes de mostrar nada ------------------
if "authentication_status" not in st.session_state or st.session_state["authentication_status"] != True:
    st.warning("🔒 Por favor, inicia sesión desde la página **Inicio** del menú lateral.")
    st.stop()

# Configuración de la pestaña a mostrar en el navegador ---
st.set_page_config(
    page_title="Subir BD",
    page_icon="📤"
)

# Configuración de la página inicial ----------------------
st.title("Subir el archivo")
st.subheader(SUBTITLE)
if (st.session_state.get("db_path")) is None:
    st.info(NOFILEYET)
st.divider()

# Barra lateral -------------------------------------------
with st.sidebar:
    st.success(st.session_state.get('email'))
    if st.button("Cerrar sesión"):
        limpiar_estado("Purga desde 'Subir Base de Datos'")
# ---------------------------------------------------------

uploaded_file = st.file_uploader("Elige tu base de datos SQLite en tu dispositivo", type=["sqlite", "db"])

if uploaded_file is not None:
    # Añadimos el path 'db/' al nombre del archivo para guardarlo en esa carpeta
    save_path = os.path.join("db", uploaded_file.name)

    try:
        # Guarda el archivo en el directorio 'db/'
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        #st.success(f"Archivo {uploaded_file.name} guardado correctamente")
        # Guardamos la ruta en session_state para que otras páginas lo usen
        st.session_state["db_path"]    = save_path
        st.session_state["current_db"] = uploaded_file.name
        st.badge("¡Base de datos subida correctamente!", color="green")
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
        st.stop()
else:
    if st.session_state.get("current_db"):
        st.info(f"Base de datos actualmente en uso: **{st.session_state['current_db']}**")
    else:
        st.warning("No se ha subido ningún fichero aún.")


# Footer -----------------
st.divider()
st.caption(DISCLAMER)
