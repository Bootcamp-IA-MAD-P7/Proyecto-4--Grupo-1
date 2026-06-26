from datetime import datetime
from pathlib import Path
import base64
import csv
import shutil
import sys

import joblib
import nbformat
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

BASE = Path(__file__).parent
PROJECT_ROOT = BASE.parent
for import_path in (BASE, PROJECT_ROOT):
    if str(import_path) not in sys.path:
        sys.path.append(str(import_path))

from paths import get_data_path

try:
    import pygwalker as pyg
except ModuleNotFoundError:
    pyg = None


from src import database
from src.features import add_engineered_features, summarize_engineered_features
from src.pipeline import build_retraining_dataset

DATA_PATH = get_data_path("train.csv")

MODEL_FILENAME = "flood_baseline_model.joblib"
MODEL_NAME = "Linear Regression Baseline"
MODEL_VERSION = "baseline_v1"
MODEL_PATH = PROJECT_ROOT / "models" / MODEL_FILENAME
MODEL_CANDIDATES = [
    MODEL_PATH,
    PROJECT_ROOT / "data" / "raw" / "models" / MODEL_FILENAME,
]

FEEDBACK_PATH = PROJECT_ROOT / "data" / "feedback" / "predicciones.csv"
NEW_DATA_PATH = PROJECT_ROOT / "data" / "new_data" / "nuevos_registros.csv"
RETRAINING_DATASET_PATH = PROJECT_ROOT / "data" / "processed" / "retraining_dataset.csv"
DATABASE_PATH = PROJECT_ROOT / "data" / "database" / "flood_app.sqlite"
STYLE_PATH = BASE / "style.css"
WEATHER_BACKGROUND_PATH = BASE / "assets" / "weather-dashboard-bg.jpg"

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
    "MonsoonIntensity": ("Intensidad del monzón", "Nivel de intensidad de lluvias monzónicas."),
    "TopographyDrainage": ("Drenaje y topografía", "Capacidad del terreno para evacuar agua."),
    "RiverManagement": ("Gestión de ríos", "Calidad de la gestión de cauces, ríos y canales."),
    "Deforestation": ("Deforestación", "Nivel de pérdida de cobertura vegetal."),
    "Urbanization": ("Urbanización", "Grado de urbanización del área."),
    "ClimateChange": ("Cambio climático", "Impacto estimado de eventos extremos de lluvia o inundación."),
    "DamsQuality": ("Calidad de presas", "Estado de presas e infraestructuras de contención."),
    "Siltation": ("Sedimentación", "Acumulación de sedimentos en cauces o sistemas de agua."),
    "AgriculturalPractices": ("Prácticas agrícolas", "Impacto de prácticas agrícolas sobre el terreno."),
    "Encroachments": ("Ocupación de zonas de riesgo", "Construcciones o usos en zonas inundables."),
    "IneffectiveDisasterPreparedness": ("Preparación ante desastres", "Falta de preparación frente a emergencias."),
    "DrainageSystems": ("Sistemas de drenaje", "Estado de alcantarillado y drenaje urbano."),
    "CoastalVulnerability": ("Vulnerabilidad costera", "Exposición a marejadas o subida del nivel del mar."),
    "Landslides": ("Deslizamientos de tierra", "Riesgo de deslizamientos que agraven inundaciones."),
    "Watersheds": ("Cuencas hidrográficas", "Condición de las cuencas que recogen el agua de lluvia."),
    "DeterioratingInfrastructure": ("Infraestructura deteriorada", "Deterioro de carreteras, drenajes, puentes u obras hidráulicas."),
    "PopulationScore": ("Exposición de población", "Nivel de población expuesta en la zona analizada."),
    "WetlandLoss": ("Pérdida de humedales", "Pérdida de zonas naturales que absorben agua."),
    "InadequatePlanning": ("Planificación urbana inadecuada", "Deficiencias en ordenación territorial o urbanística."),
    "PoliticalFactors": ("Factores políticos", "Factores institucionales que afectan prevención y respuesta."),
}

FEATURE_GUIDANCE = {
    "MonsoonIntensity": "Bajo: lluvias poco frecuentes. Medio: temporada habitual. Alto: lluvias intensas o extremas.",
    "TopographyDrainage": "Bajo: buen drenaje natural. Medio: drenaje aceptable. Alto: zonas bajas o con acumulación de agua.",
    "RiverManagement": "Bajo: ríos mantenidos. Medio: mantenimiento irregular. Alto: cauces mal gestionados.",
    "Deforestation": "Bajo: buena cobertura vegetal. Medio: pérdida parcial. Alto: deforestación notable.",
    "Urbanization": "Bajo: zona rural. Medio: área semiurbana. Alto: ciudad densa con suelo impermeable.",
    "ClimateChange": "Bajo: pocos eventos extremos. Medio: cambios moderados. Alto: aumento claro de eventos extremos.",
    "DamsQuality": "Bajo: contenciones en buen estado. Medio: mantenimiento mejorable. Alto: infraestructura insuficiente.",
    "Siltation": "Bajo: pocos sedimentos. Medio: acumulación moderada. Alto: sedimentos que reducen el paso del agua.",
    "AgriculturalPractices": "Bajo: conservan suelo y drenaje. Medio: impacto moderado. Alto: favorecen erosión o escorrentía.",
    "Encroachments": "Bajo: sin ocupación de cauces. Medio: ocupación puntual. Alto: construcciones en zonas de riesgo.",
    "IneffectiveDisasterPreparedness": "Bajo: buenos planes. Medio: planes incompletos. Alto: poca preparación.",
    "DrainageSystems": "Bajo: drenaje suficiente. Medio: drenaje limitado. Alto: alcantarillado insuficiente u obstruido.",
    "CoastalVulnerability": "Bajo: zona interior o protegida. Medio: exposición parcial. Alto: costa muy expuesta.",
    "Landslides": "Bajo: terreno estable. Medio: pendientes o riesgo puntual. Alto: deslizamientos probables.",
    "Watersheds": "Bajo: cuenca conservada. Medio: presión moderada. Alto: cuenca degradada.",
    "DeterioratingInfrastructure": "Bajo: buen estado. Medio: deterioro parcial. Alto: infraestructura en mal estado.",
    "PopulationScore": "Bajo: poca población expuesta. Medio: población moderada. Alto: zona urbana densa.",
    "WetlandLoss": "Bajo: humedales conservados. Medio: pérdida parcial. Alto: pérdida importante.",
    "InadequatePlanning": "Bajo: planificación adecuada. Medio: algunos problemas. Alto: crecimiento en zonas inundables.",
    "PoliticalFactors": "Bajo: buena coordinación. Medio: gestión irregular. Alto: barreras institucionales.",
}

DEFAULT_VARIABLE_RANGES = {
    "MonsoonIntensity": {"min": 0, "max": 16, "default": 5},
    "TopographyDrainage": {"min": 0, "max": 18, "default": 5},
    "RiverManagement": {"min": 0, "max": 16, "default": 5},
    "Deforestation": {"min": 0, "max": 17, "default": 5},
    "Urbanization": {"min": 0, "max": 17, "default": 5},
    "ClimateChange": {"min": 0, "max": 17, "default": 5},
    "DamsQuality": {"min": 0, "max": 16, "default": 5},
    "Siltation": {"min": 0, "max": 16, "default": 5},
    "AgriculturalPractices": {"min": 0, "max": 16, "default": 5},
    "Encroachments": {"min": 0, "max": 18, "default": 5},
    "IneffectiveDisasterPreparedness": {"min": 0, "max": 16, "default": 5},
    "DrainageSystems": {"min": 0, "max": 17, "default": 5},
    "CoastalVulnerability": {"min": 0, "max": 17, "default": 5},
    "Landslides": {"min": 0, "max": 16, "default": 5},
    "Watersheds": {"min": 0, "max": 16, "default": 5},
    "DeterioratingInfrastructure": {"min": 0, "max": 17, "default": 5},
    "PopulationScore": {"min": 0, "max": 18, "default": 5},
    "WetlandLoss": {"min": 0, "max": 19, "default": 5},
    "InadequatePlanning": {"min": 0, "max": 16, "default": 5},
    "PoliticalFactors": {"min": 0, "max": 16, "default": 5},
}

NOTEBOOK_CONTEXT = {
    "01_EDA.ipynb": (
        "Análisis exploratorio",
        "Revisa la calidad del dataset, la distribución de FloodProbability, correlaciones y visualizaciones iniciales.",
    ),
    "02_modeling.ipynb": (
        "Modelado y baseline",
        "Entrena modelos iniciales, compara métricas de regresión y guarda el modelo base usado por la app.",
    ),
}


def mostrar_tarjeta(titulo, texto, color="#F8FAFC", borde="#CBD5E1"):
    st.markdown(
        f"""
        <div style="
            background:{color};
            border-left: 6px solid {borde};
            padding: 1rem 1.1rem;
            border-radius: 0.5rem;
            margin: 0.6rem 0 1rem 0;
            color:#0F172A;
        ">
            <strong style="color:#0F172A;">{titulo}</strong>
            <p style="margin:0.35rem 0 0 0;color:#1E293B;">{texto}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def aplicar_estilo_visual():
    css = STYLE_PATH.read_text(encoding="utf-8") if STYLE_PATH.exists() else ""
    background_css = ""
    if WEATHER_BACKGROUND_PATH.exists():
        image_b64 = base64.b64encode(WEATHER_BACKGROUND_PATH.read_bytes()).decode("utf-8")
        background_css = f":root {{ --weather-bg: url('data:image/png;base64,{image_b64}'); }}"

    st.markdown(f"<style>{background_css}\n{css}</style>", unsafe_allow_html=True)


def guardar_registro_base_datos(fila):
    try:
        database.save_prediction_record(DATABASE_PATH, fila, FEATURE_COLUMNS)
        backend = database.get_database_backend(DATABASE_PATH)
        return True, f"Registro guardado tambien en la base de datos ({backend['engine']})."
    except Exception as exc:
        return False, f"No se pudo guardar en la base de datos: {exc}"


def mostrar_cabecera(nombre_usuario):
    st.markdown(
        f"""
        <section class="app-hero">
            <div>
                <p class="app-hero__eyebrow">Flood Risk Intelligence</p>
                <h1>Centro de análisis de inundaciones</h1>
                <p class="app-hero__subtitle">
                    Predicción, monitorización, base de datos y pipeline de ingesta para apoyar decisiones de riesgo.
                </p>
            </div>
            <div class="app-hero__meta">
                <span>Grupo 1</span>
                <strong>{nombre_usuario}</strong>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


@st.cache_resource
def cargar_modelo(path):
    return joblib.load(path)


@st.cache_data
def cargar_preview(path, filas):
    return pd.read_csv(path, nrows=filas)


@st.cache_data
def cargar_rangos_variables(path):
    if not path.exists():
        return DEFAULT_VARIABLE_RANGES

    df = pd.read_csv(path, usecols=FEATURE_COLUMNS)
    return {
        feature: {
            "min": int(df[feature].min()),
            "max": int(df[feature].max()),
            "default": int(round(df[feature].median())),
        }
        for feature in FEATURE_COLUMNS
    }


def crear_muestra_demo_dataset(filas):
    rows = []
    for idx in range(filas):
        row = {"id": idx}
        for feature_idx, feature in enumerate(FEATURE_COLUMNS):
            feature_range = DEFAULT_VARIABLE_RANGES[feature]
            span = feature_range["max"] - feature_range["min"] + 1
            row[feature] = int(feature_range["min"] + ((idx + feature_idx) % span))
        row["FloodProbability"] = round(0.25 + ((idx % 10) * 0.05), 3)
        rows.append(row)
    return pd.DataFrame(rows)


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
    if path.exists():
        columnas_actuales = leer_columnas_csv(path)
        columnas_nuevas = list(fila.keys())
        if columnas_actuales and columnas_actuales != columnas_nuevas:
            try:
                df_existente = pd.read_csv(path)
            except (pd.errors.ParserError, pd.errors.EmptyDataError):
                crear_backup_csv(path)
            else:
                df_nuevo = pd.DataFrame([fila])
                columnas_finales = list(dict.fromkeys([*df_existente.columns, *df_nuevo.columns]))
                df_existente = df_existente.reindex(columns=columnas_finales)
                df_nuevo = df_nuevo.reindex(columns=columnas_finales)
                pd.concat([df_existente, df_nuevo], ignore_index=True).to_csv(path, index=False)
                return
    pd.DataFrame([fila]).to_csv(path, mode="a", header=not path.exists(), index=False)


def leer_columnas_csv(path):
    try:
        with path.open("r", encoding="utf-8", newline="") as file:
            return next(csv.reader(file), [])
    except (OSError, StopIteration):
        return []


def crear_backup_csv(path):
    if not path.exists():
        return None
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = path.with_name(f"{path.stem}_backup_{timestamp}{path.suffix}")
    shutil.copy2(path, backup_path)
    path.unlink()
    return backup_path


def crear_copia_seguridad_csv(path, motivo):
    if not path.exists():
        return None
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = path.with_name(f"{path.stem}_{motivo}_{timestamp}{path.suffix}")
    shutil.copy2(path, backup_path)
    return backup_path


def crear_prediction_id():
    return datetime.now().strftime("pred_%Y%m%d_%H%M%S_%f")


def normalizar_feedback_df(feedback_df):
    feedback_df = feedback_df.copy()
    if "model_name" not in feedback_df.columns:
        feedback_df["model_name"] = MODEL_NAME
    if "model_version" not in feedback_df.columns:
        feedback_df["model_version"] = MODEL_VERSION
    if "model_file" not in feedback_df.columns:
        feedback_df["model_file"] = MODEL_FILENAME
    if "prediction_id" not in feedback_df.columns:
        feedback_df.insert(0, "prediction_id", "")

    ids_vacios = feedback_df["prediction_id"].isna() | (feedback_df["prediction_id"].astype(str).str.strip() == "")
    if ids_vacios.any():
        for idx in feedback_df[ids_vacios].index:
            timestamp = str(feedback_df.at[idx, "timestamp"]) if "timestamp" in feedback_df.columns else "sin_fecha"
            timestamp = timestamp.replace(":", "").replace("-", "").replace(" ", "_")
            feedback_df.at[idx, "prediction_id"] = f"pred_legacy_{idx}_{timestamp}"

    return feedback_df


def normalizar_nuevos_datos_df(new_data_df):
    new_data_df = new_data_df.copy()
    if "prediction_id" not in new_data_df.columns:
        new_data_df.insert(0, "prediction_id", "")
    if "actual_value" not in new_data_df.columns:
        new_data_df["actual_value"] = ""
    if "record_status" not in new_data_df.columns:
        new_data_df["record_status"] = ""

    ids_vacios = new_data_df["prediction_id"].isna() | (new_data_df["prediction_id"].astype(str).str.strip() == "")
    if ids_vacios.any():
        for idx in new_data_df[ids_vacios].index:
            timestamp = str(new_data_df.at[idx, "timestamp"]) if "timestamp" in new_data_df.columns else "sin_fecha"
            timestamp = timestamp.replace(":", "").replace("-", "").replace(" ", "_")
            new_data_df.at[idx, "prediction_id"] = f"new_legacy_{idx}_{timestamp}"

    new_data_df["actual_value"] = pd.to_numeric(new_data_df["actual_value"], errors="coerce")
    current_status = new_data_df["record_status"].astype(str)
    new_data_df["record_status"] = np.select(
        [
            current_status.eq("ingested_for_retraining"),
            new_data_df["actual_value"].notna(),
        ],
        [
            "ingested_for_retraining",
            "validated_for_retraining",
        ],
        default="pending_target",
    )
    return new_data_df


def actualizar_valor_real_nuevos_datos(path, prediction_id, valor_real):
    if not path.exists():
        return

    try:
        new_data_df = pd.read_csv(path)
    except (pd.errors.ParserError, pd.errors.EmptyDataError):
        crear_backup_csv(path)
        return

    new_data_df = normalizar_nuevos_datos_df(new_data_df)
    mask = new_data_df["prediction_id"].astype(str) == str(prediction_id)
    if not mask.any():
        return

    new_data_df.loc[mask, "actual_value"] = valor_real
    new_data_df.loc[mask, "record_status"] = "validated_for_retraining"
    new_data_df.to_csv(path, index=False)


def actualizar_valor_real_feedback(path, prediction_id, valor_real, new_data_path=None):
    if not path.exists():
        return False, "No existe el archivo de feedback."

    try:
        feedback_df = pd.read_csv(path)
    except (pd.errors.ParserError, pd.errors.EmptyDataError):
        backup_path = crear_backup_csv(path)
        return False, f"El archivo de feedback tenía formato incorrecto. Se guardó backup: {backup_path.name}."

    feedback_df = normalizar_feedback_df(feedback_df)
    feedback_df["prediction"] = pd.to_numeric(feedback_df.get("prediction"), errors="coerce")
    mask = feedback_df["prediction_id"].astype(str) == str(prediction_id)

    if not mask.any():
        return False, "No se encontró la predicción seleccionada."

    prediction = feedback_df.loc[mask, "prediction"].iloc[0]
    if pd.isna(prediction):
        return False, "La predicción seleccionada no tiene un valor numérico válido."

    feedback_df.loc[mask, "actual_value"] = valor_real
    feedback_df.loc[mask, "error"] = abs(float(valor_real) - float(prediction))
    feedback_df.loc[mask, "record_status"] = "validated_for_retraining"
    path.parent.mkdir(parents=True, exist_ok=True)
    feedback_df.to_csv(path, index=False)
    if new_data_path is not None:
        actualizar_valor_real_nuevos_datos(new_data_path, prediction_id, valor_real)
    db_warning = ""
    try:
        database.update_actual_value(DATABASE_PATH, str(prediction_id), float(valor_real), float(prediction))
    except Exception as exc:
        db_warning = f" Aviso: no se pudo actualizar la base de datos local ({exc})."
    cargar_feedback.clear()
    return True, f"Valor real guardado. Las métricas se han actualizado.{db_warning}"


def eliminar_prediccion_registrada(feedback_path, new_data_path, prediction_id):
    if not feedback_path.exists():
        return False, "No existe el archivo de feedback."

    try:
        feedback_df = pd.read_csv(feedback_path)
    except (pd.errors.ParserError, pd.errors.EmptyDataError):
        backup_path = crear_backup_csv(feedback_path)
        return False, f"El archivo de feedback tenía formato incorrecto. Se guardó backup: {backup_path.name}."

    feedback_df = normalizar_feedback_df(feedback_df)
    mask_feedback = feedback_df["prediction_id"].astype(str) == str(prediction_id)
    if not mask_feedback.any():
        return False, "No se encontró la predicción seleccionada en feedback."

    backup_feedback = crear_copia_seguridad_csv(feedback_path, "antes_eliminar")
    feedback_df = feedback_df.loc[~mask_feedback].copy()
    feedback_df.to_csv(feedback_path, index=False)

    backup_new_data = None
    if new_data_path.exists():
        try:
            new_data_df = pd.read_csv(new_data_path)
        except (pd.errors.ParserError, pd.errors.EmptyDataError):
            backup_new_data = crear_backup_csv(new_data_path)
        else:
            if "prediction_id" in new_data_df.columns:
                mask_new_data = new_data_df["prediction_id"].astype(str) == str(prediction_id)
                if mask_new_data.any():
                    backup_new_data = crear_copia_seguridad_csv(new_data_path, "antes_eliminar")
                    new_data_df = new_data_df.loc[~mask_new_data].copy()
                    new_data_df.to_csv(new_data_path, index=False)

    db_warning = ""
    try:
        database.delete_prediction_record(DATABASE_PATH, str(prediction_id))
    except Exception as exc:
        db_warning = f" Aviso: no se pudo actualizar la base de datos local ({exc})."

    cargar_feedback.clear()
    backups = [backup.name for backup in [backup_feedback, backup_new_data] if backup is not None]
    detalle_backup = f" Copia de seguridad: {', '.join(backups)}." if backups else ""
    return True, f"Predicción eliminada del histórico local.{detalle_backup}{db_warning}"


def restablecer_valores(rangos_variables):
    for feature, rango in rangos_variables.items():
        st.session_state[f"input_{feature}"] = rango["default"]
    st.session_state["guardar_valor_real"] = False
    st.session_state["valor_real_pct"] = 50


def interpretar_riesgo(prediccion):
    porcentaje = prediccion * 100
    if porcentaje < 33:
        return porcentaje, "Riesgo bajo", "El modelo estima una probabilidad baja de inundación."
    if porcentaje < 66:
        return porcentaje, "Riesgo medio", "El modelo estima una probabilidad intermedia de inundación."
    return porcentaje, "Riesgo alto", "El modelo estima una probabilidad alta de inundación."


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


def reparar_texto(texto):
    if not isinstance(texto, str):
        return texto
    if not any(marca in texto for marca in ("Ã", "Â", "â", "�")):
        return texto
    try:
        return texto.encode("latin1").decode("utf-8")
    except UnicodeError:
        return texto


def renderizar_notebook_real(notebook_path):
    try:
        with open(notebook_path, "r", encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)

        for cell in nb.cells:
            if cell.cell_type == "markdown":
                st.markdown(reparar_texto(cell.source))
            elif cell.cell_type == "code":
                for output in cell.outputs:
                    if output.output_type == "stream":
                        st.markdown(
                            f"<div class='notebook-output'><pre>{reparar_texto(output.text)}</pre></div>",
                            unsafe_allow_html=True,
                        )
                    elif output.output_type in ("execute_result", "display_data"):
                        if "text/html" in output.data:
                            st.markdown(
                                f"<div class='notebook-output'>{reparar_texto(output.data['text/html'])}</div>",
                                unsafe_allow_html=True,
                            )
                        elif "text/plain" in output.data:
                            st.markdown(
                                f"<div class='notebook-output'><pre>{reparar_texto(output.data['text/plain'])}</pre></div>",
                                unsafe_allow_html=True,
                            )
                        if "image/png" in output.data:
                            st.image(base64.b64decode(output.data["image/png"]))
    except Exception as e:
        st.error(f"No se pudieron extraer algunos elementos del notebook: {e}")


def mostrar_guia_uso():
    st.header("Guía del proyecto y uso de la aplicación")
    st.write(
        "Esta pantalla explica qué hace la solución, cómo usarla y cómo interpretar las partes "
        "principales de un proyecto de regresión sin necesidad de entrar en detalle técnico."
    )

    col_objetivo, col_ciclo = st.columns([1, 1])
    with col_objetivo:
        mostrar_tarjeta(
            "Qué problema resuelve",
            "La app estima una variable numérica: la probabilidad de inundación. "
            "Para ello usa factores de riesgo como lluvia, drenaje, urbanización, presas, planificación o vulnerabilidad costera.",
            color="#E0F2FE",
            borde="#0284C7",
        )
    with col_ciclo:
        mostrar_tarjeta(
            "Qué ciclo cubre",
            "Permite predecir, guardar feedback, comparar con valores reales, monitorizar errores, "
            "guardar datos en base de datos y preparar casos validados para futuros reentrenamientos.",
            color="#ECFDF5",
            borde="#059669",
        )

    st.markdown(
        """
        <div class="app-flow">
            <div><strong>1. Explorar</strong><span>EDA y comprensión del dataset</span></div>
            <div><strong>2. Entrenar</strong><span>Modelo de regresión y métricas</span></div>
            <div><strong>3. Usar</strong><span>Predicción desde Streamlit</span></div>
            <div><strong>4. Medir</strong><span>Feedback, valor real y errores</span></div>
            <div><strong>5. Preparar</strong><span>Pipeline de ingesta para reentrenar</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_resumen, tab_modelo, tab_app, tab_metricas, tab_pipeline, tab_ejemplo = st.tabs(
        [
            "Qué hace",
            "Modelo y EDA",
            "Cómo se usa",
            "Cómo interpretar",
            "Pipeline y features",
            "Ejemplo práctico",
        ]
    )

    with tab_resumen:
        st.subheader("Qué hace esta aplicación")
        st.markdown(
            """
            La aplicación convierte el trabajo de notebooks en una herramienta usable.

            - **Recibe datos de una zona** mediante controles sencillos.
            - **Calcula una probabilidad estimada de inundación** usando el modelo entrenado.
            - **Guarda cada predicción** para poder revisarla después.
            - **Permite añadir el valor real observado** cuando se conozca.
            - **Compara predicción y realidad** para monitorizar si el modelo funciona bien.
            - **Guarda los datos recogidos en base de datos**: SQLite en local y PostgreSQL persistente en Render.
            - **Prepara un dataset de reentrenamiento** con los casos que ya tienen valor real.
            """
        )

        st.subheader("Por qué esto es regresión")
        st.write(
            "Es un problema de regresión porque el modelo no clasifica en categorías cerradas, sino que predice "
            "un número continuo: `FloodProbability`. La app lo muestra como porcentaje para que sea más fácil de leer."
        )

        st.subheader("Como leer los valores de entrada")
        st.write(
            "Los controles de Prediccion no son porcentajes. Son puntuaciones discretas del dataset: "
            "un valor bajo indica menor presencia del factor y un valor alto indica mayor intensidad o presencia. "
            "Cada variable usa su rango real observado en entrenamiento; por ejemplo, algunas llegan a 16, otras a 18 o 19. "
            "La probabilidad final de inundacion si se muestra como porcentaje."
        )

    with tab_modelo:
        st.subheader("Qué aporta el EDA")
        st.write(
            "El EDA sirve para conocer el dataset antes de entrenar. Ayuda a ver la distribución de la variable objetivo, "
            "detectar patrones, revisar correlaciones y comprobar si las variables tienen sentido para explicar el riesgo."
        )
        eda_df = pd.DataFrame(
            [
                {
                    "Elemento": "Distribución de FloodProbability",
                    "Para qué sirve": "Ver si los valores están concentrados, equilibrados o tienen comportamientos raros.",
                },
                {
                    "Elemento": "Correlaciones",
                    "Para qué sirve": "Identificar qué factores se relacionan más con la probabilidad de inundación.",
                },
                {
                    "Elemento": "Scatter plots",
                    "Para qué sirve": "Ver relaciones entre variables y detectar tendencias visuales.",
                },
                {
                    "Elemento": "Histogramas",
                    "Para qué sirve": "Entender cómo se distribuyen los factores de riesgo.",
                },
            ]
        )
        st.dataframe(eda_df, width="stretch", hide_index=True)

        st.subheader("Cómo se construyó el modelo")
        st.markdown(
            """
            El proyecto parte de un modelo baseline funcional y después compara técnicas más avanzadas:

            - **Linear Regression:** modelo base usado por la app.
            - **Random Forest / Gradient Boosting / XGBoost / LightGBM:** modelos ensemble comparados en notebooks.
            - **Validación cruzada K-Fold:** divide los datos en varias particiones para medir si el rendimiento es estable.
            - **Optimización de hiperparámetros:** prueba combinaciones de configuración para intentar mejorar resultados.

            La app usa el modelo guardado en `models/flood_baseline_model.joblib`. Los notebooks justifican la selección y el rendimiento.
            """
        )

    with tab_app:
        st.subheader("Cómo se usa la app")
        uso_df = pd.DataFrame(
            [
                {
                    "Vista": "Predicción",
                    "Qué haces": "Introduces los factores de riesgo y calculas una estimación.",
                    "Qué obtienes": "Probabilidad estimada de inundación y registro guardado.",
                },
                {
                    "Vista": "Monitorización",
                    "Qué haces": "Añades valores reales cuando estén disponibles.",
                    "Qué obtienes": "Errores, métricas acumuladas y gráficas; en Render se cargan desde PostgreSQL.",
                },
                {
                    "Vista": "Base de datos",
                    "Qué haces": "Compruebas que las predicciones se han guardado.",
                    "Qué obtienes": "Motor activo, conteo de registros y últimos datos almacenados.",
                },
                {
                    "Vista": "Pipeline de reentrenamiento",
                    "Qué haces": "Ejecutas el pipeline de ingesta con casos validados.",
                    "Qué obtienes": "Dataset preparado para futuros reentrenamientos.",
                },
                {
                    "Vista": "Informes técnicos",
                    "Qué haces": "Revisas notebooks y resultados del trabajo técnico.",
                    "Qué obtienes": "EDA, modelado, métricas y conclusiones.",
                },
            ]
        )
        st.dataframe(uso_df, width="stretch", hide_index=True)

        st.info(
            "Si no conoces el valor real, puedes usar la app igualmente. El registro queda pendiente y se puede completar más tarde."
        )

    with tab_metricas:
        st.subheader("Cómo interpretar el rendimiento")
        metricas_df = pd.DataFrame(
            [
                {
                    "Métrica": "MAE",
                    "Lectura simple": "Error medio absoluto. Cuanto más bajo, mejor.",
                },
                {
                    "Métrica": "RMSE",
                    "Lectura simple": "Penaliza más los errores grandes. Cuanto más bajo, mejor.",
                },
                {
                    "Métrica": "R²",
                    "Lectura simple": "Indica cuánto explica el modelo. Más cerca de 1 suele ser mejor.",
                },
                {
                    "Métrica": "Overfitting",
                    "Lectura simple": "Compara train y validación. Si la diferencia es baja, el modelo generaliza mejor.",
                },
            ]
        )
        st.dataframe(metricas_df, width="stretch", hide_index=True)

        st.write(
            "En la app, estas métricas solo tienen sentido cuando existen valores reales. Sin valor real, la app puede guardar "
            "predicciones, pero no puede saber si el modelo acertó."
        )

    with tab_pipeline:
        st.subheader("Por qué existe el pipeline de ingesta")
        st.write(
            "Un modelo no debería quedarse congelado para siempre. Si la app se usa y después se conocen valores reales, "
            "esos casos pueden convertirse en datos supervisados nuevos. El pipeline ordena ese proceso."
        )

        st.markdown(
            """
            **Qué hace el botón `Ejecutar pipeline de ingesta`:**

            1. Revisa los registros generados por la app.
            2. Se queda solo con los que tienen valor real confirmado.
            3. Construye un dataset con la variable objetivo `FloodProbability`.
            4. Añade indicadores de feature engineering.
            5. Guarda `data/processed/retraining_dataset.csv`.
            6. Marca esos registros como ingeridos para que salgan de la cola.

            Si todavia no hay valores reales confirmados, el boton aparece bloqueado. Eso significa que el pipeline
            existe, pero esta esperando datos validos para preparar el dataset.

            Este botón **no cambia el modelo activo**. Deja los datos preparados para un reentrenamiento posterior.
            """
        )

        st.subheader("Qué es feature engineering en esta app")
        st.write(
            "Feature engineering significa crear variables nuevas a partir de las originales para ayudar a interpretar o mejorar "
            "el modelo. Aquí no pedimos al usuario más datos: agrupamos los factores existentes en indicadores compuestos."
        )
        features_df = pd.DataFrame(
            [
                {"Indicador": "risk_score_sum", "Qué resume": "Suma total de factores de riesgo."},
                {"Indicador": "risk_score_mean", "Qué resume": "Riesgo medio general."},
                {"Indicador": "water_pressure_risk", "Qué resume": "Lluvia, drenaje, ríos, sedimentación y cuencas."},
                {"Indicador": "environmental_risk", "Qué resume": "Deforestación, humedales, clima y prácticas agrícolas."},
                {"Indicador": "infrastructure_risk", "Qué resume": "Presas, drenaje e infraestructura deteriorada."},
                {"Indicador": "planning_risk", "Qué resume": "Urbanización, planificación, ocupación y factores políticos."},
                {"Indicador": "exposure_risk", "Qué resume": "Población expuesta, costa, deslizamientos y preparación."},
            ]
        )
        st.dataframe(features_df, width="stretch", hide_index=True)

    with tab_ejemplo:
        st.subheader("Ejemplo práctico: de una predicción a datos para reentrenar")
        st.write(
            "Imagina que una consultora quiere evaluar una zona antes de una temporada de lluvias. "
            "La app le permite hacer una estimación, guardarla y convertirla más tarde en información útil para mejorar el modelo."
        )

        ejemplo_df = pd.DataFrame(
            [
                {
                    "Paso": "1. Evaluar una zona",
                    "Qué haces": "Entras en Predicción y ajustas los factores de riesgo.",
                    "Cómo interpretarlo": "Valores altos indican más presencia del factor: más lluvia, peor drenaje, más urbanización, etc.",
                },
                {
                    "Paso": "2. Calcular riesgo",
                    "Qué haces": "Pulsas Calcular riesgo de inundación.",
                    "Cómo interpretarlo": "La app devuelve una probabilidad estimada. No es una alerta oficial, es una estimación estadística.",
                },
                {
                    "Paso": "3. Guardar seguimiento",
                    "Qué haces": "La predicción se guarda automáticamente.",
                    "Cómo interpretarlo": "Aunque no haya valor real todavía, ya existe un registro para revisar después.",
                },
                {
                    "Paso": "4. Añadir valor real",
                    "Qué haces": "Cuando se conozca el dato observado, lo completas en Monitorización.",
                    "Cómo interpretarlo": "La app ya puede comparar lo que predijo con lo que pasó realmente.",
                },
                {
                    "Paso": "5. Leer métricas",
                    "Qué haces": "Revisas MAE, RMSE y R² en Monitorización.",
                    "Cómo interpretarlo": "MAE/RMSE bajos indican menor error. R² ayuda a ver si el modelo explica bien la variación.",
                },
                {
                    "Paso": "6. Comprobar persistencia",
                    "Qué haces": "Entras en Base de datos.",
                    "Cómo interpretarlo": "Ves si la predicción quedó guardada. En Render debe aparecer PostgreSQL persistente.",
                },
                {
                    "Paso": "7. Preparar reentrenamiento",
                    "Qué haces": "En Pipeline de reentrenamiento pulsas Ejecutar pipeline de ingesta.",
                    "Cómo interpretarlo": "Si el boton esta activo, hay casos con valor real. Solo esos casos pasan al dataset validado.",
                },
            ]
        )
        st.dataframe(ejemplo_df, width="stretch", hide_index=True)

        st.subheader("Qué haría después el equipo")
        st.markdown(
            """
            - Revisar si hay suficientes casos validados.
            - Comparar las métricas nuevas con las del modelo actual.
            - Decidir si merece la pena reentrenar.
            - Entrenar una nueva versión en notebook o script.
            - Sustituir el modelo activo solo si mejora de forma clara.

            La idea es que la app no sea solo un formulario de predicción, sino una herramienta para cerrar el ciclo:
            **predecir, observar, medir y preparar mejores datos**.
            """
        )


def mostrar_prediccion(nombre_usuario):
    st.header("Estimador de riesgo de inundación")
    st.write(
        "Esta vista permite introducir las condiciones de una zona y obtener una estimación "
        "del riesgo de inundación según el modelo entrenado."
    )
    with st.expander("Antes de calcular: qué hacer con el valor real"):
        st.markdown(
            """
            - Si solo quieres obtener una predicción, deja sin marcar **Guardar también el valor real observado**.
            - Si conoces el dato real o confirmado, marca la casilla e introduce ese porcentaje.
            - El valor real permite calcular errores en **Monitorización**.
            - Aunque no guardes valor real, la predicción se conserva como nuevo registro para análisis futuros.
            """
        )

    ruta_modelo, ruta_origen_modelo = resolver_modelo()
    if ruta_modelo is None:
        st.error("No se encontró el modelo entrenado.")
        st.info(
            "Ejecuta notebooks/02_modeling.ipynb para generar flood_baseline_model.joblib. "
            "La app lo buscará en models/ y en data/raw/models/."
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

        with st.expander("Guía rápida para elegir valores"):
            st.write(
                "Valores bajos significan menor presencia del factor. Valores altos significan "
                "mayor presencia del factor. El resultado final sí se expresa como porcentaje."
            )
            guia = pd.DataFrame(
                [
                    {"Factor": FEATURE_INFO[feature][0], "Cómo decidir el valor": FEATURE_GUIDANCE[feature]}
                    for feature in FEATURE_COLUMNS
                ]
            )
            st.dataframe(guia, width="stretch", hide_index=True)

        st.markdown("### Seguimiento del resultado real")
        st.caption(
            "El valor real es el dato observado o confirmado posteriormente. "
            "Sirve para comparar la predicción con la realidad y calcular métricas de rendimiento."
        )
        guardar_valor_real = st.checkbox(
            "Guardar también el valor real observado",
            key="guardar_valor_real",
        )
        valor_real_pct = st.slider(
            "Valor real observado de inundación (%)",
            min_value=0,
            max_value=100,
            step=1,
            key="valor_real_pct",
            help="Solo se guardará si marcas la casilla anterior.",
        )
        valor_real = valor_real_pct / 100 if guardar_valor_real else None

        submitted = st.form_submit_button("Calcular riesgo de inundación")

    if not submitted:
        return

    input_df = pd.DataFrame([valores], columns=FEATURE_COLUMNS)
    engineered_summary = summarize_engineered_features(input_df)
    prediccion_raw = float(modelo.predict(input_df)[0])
    prediccion = max(0.0, min(1.0, prediccion_raw))
    porcentaje, nivel_riesgo, explicacion_riesgo = interpretar_riesgo(prediccion)

    col_resultado, col_nivel = st.columns([1, 2])
    with col_resultado:
        st.metric("Probabilidad estimada de inundación", f"{porcentaje:.2f}%")
    with col_nivel:
        st.subheader(nivel_riesgo)
        st.write(explicacion_riesgo)
        st.caption("Estimación estadística del modelo, no una alerta oficial.")

    if prediccion_raw < 0 or prediccion_raw > 1:
        st.warning(
            "El modelo generó un valor fuera del rango 0%-100%. "
            "La app lo limita al rango válido, pero conviene revisar estos valores."
        )

    if valor_real is not None:
        error_pct = abs(valor_real - prediccion) * 100
        st.write(f"Diferencia frente al valor real introducido: {error_pct:.2f} puntos porcentuales.")

    with st.expander("Lectura automatica de factores compuestos"):
        st.write(
            "La app agrupa los factores introducidos en indicadores mas faciles de leer. "
            "Estos indicadores forman la capa de feature engineering preparada para futuros reentrenamientos."
        )
        feature_labels = {
            "risk_score_sum": "Riesgo acumulado total",
            "risk_score_mean": "Riesgo medio general",
            "water_pressure_risk": "Presion hidrologica",
            "environmental_risk": "Riesgo ambiental",
            "infrastructure_risk": "Riesgo de infraestructura",
            "planning_risk": "Riesgo de planificacion",
            "exposure_risk": "Exposicion y vulnerabilidad",
        }
        engineered_display = pd.DataFrame(
            [
                {"Indicador": feature_labels.get(feature, feature), "Valor": round(value, 2)}
                for feature, value in engineered_summary.items()
            ]
        )
        st.dataframe(engineered_display, width="stretch", hide_index=True)

    timestamp = datetime.now().isoformat(timespec="seconds")
    prediction_id = crear_prediction_id()
    fila_base = {
        "prediction_id": prediction_id,
        "timestamp": timestamp,
        "consultor": nombre_usuario,
        "model_name": MODEL_NAME,
        "model_version": MODEL_VERSION,
        "model_file": MODEL_FILENAME,
        **valores,
        "prediction": prediccion,
        "actual_value": valor_real if valor_real is not None else "",
        "record_status": "validated_for_retraining" if valor_real is not None else "pending_target",
    }
    fila_feedback = fila_base.copy()
    fila_feedback["actual_value"] = valor_real if valor_real is not None else ""
    fila_feedback["error"] = abs(valor_real - prediccion) if valor_real is not None else ""

    guardar_fila_csv(FEEDBACK_PATH, fila_feedback)
    guardar_fila_csv(NEW_DATA_PATH, fila_base)
    db_ok, db_message = guardar_registro_base_datos(fila_feedback)
    if "cargar_feedback" in globals():
        cargar_feedback.clear()
    st.success("Resultado guardado para seguimiento del modelo y futuros reentrenamientos.")
    if db_ok:
        st.caption(db_message)
    else:
        st.warning(db_message)


def mostrar_informes():
    st.header("Informes técnicos del proyecto")
    st.write(
        "Esta vista separa los notebooks de la herramienta de predicción. "
        "Sirve para revisar el trabajo técnico que justifica el modelo."
    )

    notebooks_dir = PROJECT_ROOT / "notebooks"
    nb_files = sorted(list(notebooks_dir.glob("*.ipynb")))
    if not nb_files:
        st.warning("No se encontraron notebooks en la carpeta notebooks/.")
        return

    nb_choice = st.selectbox(
        "Selecciona el informe técnico",
        options=[p.name for p in nb_files],
        key="client_nb_choice",
    )
    titulo, contexto = NOTEBOOK_CONTEXT.get(
        nb_choice,
        ("Notebook técnico", "Documento técnico del proyecto."),
    )

    st.subheader(titulo)
    st.write(contexto)
    st.caption("El contenido siguiente procede del notebook ejecutado por el equipo.")
    st.divider()
    renderizar_notebook_real(notebooks_dir / nb_choice)


@st.cache_data(ttl=5)
def cargar_feedback(path):
    if not path.exists():
        return pd.DataFrame()
    try:
        feedback_df = pd.read_csv(path)
    except (pd.errors.ParserError, pd.errors.EmptyDataError):
        crear_backup_csv(path)
        return pd.DataFrame()
    return normalizar_feedback_df(feedback_df)


def usar_base_datos_persistente():
    return bool(database.get_database_backend(DATABASE_PATH).get("persistent"))


@st.cache_data(ttl=5)
def cargar_feedback_monitorizacion(path):
    if usar_base_datos_persistente():
        return database.load_monitoring_records(DATABASE_PATH)
    return cargar_feedback(path)


def mostrar_monitorizacion():
    st.header("Monitorización del modelo")
    st.write(
        "Esta vista usa el feedback generado por la aplicación para revisar el rendimiento "
        "del modelo cuando existen valores reales introducidos por el usuario."
    )
    st.info(
        "Una predicción solo permite saber qué estimó el modelo. Para medir si acertó, "
        "hay que compararla con un valor real observado. Por eso las métricas solo aparecen "
        "cuando alguna predicción tiene valor real guardado."
    )

    usa_bd_persistente = usar_base_datos_persistente()
    feedback_df = cargar_feedback_monitorizacion(FEEDBACK_PATH)
    if feedback_df.empty:
        backups = [] if usa_bd_persistente else sorted(FEEDBACK_PATH.parent.glob(f"{FEEDBACK_PATH.stem}_backup_*.csv"))
        if backups:
            st.warning(
                "Se detectó un archivo de feedback anterior con formato incompatible o corrupto. "
                f"Se guardó una copia de seguridad como `{backups[-1].name}` y la app generará un CSV limpio."
            )
        st.info(
            "Todavía no hay predicciones guardadas. Realiza predicciones desde la vista "
            "`Predicción` para empezar a generar feedback."
        )
        return

    if usa_bd_persistente:
        st.caption("Monitorizacion cargada desde PostgreSQL persistente.")

    total_predicciones = len(feedback_df)
    feedback_df["actual_value"] = pd.to_numeric(feedback_df.get("actual_value"), errors="coerce")
    feedback_df["prediction"] = pd.to_numeric(feedback_df.get("prediction"), errors="coerce")
    feedback_con_real = feedback_df.dropna(subset=["actual_value", "prediction"]).copy()

    col_total, col_con_real, col_pendientes = st.columns(3)
    col_total.metric("Predicciones guardadas", total_predicciones)
    col_con_real.metric("Con valor real", len(feedback_con_real))
    col_pendientes.metric("Sin valor real", total_predicciones - len(feedback_con_real))

    pendientes_df = feedback_df[
        feedback_df["actual_value"].isna() & feedback_df["prediction"].notna()
    ].copy()

    st.subheader("Completar valor real pendiente")
    st.write(
        "Si una predicción se guardó sin valor real, puedes añadirlo aquí cuando el dato ya esté confirmado. "
        "Al guardarlo, la app recalcula el error y actualiza las métricas de monitorización."
    )

    if pendientes_df.empty:
        st.success("No hay predicciones pendientes de valor real.")
    else:
        pendientes_df = pendientes_df.sort_index(ascending=False)
        opciones_pendientes = pendientes_df["prediction_id"].astype(str).tolist()

        def formatear_prediccion_pendiente(prediction_id):
            fila = pendientes_df[pendientes_df["prediction_id"].astype(str) == str(prediction_id)].iloc[0]
            fecha = fila.get("timestamp", "sin fecha")
            prediccion_pct = float(fila.get("prediction", 0)) * 100
            return f"{fecha} | predicción {prediccion_pct:.2f}% | {prediction_id}"

        with st.form("actualizar_valor_real_form"):
            prediction_id_seleccionado = st.selectbox(
                "Predicción pendiente",
                options=opciones_pendientes,
                format_func=formatear_prediccion_pendiente,
            )
            valor_real_pendiente_pct = st.slider(
                "Valor real observado de inundación (%)",
                min_value=0,
                max_value=100,
                value=50,
                step=1,
                help="Introduce el porcentaje real observado para esta predicción ya guardada.",
            )
            guardar_actualizacion = st.form_submit_button("Guardar valor real en esta predicción")

        if guardar_actualizacion:
            if usa_bd_persistente:
                fila = pendientes_df[
                    pendientes_df["prediction_id"].astype(str) == str(prediction_id_seleccionado)
                ].iloc[0]
                try:
                    database.update_actual_value(
                        DATABASE_PATH,
                        str(prediction_id_seleccionado),
                        valor_real_pendiente_pct / 100,
                        float(fila.get("prediction")),
                    )
                    cargar_feedback_monitorizacion.clear()
                    ok, mensaje = True, "Valor real guardado en PostgreSQL. Las metricas se han actualizado."
                except Exception as exc:
                    ok, mensaje = False, f"No se pudo actualizar PostgreSQL: {exc}"
            else:
                ok, mensaje = actualizar_valor_real_feedback(
                    FEEDBACK_PATH,
                    prediction_id_seleccionado,
                    valor_real_pendiente_pct / 100,
                    NEW_DATA_PATH,
                )
            if ok:
                st.success(mensaje)
                st.rerun()
            else:
                st.error(mensaje)

    st.subheader("Gestionar registros de feedback")
    st.warning(
        "Esta zona modifica el histórico local de feedback. Editar un valor real cambia las métricas. "
        "Eliminar una predicción la quita del feedback y, si existe, también del archivo de nuevos datos "
        "para reentrenamiento."
    )

    gestion_df = feedback_df.sort_index(ascending=False).copy()
    opciones_gestion = gestion_df["prediction_id"].astype(str).tolist()

    def formatear_prediccion_gestion(prediction_id):
        fila = gestion_df[gestion_df["prediction_id"].astype(str) == str(prediction_id)].iloc[0]
        fecha = fila.get("timestamp", "sin fecha")
        prediccion_pct = float(fila.get("prediction", 0)) * 100 if pd.notna(fila.get("prediction")) else 0
        valor_real = fila.get("actual_value")
        valor_real_txt = "sin valor real" if pd.isna(valor_real) else f"real {float(valor_real) * 100:.2f}%"
        return f"{fecha} | predicción {prediccion_pct:.2f}% | {valor_real_txt} | {prediction_id}"

    registro_id = st.selectbox(
        "Selecciona una predicción guardada",
        options=opciones_gestion,
        format_func=formatear_prediccion_gestion,
        key="gestion_prediction_id",
    )
    registro = gestion_df[gestion_df["prediction_id"].astype(str) == str(registro_id)].iloc[0]
    prediccion_registro_pct = float(registro.get("prediction", 0)) * 100 if pd.notna(registro.get("prediction")) else 0
    valor_real_actual = registro.get("actual_value")
    valor_real_actual_pct = 50 if pd.isna(valor_real_actual) else int(round(float(valor_real_actual) * 100))

    col_detalle, col_editar = st.columns([1, 1])
    with col_detalle:
        st.caption("Detalle del registro seleccionado")
        st.write(f"Fecha: {registro.get('timestamp', 'sin fecha')}")
        st.write(f"Predicción del modelo: {prediccion_registro_pct:.2f}%")
        if pd.isna(valor_real_actual):
            st.write("Valor real actual: pendiente")
        else:
            st.write(f"Valor real actual: {float(valor_real_actual) * 100:.2f}%")
        st.write(f"Modelo: {registro.get('model_name', MODEL_NAME)} / {registro.get('model_version', MODEL_VERSION)}")

    with col_editar:
        with st.form("editar_valor_real_form"):
            nuevo_valor_real_pct = st.slider(
                "Nuevo valor real observado (%)",
                min_value=0,
                max_value=100,
                value=valor_real_actual_pct,
                step=1,
                key="editar_valor_real_pct",
            )
            guardar_edicion = st.form_submit_button("Actualizar valor real")

        if guardar_edicion:
            if usa_bd_persistente:
                try:
                    database.update_actual_value(
                        DATABASE_PATH,
                        str(registro_id),
                        nuevo_valor_real_pct / 100,
                        float(registro.get("prediction")),
                    )
                    cargar_feedback_monitorizacion.clear()
                    ok, mensaje = True, "Valor real actualizado en PostgreSQL."
                except Exception as exc:
                    ok, mensaje = False, f"No se pudo actualizar PostgreSQL: {exc}"
            else:
                ok, mensaje = actualizar_valor_real_feedback(
                    FEEDBACK_PATH,
                    registro_id,
                    nuevo_valor_real_pct / 100,
                    NEW_DATA_PATH,
                )
            if ok:
                st.success(mensaje)
                st.rerun()
            else:
                st.error(mensaje)

    with st.expander("Eliminar registro seleccionado"):
        st.error(
            "Eliminar este registro borra la predicción del histórico local de feedback. "
            "También se intentará eliminar su fila asociada en nuevos_registros.csv. "
            "Esto puede cambiar métricas, gráficas y el conjunto disponible para reentrenamiento."
        )
        st.caption("Para confirmar, escribe exactamente ELIMINAR.")
        confirmacion_eliminar = st.text_input(
            "Confirmación de borrado",
            key=f"confirmar_eliminar_{registro_id}",
        )
        if st.button("Eliminar definitivamente este registro", type="primary"):
            if confirmacion_eliminar != "ELIMINAR":
                st.error("No se eliminó nada. Debes escribir ELIMINAR para confirmar.")
            else:
                if usa_bd_persistente:
                    try:
                        database.delete_prediction_record(DATABASE_PATH, str(registro_id))
                        cargar_feedback_monitorizacion.clear()
                        ok, mensaje = True, "Prediccion eliminada de PostgreSQL."
                    except Exception as exc:
                        ok, mensaje = False, f"No se pudo eliminar de PostgreSQL: {exc}"
                else:
                    ok, mensaje = eliminar_prediccion_registrada(FEEDBACK_PATH, NEW_DATA_PATH, registro_id)
                if ok:
                    st.success(mensaje)
                    st.rerun()
                else:
                    st.error(mensaje)

    st.divider()

    if feedback_con_real.empty:
        st.warning(
            "Hay predicciones guardadas, pero ninguna tiene valor real. "
            "Añade el valor real en el bloque anterior o guarda una nueva predicción con valor real "
            "para activar las métricas."
        )
    else:
        y_true = feedback_con_real["actual_value"]
        y_pred = feedback_con_real["prediction"]
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))

        col_mae, col_rmse, col_r2 = st.columns(3)
        col_mae.metric("MAE acumulado", f"{mae:.4f}")
        col_rmse.metric("RMSE acumulado", f"{rmse:.4f}")

        if len(feedback_con_real) >= 2 and y_true.nunique() > 1:
            r2 = r2_score(y_true, y_pred)
            col_r2.metric("R2 acumulado", f"{r2:.4f}")
        else:
            col_r2.metric("R2 acumulado", "N/D")
            st.caption("R2 necesita al menos dos valores reales distintos para ser informativo.")

        feedback_con_real["absolute_error"] = (y_true - y_pred).abs()
        if "timestamp" in feedback_con_real.columns:
            feedback_con_real["timestamp"] = pd.to_datetime(feedback_con_real["timestamp"], errors="coerce")
            serie_error = feedback_con_real.dropna(subset=["timestamp"]).sort_values("timestamp")
            if not serie_error.empty:
                st.subheader("Evolución del error absoluto")
                st.line_chart(serie_error.set_index("timestamp")["absolute_error"])

    st.subheader("Feedback reciente")
    feedback_display = feedback_df.copy()
    for col in ["prediction", "actual_value", "error"]:
        if col in feedback_display.columns:
            feedback_display[col] = pd.to_numeric(feedback_display[col], errors="coerce") * 100

    columnas_mostrar = [
        col
        for col in ["timestamp", "consultor", "model_name", "model_version", "prediction", "actual_value", "error"]
        if col in feedback_display.columns
    ]
    feedback_display = feedback_display[columnas_mostrar].tail(20).rename(
        columns={
            "timestamp": "fecha",
            "consultor": "consultor",
            "model_name": "modelo",
            "model_version": "versión",
            "prediction": "predicción (%)",
            "actual_value": "valor real (%)",
            "error": "error absoluto (%)",
        }
    )
    st.dataframe(feedback_display.fillna(""), width="stretch", hide_index=True)

    with st.expander("Ubicación del archivo de feedback"):
        st.code(str(FEEDBACK_PATH), language="text")


def mostrar_base_datos():
    st.header("Base de datos de la aplicacion")
    st.write(
        "Esta vista comprueba que los datos recogidos por la app tambien se guardan en una base de datos estructurada. "
        "En local usa SQLite; en despliegue puede usar PostgreSQL persistente si existe DATABASE_URL."
    )

    try:
        summary = database.get_database_summary(DATABASE_PATH)
    except Exception as exc:
        st.error(f"No se pudo abrir la base de datos: {exc}")
        return

    col_estado, col_total, col_validados, col_pendientes = st.columns(4)
    estado_bd = "Persistente" if summary.get("persistent") else "Local"
    col_estado.metric("Base de datos", f"{summary.get('engine', 'SQLite')} - {estado_bd}")
    col_total.metric("Predicciones en BD", summary["total_predictions"])
    col_validados.metric("Con valor real", summary["validated_predictions"])
    col_pendientes.metric("Pendientes", summary["pending_predictions"])

    st.info(
        "Cada vez que se calcula una prediccion, la app guarda el identificador, fecha, consultor, "
        "modelo usado, valores introducidos, prediccion, valor real si existe y estado del registro."
    )

    st.subheader("Registros recientes en la base de datos")
    recent_df = database.load_recent_predictions(DATABASE_PATH)
    if recent_df.empty:
        st.warning("Todavia no hay registros en la base de datos. Haz una prediccion para crear el primer registro.")
    else:
        for col in ["prediction", "actual_value", "error"]:
            if col in recent_df.columns:
                recent_df[col] = pd.to_numeric(recent_df[col], errors="coerce") * 100
        st.dataframe(recent_df.fillna(""), width="stretch", hide_index=True)

    with st.expander("Ubicacion y esquema"):
        st.code(str(summary["path"]), language="text")
        st.write(
            "Tabla principal: `app_predictions`. Tabla auxiliar: `app_events`, usada para registrar guardados, "
            "actualizaciones y borrados."
        )


@st.cache_data(ttl=5)
def cargar_nuevos_datos(path):
    if usar_base_datos_persistente():
        return database.load_pipeline_records(DATABASE_PATH)

    if not path.exists():
        return pd.DataFrame()
    try:
        new_data_df = pd.read_csv(path)
    except (pd.errors.ParserError, pd.errors.EmptyDataError):
        crear_backup_csv(path)
        return pd.DataFrame()
    new_data_df = normalizar_nuevos_datos_df(new_data_df)
    return new_data_df[new_data_df["record_status"].astype(str) != "ingested_for_retraining"].copy()


def marcar_registros_ingeridos(path, prediction_ids):
    prediction_ids = [str(prediction_id) for prediction_id in prediction_ids if str(prediction_id).strip()]
    if not prediction_ids:
        return 0

    if usar_base_datos_persistente():
        updated = database.mark_predictions_ingested(DATABASE_PATH, prediction_ids)
        cargar_nuevos_datos.clear()
        cargar_feedback_monitorizacion.clear()
        return updated

    if not path.exists():
        return 0

    try:
        new_data_df = pd.read_csv(path)
    except (pd.errors.ParserError, pd.errors.EmptyDataError):
        crear_backup_csv(path)
        return 0

    new_data_df = normalizar_nuevos_datos_df(new_data_df)
    mask = new_data_df["prediction_id"].astype(str).isin(prediction_ids)
    updated = int(mask.sum())
    if updated:
        new_data_df.loc[mask, "record_status"] = "ingested_for_retraining"
        new_data_df.to_csv(path, index=False)
        cargar_nuevos_datos.clear()
    return updated


def construir_dataset_reentrenamiento(new_data_df):
    return build_retraining_dataset(new_data_df, FEATURE_COLUMNS)


def guardar_dataset_reentrenamiento(retraining_df, path):
    if retraining_df.empty:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        try:
            existing_df = pd.read_csv(path)
        except (pd.errors.ParserError, pd.errors.EmptyDataError):
            crear_backup_csv(path)
            existing_df = pd.DataFrame()
        if not existing_df.empty:
            retraining_df = pd.concat([existing_df, retraining_df], ignore_index=True)
            retraining_df = retraining_df.drop_duplicates(ignore_index=True)
    retraining_df.to_csv(path, index=False)
    return True


def mostrar_descarga_dataset_procesado():
    if not RETRAINING_DATASET_PATH.exists():
        return
    try:
        processed_df = pd.read_csv(RETRAINING_DATASET_PATH)
    except (pd.errors.ParserError, pd.errors.EmptyDataError):
        return
    if processed_df.empty:
        return

    st.subheader("Ultimo dataset preparado")
    st.caption(
        f"Dataset acumulado disponible con {len(processed_df)} registros preparados para reentrenamiento."
    )
    st.download_button(
        "Descargar ultimo dataset validado",
        data=processed_df.to_csv(index=False).encode("utf-8"),
        file_name="retraining_dataset.csv",
        mime="text/csv",
    )


@st.cache_data(show_spinner=False)
def generar_explorador_visual_html(df):
    return pyg.to_html(df, appearance="dark", theme_key="g2", default_tab="vis")


def mostrar_pipeline_reentrenamiento():
    st.header("Pipeline de ingestión para reentrenamiento")
    pipeline_message = st.session_state.pop("pipeline_ingestion_message", None)
    if pipeline_message:
        st.success(pipeline_message)

    st.write(
        "Esta vista prepara los datos nuevos recogidos por la aplicación para futuros reentrenamientos. "
        "Solo los registros con valor real observado pueden usarse como datos supervisados."
    )
    st.info(
        "La predicción del modelo sirve como referencia, pero no debe usarse como variable objetivo para reentrenar. "
        "Para reentrenamiento se usa el valor real observado como `FloodProbability`."
    )

    st.caption(
        "El archivo generado incluye las variables originales y una capa de feature engineering "
        "con indicadores compuestos de riesgo ambiental, infraestructura, planificacion y exposicion."
    )

    st.markdown(
        """
        <div class="app-flow">
            <div><strong>1. Se calcula</strong><span>La app guarda una prediccion nueva.</span></div>
            <div><strong>2. Se confirma</strong><span>Se anade el valor real observado.</span></div>
            <div><strong>3. Se activa</strong><span>El boton de ingesta queda disponible.</span></div>
            <div><strong>4. Se prepara</strong><span>Se crea el dataset para reentrenar.</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    new_data_df = cargar_nuevos_datos(NEW_DATA_PATH)
    if new_data_df.empty:
        st.warning(
            "No hay registros pendientes de ingesta. Genera predicciones nuevas o revisa el ultimo dataset preparado."
        )
        mostrar_descarga_dataset_procesado()
        st.subheader("Accion del pipeline")
        st.button("Ejecutar pipeline de ingesta", type="primary", disabled=True)
        st.caption(
            "El boton se activara cuando exista al menos una prediccion guardada con valor real observado."
        )
        return

    total_registros = len(new_data_df)
    registros_validados = new_data_df.dropna(subset=["actual_value"]).copy()
    registros_pendientes = total_registros - len(registros_validados)

    col_total, col_validos, col_pendientes = st.columns(3)
    col_total.metric("Registros nuevos", total_registros)
    col_validos.metric("Listos para reentrenar", len(registros_validados))
    col_pendientes.metric("Pendientes de valor real", registros_pendientes)

    st.subheader("Estado del pipeline")
    st.caption(
        "Al ejecutar el pipeline de ingesta, la app prepara automaticamente los casos que ya tienen "
        "valor real confirmado y los deja listos para usarlos en un futuro reentrenamiento."
    )

    if registros_validados.empty:
        st.warning(
            "Hay registros nuevos, pero ninguno tiene valor real. Completa valores reales en Monitorización "
            "para poder generar un dataset supervisado."
        )
        st.subheader("Accion del pipeline")
        st.button("Ejecutar pipeline de ingesta", type="primary", disabled=True)
        st.caption(
            "Ahora mismo el pipeline esta esperando el valor real. Cuando lo anadas en Monitorizacion, "
            "este boton pasara a estar disponible."
        )
    else:
        retraining_df = construir_dataset_reentrenamiento(new_data_df)
        st.success(
            f"Hay {len(retraining_df)} registros validados que pueden incorporarse a futuros reentrenamientos."
        )

        preview_df = retraining_df.tail(20).copy()
        st.dataframe(preview_df, width="stretch", hide_index=True)

        col_guardar, col_descargar = st.columns([1, 1])
        with col_guardar:
            st.subheader("Accion del pipeline")
            if st.button("Ejecutar pipeline de ingesta", type="primary"):
                if guardar_dataset_reentrenamiento(retraining_df, RETRAINING_DATASET_PATH):
                    prediction_ids = (
                        registros_validados["prediction_id"].dropna().astype(str).tolist()
                        if "prediction_id" in registros_validados.columns
                        else []
                    )
                    registros_marcados = marcar_registros_ingeridos(NEW_DATA_PATH, prediction_ids)
                    if registros_marcados:
                        st.session_state["pipeline_ingestion_message"] = (
                            f"{registros_marcados} registros han salido de la cola de ingesta "
                            "para no volver a procesarse en la siguiente ejecucion."
                        )
                    else:
                        st.session_state["pipeline_ingestion_message"] = "Pipeline de ingesta ejecutado correctamente."
                    st.rerun()
                else:
                    st.error("No se pudo ejecutar el pipeline de ingesta.")

        with col_descargar:
            csv_bytes = retraining_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Descargar dataset validado",
                data=csv_bytes,
                file_name="retraining_dataset.csv",
                mime="text/csv",
            )

    st.subheader("Registros recientes recogidos por la app")
    display_cols = [
        col
        for col in [
            "timestamp",
            "consultor",
            "model_name",
            "model_version",
            "prediction",
            "actual_value",
            "record_status",
        ]
        if col in new_data_df.columns
    ]
    display_df = new_data_df[display_cols].tail(20).copy()
    for col in ["prediction", "actual_value"]:
        if col in display_df.columns:
            display_df[col] = pd.to_numeric(display_df[col], errors="coerce") * 100
    st.dataframe(display_df.fillna(""), width="stretch", hide_index=True)

    with st.expander("Archivos del pipeline"):
        st.code(str(NEW_DATA_PATH), language="text")
        st.code(str(RETRAINING_DATASET_PATH), language="text")


def mostrar_datos(num_rows):
    st.header("Datos y exploración")
    st.write(
        "Esta vista permite revisar una muestra del dataset usado por el proyecto. "
        "No es necesaria para usar el predictor, pero ayuda a entender la base de datos."
    )

    if not DATA_PATH.exists():
        st.warning(
            "No se encontro el CSV original del dataset en este entorno. "
            "Se muestra una muestra de demostracion con la misma estructura para mantener activa la vista."
        )
        st.caption(f"Ruta esperada del dataset real: {DATA_PATH}")
        df_preview = crear_muestra_demo_dataset(num_rows)
    else:
        df_preview = cargar_preview(DATA_PATH, num_rows)
    tab1, tab2 = st.tabs(["Tabla de datos", "Explorador visual"])

    with tab1:
        st.write(f"Mostrando las primeras {num_rows} filas del dataset:")
        st.dataframe(df_preview, width="stretch")

    with tab2:
        st.subheader("Explorador visual del dataset")
        st.write(
            "Esta vista permite analizar el dataset sin escribir codigo: seleccionar columnas, cruzar variables "
            "y crear graficos rapidos para entender patrones antes o despues del modelado."
        )
        mostrar_tarjeta(
            "Para que sirve",
            "Ayuda a reforzar el EDA desde la propia aplicacion: distribuciones, relaciones entre variables, "
            "posibles correlaciones y comparaciones visuales de la variable objetivo.",
            color="#E0F2FE",
            borde="#0891B2",
        )

        if pyg is None:
            st.info(
                "La dependencia del explorador visual no esta instalada en este entorno. No afecta al predictor, la monitorizacion, "
                "la base de datos ni el pipeline de ingesta."
            )
            st.write(
                "Esta pestaña serviria para explorar el dataset de forma visual, creando graficos rapidos "
                "a partir de las columnas. La tabla de datos sigue estando disponible en la pestaña anterior."
            )
            with st.expander("Instalacion para activar el explorador visual"):
                st.code("pip install pygwalker", language="bash")
        else:
            import streamlit.components.v1 as components

            with st.spinner("Preparando explorador visual..."):
                try:
                    pyg_html = generar_explorador_visual_html(df_preview)
                    components.html(pyg_html, height=820, scrolling=True)
                except Exception as exc:
                    st.error("No se pudo cargar el explorador visual en esta sesion.")
                    st.caption(f"Detalle tecnico: {exc}")


def main():
    st.set_page_config(page_title="Análisis de Inundaciones", layout="wide")
    aplicar_estilo_visual()

    st.sidebar.header("Panel de control")
    nombre_usuario = st.sidebar.text_input("Consultor a cargo:", value="Estudiante")
    vista = st.sidebar.radio(
        "Vista",
        [
            "Guía del proyecto",
            "Predicción",
            "Monitorización",
            "Base de datos",
            "Pipeline de reentrenamiento",
            "Informes técnicos",
            "Datos",
        ],
    )

    num_rows = st.sidebar.slider(
        "Filas a cargar en la vista de datos:",
        min_value=5,
        max_value=1000,
        value=50,
        step=5,
    )

    modo_vista = st.sidebar.selectbox(
        "Modo de visualización:",
        options=["Estándar", "Texto grande", "Alto contraste"],
    )
    aplicar_accesibilidad(modo_vista)

    mostrar_cabecera(nombre_usuario)

    if vista in ["Guía de uso", "Guía del proyecto"]:
        mostrar_guia_uso()
    elif vista == "Predicción":
        mostrar_prediccion(nombre_usuario)
    elif vista == "Monitorización":
        mostrar_monitorizacion()
    elif vista == "Base de datos":
        mostrar_base_datos()
    elif vista == "Pipeline de reentrenamiento":
        mostrar_pipeline_reentrenamiento()
    elif vista == "Informes técnicos":
        mostrar_informes()
    else:
        mostrar_datos(num_rows)


if __name__ == "__main__":
    main()


