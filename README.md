# Generador de ficheros de datos (Streamlit)

[![Made with Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.47.1-FF4B4B?logo=streamlit&logoColor=white)
![Authenticator](https://img.shields.io/badge/streamlit--authenticator-0.4.2-blue)
![PyYAML](https://img.shields.io/badge/PyYAML-6.0.2-yellow)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey?logo=sqlite&logoColor=white)
![OS](https://img.shields.io/badge/OS-Windows%2010%2F11-0078D6?logo=windows)
![GPT-5](https://img.shields.io/badge/GPT--5-262626?logo=openai&logoColor=white)

Aplicación web (Streamlit) para generar, comprimir y descargar ficheros de datos de prueba a partir de una base de datos SQLite. Incluye autenticación con `streamlit-authenticator` y limpieza automática de datos al finalizar la sesión.

## Qué puedes hacer con esta app
- Acceder con usuario/contraseña y mantener una sesión segura.
- Subir un fichero SQLite (.sqlite / .db) como fuente de datos.
- Generar ficheros de datos (.txt) y empaquetarlos en .zip automáticamente.
- Descargar los paquetes .zip generados desde la propia app.
- Revisar el log del proceso de generación.

## Tecnologías
- Streamlit (UI, estado de sesión, widgets y layout)
- streamlit-authenticator (login/cookies)
- SQLite (fuente de datos)
- PyYAML (configuración)

## Requisitos
- Python 3.12.11
- Windows 10/11

## Puesta en marcha
1) (Opcional) Crear y activar un entorno virtual

```pwsh
python -m venv .venv
. .venv/Scripts/Activate.ps1
```

2) Instalar dependencias

```pwsh
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

3) Configurar credenciales y secretos
- Usuarios y cookies: `.streamlit/auth.yaml` (incluido en el proyecto).
- Secretos para generación (usados en `pages/3_🤹‍♂️_Generar_ficheros.py`): crea `.streamlit/secrets.toml` con:

```toml
[portal_credentials]
clavePortal   = "*******"
claveGestiona = "*******"
```

4) Ejecutar la app

```pwsh
streamlit run "1_🏠_Inicio.py"
```

> Si el puerto 8501 está ocupado, añade `--server.port 8502`.

## Manual de usuario
### 1. Inicio (Login)
- Entra en “Inicio” y autentícate con un usuario de `.streamlit/auth.yaml`.
- Tras iniciar sesión, la app prepara el entorno (limpieza de restos previos).

### 2. Subir Base de Datos
- En “Subir Base de Datos” selecciona tu fichero `.sqlite` o `.db`.
- El archivo se guarda en `db/` y su ruta queda disponible para las demás páginas.

### 3. Generar ficheros
- En “Generar ficheros” pulsa “Generar ficheros”.
- Se ejecuta el proceso que crea `.txt` y los comprime en un `.zip` en `files/`.
- Se muestra la salida (log) del proceso. Si todo está bien, verás un aviso con el `.zip` disponible.

### 4. Descargar ficheros
- En “Descargar ficheros” selecciona el `.zip` deseado y pulsa el botón de descarga.

### 5. Cerrar sesión y limpieza
- Desde la barra lateral pulsa “Cerrar sesión”.
- La app borra `db/` y `files/` para preservar la confidencialidad de los datos.

## Sobre Streamlit y posibilidades
- Libre y open source (Sin licencias de pago. Puede usarse comercialmente)
- Widgets interactivos (subida de archivos, botones, selectores, desplegables, checks, etc.).
- Ideal para Data Science (Se integra con Pandas, Matplotlib, Plotly, Seaborn, Altair, Scikit-learn, etc.)
- Estado de sesión (`st.session_state`) para mantener contexto entre páginas.
- Secrets management nativo con máxima fiabilidad en `.streamlit/secrets.toml`, y admite muchos más.
- Despliegue sencillo local o en la nube (Streamlit Cloud u otros PaaS).
- Extensible con multitud de componentes de terceros (p. ej., `extra-streamlit-components`, utilizado por `streamlit-authenticator`).

## Estructura principal
- `1_🏠_Inicio.py`: entrada y login.
- `pages/2_📤_Subir_Base_de_Datos.py`: carga de BD.
- `pages/3_🤹‍♂️_Generar_ficheros.py`: generación y empaquetado.
- `pages/4_📥_Descargar_ficheros.py`: descarga de zips.
- `utils.py`: utilidades de borrado, zip y nombres.
- `logs/files_creation.log`: log del proceso de generación.

## Autores
Antonio y su nuevo amigo (![GPT-5](https://img.shields.io/badge/GPT--5-262626?logo=openai&logoColor=white))
<!-- Foto del autor principal -->
<p>
	<img src=".streamlit/anvatar_QA.jpg" alt="Antonio" width="120" style="border-radius: 8px;" />
</p>

## Equipo QA
- José Luis Pérez
- Fernando
- Carmen Prats
- Antonio
- Carmen Arroyo
- Alberto Barragán


## Changelog
Consulta el historial de cambios en [CHANGELOG.md](./CHANGELOG.md).

## FAQ / Problemas comunes
- “Faltan dependencias”: ejecuta `pip install -r requirements.txt` en el entorno activo.
- “No abre el fichero principal”: usa comillas por los emojis: `streamlit run "1_🏠_Inicio.py"`.
- “Puerto en uso”: añade `--server.port 8502` al comando de ejecución.
