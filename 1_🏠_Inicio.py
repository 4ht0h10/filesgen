import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from utils import borra_ficheros

# Constantes ----------------------------------------------
SUBTITLE = "Aplicación para generar los ficheros de datos que serán usados en los tests automáticos del _Portal del Empleado_."
EXPLANATION = """Los datos se extraen de un fichero _SQLite_ que deberá de ser proporcionado previamente por el propio usuario. Para ello se debe usar la sección **Subir base de datos** del menú lateral.

Cuando se disponga de dicha base de datos se puede lanzar el proceso de generación tantas veces como se desee desde la opción de menú **Generar ficheros**.

Y finalmente, dichos ficheros generados pueden ser obtenidos desde la sección **Descargar ficheros**."""
DISCLAMER = "_Por confidencialidad de datos tanto los ficheros generados como la base de datos se eliminan una vez termina la sesión en curso._"
# ---------------------------------------------------------

def limpiar_estado(args):  # args es el diccionario que pasa streamlit-authenticator
    """Limpia el estado de la sesión. Útil al cerrar sesión."""
    st.session_state.clear()
    borra_ficheros("db")  # Limpia la base de datos al iniciar sesión
    borra_ficheros("files")  # Limpia la base de datos al iniciar sesión
    st.rerun()

st.set_page_config(page_title="Ficheros de test", page_icon="👨‍🦯")

with open('.streamlit/auth.yaml', 'r', encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    credentials=config['credentials'],
    cookie_name=config['cookie']['name'],
    key=config['cookie']['key'],
    cookie_expiry_days=config['cookie']['expiry_days']
)

# Llama SIEMPRE a login -----------------------------------
authenticator.login(location="main",
                    fields={"Form name": "Iniciar sesión",
                            'Username':'Usuario',
                            'Password':'Clave',
                            'Login':'Acceder',
                            'clear_on_submit': True
                            })

auth_status = st.session_state.get("authentication_status")
user_name   = st.session_state.get("name")
user_mail   = st.session_state.get("email")

# Si te acabas de logar (es decir, authentication_status acaba de pasar a True),
# fuerza un rerun SOLO la primera vez
if "authentication_status" in st.session_state and auth_status:
    if not st.session_state.get("already_logged_in"):
        st.session_state["already_logged_in"] = True
        borra_ficheros("db")     # Limpia la base de datos al iniciar sesión
        borra_ficheros("files")  # Limpia la base de datos al iniciar sesión
        borra_ficheros("logs")  # Limpia la base de datos al iniciar sesión
        st.rerun()
# ---------------------------------------------------------

if auth_status is False:
    st.error("❌ Usuario o contraseña incorrectos.")
elif auth_status is None:
    st.warning("🔒 Por favor, introduce tus credenciales.")
elif auth_status:
    st.sidebar.success(user_mail)
    authenticator.logout(button_name="Cerrar sesión",
                         location="sidebar",
                         key="logout",
                         callback=limpiar_estado)

    st.title("Generador de datos de prueba")
    st.subheader(SUBTITLE)
    st.markdown(EXPLANATION)


    # Código comentado. Ver variables de sesión durante el desarrollo ---
    #st.divider()
    #with st.expander("_Detalle de la operativa_ [*click para ver*]"):
    #    st.write(st.session_state)

    # Footer ----------------------------------------------
    st.divider()
    st.caption(DISCLAMER)
