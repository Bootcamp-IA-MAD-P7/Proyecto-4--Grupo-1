from datetime import datetime
from pathlib import Path
import base64
import shutil

import joblib
import nbformat
import pandas as pd
import streamlit as st

from paths import get_data_path

try:
    import pygwalker as pyg
except ModuleNotFoundError:
    pyg = None


BASE = Path(__file__).parent
PROJECT_ROOT = BASE.parent
DATA_PATH = get_data_path("train.csv")

MODEL_FILENAME = "flood_baseline_model.joblib"
MODEL_PATH = PROJECT_ROOT / "models" / MODEL_FILENAME
MODEL_CANDIDATES = [
    MODEL_PATH,
    PROJECT_ROOT / "data" / "raw" / "models" / MODEL_FILENAME,
]

FEEDBACK_PATH = PROJECT_ROOT / "data" / "feedback" / "predicciones.csv"
NEW_DATA_PATH = PROJECT_ROOT / "data" / "new_data" / "nuevos_registros.csv"

FEATURE_COLUMNS = [
    "MonsoonIntensity",
    "TopographyDrainage",
    "RiverManagement",
    "Deforestation",
    "Urbanization",
    "ClimateChange",
    "DamsQuality",
    "Siltation",
    "AgriculturalPractices",
    "Encroachments",
    "IneffectiveDisasterPreparedness",
    "DrainageSystems",
    "CoastalVulnerability",
    "Landslides",
    "Watersheds",
    "DeterioratingInfrastructure",
    "PopulationScore",
    "WetlandLoss",
    "InadequatePlanning",
    "PoliticalFactors",
]

FEATURE_INFO = {
    "MonsoonIntensity": ("Intensidad del monzon", "Nivel de intensidad de lluvias monzonicas."),
    "TopographyDrainage": ("Drenaje y topografia", "Capacidad del terreno para evacuar agua."),
    "RiverManagement": ("Gestion de rios", "Calidad de la gestion de cauces, rios y canales."),
    "Deforestation": ("Deforestacion", "Nivel de perdida de cobertura vegetal."),
    "Urbanization": ("Urbanizacion", "Grado de urbanizacion del area."),
    "ClimateChange": ("Cambio climatico", "Impacto estimado de eventos extremos de lluvia o inundacion."),
    "DamsQuality": ("Calidad de presas", "Estado de presas e infraestructuras de contencion."),
    "Siltation": ("Sedimentacion", "Acumulacion de sedimentos en cauces o sistemas de agua."),
    "AgriculturalPractices": ("Practicas agricolas", "Impacto de practicas agricolas sobre el terreno."),
    "Encroachments": ("Ocupacion de zonas de riesgo", "Construcciones o usos en zonas inundables."),
    "IneffectiveDisasterPreparedness": ("Preparacion ante desastres", "Falta de preparacion frente a emergencias."),
    "DrainageSystems": ("Sistemas de drenaje", "Estado de alcantarillado y drenaje urbano."),
    "CoastalVulnerability": ("Vulnerabilidad costera", "Exposicion a marejadas o subida del nivel del mar."),
    "Landslides": ("Deslizamientos de tierra", "Riesgo de deslizamientos que agraven inundaciones."),
    "Watersheds": ("Cuencas hidrograficas", "Condicion de las cuencas que recogen el agua de lluvia."),
    "DeterioratingInfrastructure": ("Infraestructura deteriorada", "Deterioro de carreteras, drenajes, puentes u obras hidraulicas."),
    "PopulationScore": ("Exposicion de poblacion", "Nivel de poblacion expuesta en la zona analizada."),
    "WetlandLoss": ("Perdida de humedales", "Perdida de zonas naturales que absorben agua."),
    "InadequatePlanning": ("Planificacion urbana inadecuada", "Deficiencias en ordenacion territorial o urbanistica."),
    "PoliticalFactors": ("Factores politicos", "Factores institucionales que afectan prevencion y respuesta."),
}

FEATURE_GUIDANCE = {
    "MonsoonIntensity": "Bajo: lluvias poco frecuentes. Medio: temporada habitual. Alto: lluvias intensas o extremas.",
    "TopographyDrainage": "Bajo: buen drenaje natural. Medio: drenaje aceptable. Alto: zonas bajas o con acumulacion de agua.",
    "RiverManagement": "Bajo: rios mantenidos. Medio: mantenimiento irregular. Alto: cauces mal gestionados.",
    "Deforestation": "Bajo: buena cobertura vegetal. Medio: perdida parcial. Alto: deforestacion notable.",
    "Urbanization": "Bajo: zona rural. Medio: area semiurbana. Alto: ciudad densa con suelo impermeable.",
    "ClimateChange": "Bajo: pocos eventos extremos. Medio: cambios moderados. Alto: aumento claro de eventos extremos.",
    "DamsQuality": "Bajo: contenciones en buen estado. Medio: mantenimiento mejorable. Alto: infraestructura insuficiente.",
    "Siltation": "Bajo: pocos sedimentos. Medio: acumulacion moderada. Alto: sedimentos que reducen el paso del agua.",
    "AgriculturalPractices": "Bajo: conservan suelo y drenaje. Medio: impacto moderado. Alto: favorecen erosion o escorrentia.",
    "Encroachments": "Bajo: sin ocupacion de cauces. Medio: ocupacion puntual. Alto: construcciones en zonas de riesgo.",
    "IneffectiveDisasterPreparedness": "Bajo: buenos planes. Medio: planes incompletos. Alto: poca preparacion.",
    "DrainageSystems": "Bajo: drenaje suficiente. Medio: drenaje limitado. Alto: alcantarillado insuficiente u obstruido.",
    "CoastalVulnerability": "Bajo: zona interior o protegida. Medio: exposicion parcial. Alto: costa muy expuesta.",
    "Landslides": "Bajo: terreno estable. Medio: pendientes o riesgo puntual. Alto: deslizamientos probables.",
    "Watersheds": "Bajo: cuenca conservada. Medio: presion moderada. Alto: cuenca degradada.",
    "DeterioratingInfrastructure": "Bajo: buen estado. Medio: deterioro parcial. Alto: infraestructura en mal estado.",
    "PopulationScore": "Bajo: poca poblacion expuesta. Medio: poblacion moderada. Alto: zona urbana densa.",
    "WetlandLoss": "Bajo: humedales conservados. Medio: perdida parcial. Alto: perdida importante.",
    "InadequatePlanning": "Bajo: planificacion adecuada. Medio: algunos problemas. Alto: crecimiento en zonas inundables.",
    "PoliticalFactors": "Bajo: buena coordinacion. Medio: gestion irregular. Alto: barreras institucionales.",
}

NOTEBOOK_CONTEXT = {
    "01_EDA.ipynb": (
        "Analisis exploratorio",
        "Revisa la calidad del dataset, la distribucion de FloodProbability, correlaciones y visualizaciones iniciales.",
    ),
    "02_modeling.ipynb": (
        "Modelado y baseline",
        "Entrena modelos iniciales, compara metricas de regresion y guarda el modelo base usado por la app.",
    ),
}


@st.cache_resource
def cargar_modelo(path):
    return joblib.load(path)


@st.cache_data
def cargar_preview(path, filas):
    return pd.read_csv(path, nrows=filas)


@st.cache_data
def cargar_rangos_variables(path):
    if not path.exists():
        return {feature: {"min": 0, "max": 20, "default": 5} for feature in FEATURE_COLUMNS}

    df = pd.read_csv(path, usecols=FEATURE_COLUMNS)
    return {
        feature: {
            "min": int(df[feature].min()),
            "max": int(df[feature].max()),
            "default": int(round(df[feature].median())),
        }
        for feature in FEATURE_COLUMNS
    }


def resolver_modelo():
    for candidate in MODEL_CANDIDATES:
        if candidate.exists():
            if candidate != MODEL_PATH:
                MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(candidate, MODEL_PATH)
                return MODEL_PATH, candidate
            return candidate, candidate
    return None, None


def guardar_fila_csv(path, fila):
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([fila]).to_csv(path, mode="a", header=not path.exists(), index=False)


def restablecer_valores(rangos_variables):
    for feature, rango in rangos_variables.items():
        st.session_state[f"input_{feature}"] = rango["default"]
    st.session_state["guardar_valor_real"] = False
    st.session_state["valor_real_pct"] = 50


def interpretar_riesgo(prediccion):
    porcentaje = prediccion * 100
    if porcentaje < 33:
        return porcentaje, "Riesgo bajo", "El modelo estima una probabilidad baja de inundacion."
    if porcentaje < 66:
        return porcentaje, "Riesgo medio", "El modelo estima una probabilidad intermedia de inundacion."
    return porcentaje, "Riesgo alto", "El modelo estima una probabilidad alta de inundacion."


def aplicar_accesibilidad(modo_vista):
    if modo_vista == "Texto grande":
        st.markdown(
            """
            <style>
            html, body, [class*="st-"] { font-size: 22px !important; }
            h1 { font-size: 3.2rem !important; }
            h2 { font-size: 2.4rem !important; }
            h3 { font-size: 1.9rem !important; }
            </style>
            """,
            unsafe_allow_html=True,
        )
    elif modo_vista == "Alto contraste":
        st.markdown(
            """
            <style>
            .stApp { background-color: #000000 !important; color: #FFFFFF !important; }
            h1, h2, h3, p, span, label, strong { color: #FFFF00 !important; }
            div[data-testid="stMarkdownContainer"] p { color: #FFFF00 !important; }
            </style>
            """,
            unsafe_allow_html=True,
        )


def renderizar_notebook_real(notebook_path):
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
                    elif output.output_type in ("execute_result", "display_data"):
                        if "text/plain" in output.data:
                            st.text(output.data["text/plain"])
                        if "image/png" in output.data:
                            st.image(base64.b64decode(output.data["image/png"]))
    except Exception as e:
        st.error(f"No se pudieron extraer algunos elementos del notebook: {e}")


def mostrar_prediccion(nombre_usuario):
    st.header("Estimador de riesgo de inundacion")
    st.write(
        "Esta vista permite introducir las condiciones de una zona y obtener una estimacion "
        "del riesgo de inundacion segun el modelo entrenado."
    )

    ruta_modelo, ruta_origen_modelo = resolver_modelo()
    if ruta_modelo is None:
        st.error("No se encontro el modelo entrenado.")
        st.info(
            "Ejecuta notebooks/02_modeling.ipynb para generar flood_baseline_model.joblib. "
            "La app lo buscara en models/ y en data/raw/models/."
        )
        return

    if ruta_origen_modelo != MODEL_PATH:
        st.success(f"Modelo encontrado en {ruta_origen_modelo} y copiado a {MODEL_PATH}.")

    modelo = cargar_modelo(ruta_modelo)
    rangos_variables = cargar_rangos_variables(DATA_PATH)

    for feature, rango in rangos_variables.items():
        st.session_state.setdefault(f"input_{feature}", rango["default"])
    st.session_state.setdefault("guardar_valor_real", False)
    st.session_state.setdefault("valor_real_pct", 50)

    if st.button("Restablecer valores recomendados"):
        restablecer_valores(rangos_variables)
        st.rerun()

    with st.form("prediction_form"):
        st.subheader("Datos de la zona a evaluar")
        st.info(
            "Los valores no son porcentajes. Cada control usa el rango real observado en el dataset. "
            "Si no conoces un factor, deja el valor recomendado."
        )

        valores = {}
        columnas_formulario = st.columns(2)
        for idx, feature in enumerate(FEATURE_COLUMNS):
            label, help_text = FEATURE_INFO[feature]
            rango = rangos_variables[feature]
            with columnas_formulario[idx % len(columnas_formulario)]:
                valores[feature] = float(
                    st.slider(
                        label,
                        min_value=rango["min"],
                        max_value=rango["max"],
                        step=1,
                        key=f"input_{feature}",
                        help=f"{help_text} {FEATURE_GUIDANCE[feature]}",
                    )
                )

        with st.expander("Guia rapida para elegir valores"):
            st.write(
                "Valores bajos significan menor presencia del factor. Valores altos significan "
                "mayor presencia del factor. El resultado final si se expresa como porcentaje."
            )
            guia = pd.DataFrame(
                [
                    {"Factor": FEATURE_INFO[feature][0], "Como decidir el valor": FEATURE_GUIDANCE[feature]}
                    for feature in FEATURE_COLUMNS
                ]
            )
            st.dataframe(guia, use_container_width=True, hide_index=True)

        guardar_valor_real = st.checkbox(
            "Conozco el resultado real y quiero guardarlo para seguimiento",
            key="guardar_valor_real",
        )
        valor_real = None
        if guardar_valor_real:
            valor_real_pct = st.slider(
                "Probabilidad real observada de inundacion (%)",
                min_value=0,
                max_value=100,
                step=1,
                key="valor_real_pct",
            )
            valor_real = valor_real_pct / 100

        submitted = st.form_submit_button("Calcular riesgo de inundacion")

    if not submitted:
        return

    input_df = pd.DataFrame([valores], columns=FEATURE_COLUMNS)
    prediccion_raw = float(modelo.predict(input_df)[0])
    prediccion = max(0.0, min(1.0, prediccion_raw))
    porcentaje, nivel_riesgo, explicacion_riesgo = interpretar_riesgo(prediccion)

    col_resultado, col_nivel = st.columns([1, 2])
    with col_resultado:
        st.metric("Probabilidad estimada de inundacion", f"{porcentaje:.2f}%")
    with col_nivel:
        st.subheader(nivel_riesgo)
        st.write(explicacion_riesgo)
        st.caption("Estimacion estadistica del modelo, no una alerta oficial.")

    if prediccion_raw < 0 or prediccion_raw > 1:
        st.warning(
            "El modelo genero un valor fuera del rango 0%-100%. "
            "La app lo limita al rango valido, pero conviene revisar estos valores."
        )

    if valor_real is not None:
        error_pct = abs(valor_real - prediccion) * 100
        st.write(f"Diferencia frente al valor real introducido: {error_pct:.2f} puntos porcentuales.")

    fila_base = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "consultor": nombre_usuario,
        "model_path": str(ruta_modelo),
        **valores,
        "prediction": prediccion,
    }
    fila_feedback = fila_base.copy()
    fila_feedback["actual_value"] = valor_real if valor_real is not None else ""
    fila_feedback["error"] = abs(valor_real - prediccion) if valor_real is not None else ""

    guardar_fila_csv(FEEDBACK_PATH, fila_feedback)
    guardar_fila_csv(NEW_DATA_PATH, fila_base)
    st.success("Resultado guardado para seguimiento del modelo y futuros reentrenamientos.")


def mostrar_informes():
    st.header("Informes tecnicos del proyecto")
    st.write(
        "Esta vista separa los notebooks de la herramienta de prediccion. "
        "Sirve para revisar el trabajo tecnico que justifica el modelo."
    )

    notebooks_dir = PROJECT_ROOT / "notebooks"
    nb_files = sorted(list(notebooks_dir.glob("*.ipynb")))
    if not nb_files:
        st.warning("No se encontraron notebooks en la carpeta notebooks/.")
        return

    nb_choice = st.selectbox(
        "Selecciona el informe tecnico",
        options=[p.name for p in nb_files],
        key="client_nb_choice",
    )
    titulo, contexto = NOTEBOOK_CONTEXT.get(
        nb_choice,
        ("Notebook tecnico", "Documento tecnico del proyecto."),
    )

    st.subheader(titulo)
    st.write(contexto)
    st.caption("El contenido siguiente procede del notebook ejecutado por el equipo.")
    st.divider()
    renderizar_notebook_real(notebooks_dir / nb_choice)


def mostrar_datos(num_rows):
    st.header("Datos y exploracion")
    st.write(
        "Esta vista permite revisar una muestra del dataset usado por el proyecto. "
        "No es necesaria para usar el predictor, pero ayuda a entender la base de datos."
    )

    if not DATA_PATH.exists():
        st.error(f"No se encontro el archivo de datos en: {DATA_PATH}")
        return

    df_preview = cargar_preview(DATA_PATH, num_rows)
    tab1, tab2 = st.tabs(["Tabla de datos", "Explorador interactivo"])

    with tab1:
        st.write(f"Mostrando las primeras {num_rows} filas del dataset:")
        st.dataframe(df_preview, use_container_width=True)

    with tab2:
        if pyg is None:
            st.warning("PyGWalker no esta instalado. La app puede seguir funcionando sin esta vista.")
            st.code("pip install pygwalker", language="bash")
        else:
            import streamlit.components.v1 as components

            pyg_html = pyg.walk(df_preview, output_type="html")
            components.html(pyg_html, height=800, scrolling=True)


st.set_page_config(page_title="Analisis de Inundaciones", layout="wide")

st.sidebar.header("Panel de control")
nombre_usuario = st.sidebar.text_input("Consultor a cargo:", value="Estudiante")
vista = st.sidebar.radio(
    "Vista",
    ["Prediccion", "Informes tecnicos", "Datos"],
)

num_rows = st.sidebar.slider(
    "Filas a cargar en la vista de datos:",
    min_value=5,
    max_value=1000,
    value=50,
    step=5,
)

modo_vista = st.sidebar.selectbox(
    "Modo de visualizacion:",
    options=["Estandar", "Texto grande", "Alto contraste"],
)
aplicar_accesibilidad(modo_vista)

st.title("Dashboard de Consultoria: Analisis de Inundaciones")
st.caption(f"Presentacion de resultados del Grupo 1. Consultor activo: {nombre_usuario}")

if vista == "Prediccion":
    mostrar_prediccion(nombre_usuario)
elif vista == "Informes tecnicos":
    mostrar_informes()
else:
    mostrar_datos(num_rows)
