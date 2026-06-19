from pathlib import Path
import streamlit as st
import pandas as pd
from paths import get_data_path
# --- NUEVA IMPORTACIÓN NATIVA PARA GRÁFICOS INTERACTIVOS ---
from pygwalker.api.streamlit import StreamlitRenderer

# --- rutas base ---
BASE = Path(__file__).parent        # app/
PROJECT_ROOT = BASE.parent          # repo root
DATA_PATH = get_data_path("train.csv")

st.set_page_config(page_title="Análisis de inundaciones", layout="wide")
st.title("Análisis de inundaciones")
st.write("Esta app muestra notebooks ejecutados y el explorador interactivo de datos.")

# Cargar CSS desde style.css (app/style.css)
css_path = BASE / "style.css"
THEME_CSS = css_path.read_text(encoding="utf-8") if css_path.exists() else ""

# Override (anula fondo blanco + tipografías dentro del HTML del notebook)
OVERRIDE_CSS = """
<style>
html, body {
  background: transparent !important;
  background-color: transparent !important;
  margin: 0 !important;
  padding: 0 !important;
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, "Noto Sans", "Liberation Sans", sans-serif !important;
}
* { color: #eaeaea !important; }
a { color: #9ad3ff !important; }
div, section, article, span {
  background: transparent !important;
  background-color: transparent !important;
}
.output, .output_area, .cell_output, .jp-OutputArea,
.jp-RenderedHTMLCommon, .rendered_html, .jp-NotebookPanel,
.card, .container, .wrapper {
  background: transparent !important;
  background-color: transparent !important;
}
pre, code, .highlight {
  background: transparent !important;
  background-color: transparent !important;
  color: #eaeaea !important;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace !important;
}
table, th, td, tr {
  background: transparent !important;
  background-color: transparent !important;
  color: #eaeaea !important;
}
hr { border-color: rgba(255,255,255,0.25) !important; }
</style>
"""

def inject_overrides(html: str) -> str:
    if "</head>" in html:
        return html.replace("</head>", OVERRIDE_CSS + "\n</head>", 1)
    if "<head>" in html:
        return html.replace("<head>", "<head>\n" + OVERRIDE_CSS, 1)
    if "</body>" in html:
        return html.replace("</body>", "\n" + OVERRIDE_CSS + "\n</body>", 1)
    return html + "\n" + OVERRIDE_CSS

# carpeta donde guardas HTML
html_dir = BASE / "notebooks_html"
html_dir.mkdir(exist_ok=True)

# Lista notebooks HTML ya convertidos
files = sorted([p for p in html_dir.glob("*.html")])
choice = st.session_state.get("selected_html_choice") if hasattr(st, "session_state") else None

if files:
    names = [p.name for p in files]
    choice_name = st.selectbox(
        "Selecciona notebook HTML (convertido)",
        names,
        index=0 if choice is None or choice not in names else names.index(choice),
        key="selected_html_choice",
    )
    choice = choice_name

# Sidebar controls
st.sidebar.header("Configuración")
_ = st.sidebar.text_input("Tu nombre")
num_rows = st.sidebar.slider("Número de filas en Preview", min_value=5, max_value=100, value=20)

# --- Notebook / ejecución ---
import nbformat
from nbclient import NotebookClient
from nbconvert import HTMLExporter

def run_notebook_ipynb(ipynb_path: Path, render_html: bool = True):
    nb = nbformat.read(ipynb_path, as_version=4)

    inject_code = (
        "from pathlib import Path\n"
        f"DATA_PATH = Path({repr(str(DATA_PATH))})\n"
        "import os\n"
        "import pandas as pd\n"
        "print('--- INJECT START ---')\n"
        "print('DATA_PATH:', DATA_PATH)\n"
        "print('DATA_PATH exists=', DATA_PATH.exists())\n"
        "os.chdir(str(DATA_PATH.parent))\n"
        "print('CWD after chdir=', os.getcwd())\n"
        "df = pd.read_csv(str(DATA_PATH))\n"
        "print('df created via DATA_PATH, shape=', df.shape)\n"
    )
    nb.cells.insert(0, nbformat.v4.new_code_cell(inject_code))

    client = NotebookClient(nb, timeout=600, kernel_name="python3")
    client.execute()

    if not render_html:
        return None

    html_exporter = HTMLExporter()
    body, _ = html_exporter.from_notebook_node(nb)
    body = inject_overrides(body)
    return body

# Ejecutar notebook "fijo"
tu_notebook_path = PROJECT_ROOT / "notebooks" / "tu_notebook.ipynb"
if tu_notebook_path.exists():
    try:
        run_notebook_ipynb(tu_notebook_path, render_html=False)
    except Exception:
        pass

# --- Ejecutar y renderizar un notebook on-demand ---
st.markdown("### Ejecutar notebook on-demand (dinámico)")
nb_files = sorted((PROJECT_ROOT / "notebooks").glob("*.ipynb"))

if not nb_files:
    st.warning("No hay notebooks en la carpeta notebooks/")
else:
    nb_choice = st.selectbox("Selecciona notebook para ejecutar", [p.name for p in nb_files], key="nb_choice")
    run_now = st.button("Ejecutar notebook ahora", key="run_now")

    if run_now:
        nb_path = PROJECT_ROOT / "notebooks" / nb_choice
        with st.spinner("Ejecutando notebook..."):
            body = run_notebook_ipynb(nb_path, render_html=True)

        cache_key = nb_choice.replace(".ipynb", "") + ".html"
        out_file = html_dir / cache_key
        out_file.write_text(body, encoding="utf-8")

        st.success("Ejecución completada")
        st.components.v1.html(THEME_CSS + body, height=800, scrolling=True)

# --- Si eligió un HTML ya convertido, mostrarlo ---
if choice:
    html = (html_dir / choice).read_text(encoding="utf-8")
    html = inject_overrides(html)

    st.markdown("### Vista (HTML convertido)")
    st.components.v1.html(THEME_CSS + html, height=800, scrolling=True)


# =========================================================
# --- NUEVA ESTRATEGIA: VISUALIZACIÓN INTERACTIVA ON-DEMAND ---
# =========================================================
st.markdown("---")
st.markdown("### 📊 Exploración de Gráficos Interactivos (On-Demand)")

if DATA_PATH.exists():
    # Cargamos el DataFrame principal de inundaciones
    df_inundaciones = pd.read_csv(DATA_PATH)
    
    # Creamos y cacheamos la interfaz gráfica nativa de PyGWalker para que rinda rápido
    @st.cache_resource
    def get_pyg_renderer(_df):
        # Almacena las configuraciones de los gráficos en la carpeta cache del proyecto
        config_path = BASE / "cache" / "viz_config.json"
        return StreamlitRenderer(_df, spec=str(config_path), spec_type="json")
    
    renderer = get_pyg_renderer(df_inundaciones)
    
    # Renderizamos la interfaz interactiva oficial sin usar contenedores HTML rotos
    renderer.explorer()
else:
    st.error(f"No se pudo cargar el visualizador interactivo porque falta: {DATA_PATH}")


# --- Preview del dataset ---
st.markdown("---")
st.markdown("### Preview del dataset")
if DATA_PATH.exists():
    st.dataframe(df_preview.head(num_rows) if 'df_preview' in locals() else df_inundaciones.head(num_rows))