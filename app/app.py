from pathlib import Path
import streamlit as st
import pandas as pd
import nbformat
from paths import get_data_path
# Importamos pygwalker por si lo estás usando de forma nativa en la app
import pygwalker as pyg 

# --- Rutas Base ---
BASE = Path(__file__).parent        # app/
PROJECT_ROOT = BASE.parent          # repo root
DATA_PATH = get_data_path("train.csv")

# --- Configuración de la Ventana ---
st.set_page_config(page_title="Análisis de Inundaciones", layout="wide")

# =====================================================================
# 🤵 BARRA LATERAL (SIDEBAR) - ¡Aquí recuperamos el panel de la izquierda!
# =====================================================================
st.sidebar.header("🤵 Panel de Control Interactive")

# 1. Identificación del consultor
nombre_usuario = st.sidebar.text_input("Consultor a cargo:", value="Estudiante")

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Configuración de Datos")

# 2. Control interactivo de filas
num_rows = st.sidebar.slider(
    "Filas a cargar en la vista rápida:", 
    min_value=5, 
    max_value=1000, 
    value=50, 
    step=5
)

st.sidebar.markdown("---")
st.sidebar.subheader("♿ Accesibilidad")

# 3. BOTÓN/SELECTOR DE ACCESIBILIDAD
# Creamos un menú desplegable para que elijan el modo de vista
modo_vista = st.sidebar.selectbox(
    "Modo de visualización:",
    options=["Estándar", "Texto Grande 🔍", "Alto Contraste 🌗"]
)

# Aplicamos la "magia" de accesibilidad inyectando CSS según lo que elijan
if modo_vista == "Texto Grande 🔍":
    st.markdown(
        """
        <style>
        html, body, [class*="st-"] {
            font-size: 24px !important; /* Agranda la letra de toda la app */
        }
        h1 { font-size: 3.5rem !important; }
        h2 { font-size: 2.8rem !important; }
        h3 { font-size: 2.2rem !important; }
        p, span, label { font-size: 1.3rem !important; }
        </style>
        """,
        unsafe_allow_html=True
    )
elif modo_vista == "Alto Contraste 🌗":
    st.markdown(
        """
        <style>
        /* Forzamos fondo negro y textos amarillos/blancos hiper-legibles */
        .stApp {
            background-color: #000000 !important;
            color: #FFFFFF !important;
        }
        h1, h2, h3, p, span, label, strong {
            color: #FFFF00 !important; /* Texto amarillo sobre fondo negro, estándar de accesibilidad */
        }
        /* Ajuste para tarjetas y bloques de texto */
        div[data-testid="stMarkdownContainer"] p {
            color: #FFFF00 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# =====================================================================
# ENCABEZADO DE NEGOCIO (Cuerpo principal)
# =====================================================================
st.title("💼 Dashboard de Consultoría: Análisis de Inundaciones")
st.caption(f"Presentación de resultados del Grupo 1. Consultor activo: {nombre_usuario}")

# =====================================================================
# 1. EL SELECTOR DE ENTREGABLES (EDA o Modelado)
# =====================================================================
notebooks_dir = PROJECT_ROOT / "notebooks"
nb_files = sorted(list(notebooks_dir.glob("*.ipynb")))

if not nb_files:
    st.warning("⚠️ No se encontraron archivos .ipynb en la carpeta notebooks/")
else:
    # Selector único para cambiar de informe
    nb_choice = st.selectbox(
        "📊 Seleccione el informe técnico que desea presentar al cliente:",
        options=[p.name for p in nb_files],
        key="client_nb_choice"
    )
    st.success(f"📋 Mostrando en pantalla el contenido real de: **{nb_choice}**")

# =====================================================================
# 2. MOTOR DE EXTRACCIÓN DINÁMICA DE NOTEBOOKS
# =====================================================================
st.markdown("---")

def renderizar_notebook_real(notebook_path):
    """Lee el archivo .ipynb y pinta su contenido de forma ejecutada en Streamlit"""
    try:
        with open(notebook_path, "r", encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)
        
        for cell in nb.cells:
            if cell.cell_type == "markdown":
                st.markdown(cell.source)
            elif cell.cell_type == "code":
                for output in cell.outputs:
                    if output.output_type == "stream":
                        st.text(output.text)
                    elif output.output_type == "execute_result" or output.output_type == "display_data":
                        if "text/plain" in output.data:
                            texto = output.data["text/plain"]
                            if "Rows:" in texto or "Columns:" in texto or "df" in cell.source:
                                st.text(texto)
                            else:
                                st.markdown(f"`{texto}`")
                        
                        if "image/png" in output.data:
                            import base64
                            img_data = output.data["image/png"]
                            st.image(base64.b64decode(img_data))
                            
    except Exception as e:
        st.error(f"Nota: No se pudieron extraer de forma nativa algunos elementos visuales: {e}")

# Ejecutamos el renderizador basado en lo que elijan
if nb_files:
    target_nb_path = notebooks_dir / nb_choice
    renderizar_notebook_real(target_nb_path)

# =====================================================================
# 3. RESPALDO: VISTA PREVIA DEL DATASET CRUDO & PYGWALKER
# =====================================================================
st.markdown("---")
st.markdown("### 📋 Anexo: Acceso rápido a la base de datos cruda")

if DATA_PATH.exists():
    @st.cache_data
    def cargar_preview(path, filas):
        return pd.read_csv(path, nrows=filas)
    
    # Cargamos dinámicamente las filas usando el valor configurado en la barra lateral
    df_preview = cargar_preview(DATA_PATH, num_rows)
    
    # Pestañas para elegir ver la tabla normal o la interfaz interactiva de PyGWalker
    tab1, tab2 = st.tabs(["📊 Tabla de Datos", "🔍 Explorador Interactivo (PyGWalker)"])
    
    with tab1:
        st.write(f"Mostrando las primeras {num_rows} filas del dataset:")
        st.dataframe(df_preview, use_container_width=True)
        
    with tab2:
        st.write("Usa la interfaz gráfica para arrastrar columnas y crear gráficos al instante:")
        # Renderiza la interfaz de PyGWalker de manera nativa en Streamlit en base a las filas elegidas
        import streamlit.components.v1 as components
        pyg_html = pyg.walk(df_preview, output_type="html")
        components.html(pyg_html, height=800, scrolling=True)
else:
    st.error(f"No se encontró el archivo de datos en: {DATA_PATH}")

