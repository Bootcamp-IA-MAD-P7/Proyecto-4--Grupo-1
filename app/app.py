from datetime import datetime
from pathlib import Path
import base64
import csv
import shutil

import joblib
import nbformat
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from paths import get_data_path

try:
    import pygwalker as pyg
except ModuleNotFoundError:
    pyg = None


BASE = Path(__file__).parent
PROJECT_ROOT = BASE.parent
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
    "DamsQuality": ("Calidad de presas", "Estado de presas e infraestructuras de contencion."),
    "Siltation": ("Sedimentación", "Acumulación de sedimentos en cauces o sistemas de agua."),
    "AgriculturalPractices": ("Prácticas agrícolas", "Impacto de prácticas agrícolas sobre el terreno."),
    "Encroachments": ("Ocupación de zonas de riesgo", "Construcciones o usos en zonas inundables."),
    "IneffectiveDisasterPreparedness": ("Preparación ante desastres", "Falta de preparación frente a emergencias."),
    "DrainageSystems": ("Sistemas de drenaje", "Estado de alcantarillado y drenaje urbano."),
    "CoastalVulnerability": ("Vulnerabilidad costera", "Exposición a marejadas o subida del nivel del mar."),
    "Landslides": ("Deslizamientos de tierra", "Riesgo de deslizamientos que agraven inundaciones."),
    "Watersheds": ("Cuencas hidrograficas", "Condicion de las cuencas que recogen el agua de lluvia."),
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
    "Urbanization": "Bajo: zona rural. Medio: area semiurbana. Alto: ciudad densa con suelo impermeable.",
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
        ">
            <strong>{titulo}</strong>
            <p style="margin:0.35rem 0 0 0;">{texto}</p>
        </div>
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


def actualizar_valor_real_feedback(path, prediction_id, valor_real):
    if not path.exists():
        return False, "No existe el archivo de feedback."

    try:
        feedback_df = pd.read_csv(path)
    except (pd.errors.ParserError, pd.errors.EmptyDataError):
        backup_path = crear_backup_csv(path)
        return False, f"El archivo de feedback tenia formato incorrecto. Se guardo backup: {backup_path.name}."

    feedback_df = normalizar_feedback_df(feedback_df)
    feedback_df["prediction"] = pd.to_numeric(feedback_df.get("prediction"), errors="coerce")
    mask = feedback_df["prediction_id"].astype(str) == str(prediction_id)

    if not mask.any():
        return False, "No se encontro la prediccion seleccionada."

    prediction = feedback_df.loc[mask, "prediction"].iloc[0]
    if pd.isna(prediction):
        return False, "La prediccion seleccionada no tiene un valor numerico valido."

    feedback_df.loc[mask, "actual_value"] = valor_real
    feedback_df.loc[mask, "error"] = abs(float(valor_real) - float(prediction))
    path.parent.mkdir(parents=True, exist_ok=True)
    feedback_df.to_csv(path, index=False)
    cargar_feedback.clear()
    return True, "Valor real guardado. Las metricas se han actualizado."


def eliminar_prediccion_registrada(feedback_path, new_data_path, prediction_id):
    if not feedback_path.exists():
        return False, "No existe el archivo de feedback."

    try:
        feedback_df = pd.read_csv(feedback_path)
    except (pd.errors.ParserError, pd.errors.EmptyDataError):
        backup_path = crear_backup_csv(feedback_path)
        return False, f"El archivo de feedback tenia formato incorrecto. Se guardo backup: {backup_path.name}."

    feedback_df = normalizar_feedback_df(feedback_df)
    mask_feedback = feedback_df["prediction_id"].astype(str) == str(prediction_id)
    if not mask_feedback.any():
        return False, "No se encontro la prediccion seleccionada en feedback."

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

    cargar_feedback.clear()
    backups = [backup.name for backup in [backup_feedback, backup_new_data] if backup is not None]
    detalle_backup = f" Copia de seguridad: {', '.join(backups)}." if backups else ""
    return True, f"Prediccion eliminada del historico local.{detalle_backup}"


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
                        st.text(reparar_texto(output.text))
                    elif output.output_type in ("execute_result", "display_data"):
                        if "text/html" in output.data:
                            st.markdown(reparar_texto(output.data["text/html"]), unsafe_allow_html=True)
                        elif "text/plain" in output.data:
                            st.text(reparar_texto(output.data["text/plain"]))
                        if "image/png" in output.data:
                            st.image(base64.b64decode(output.data["image/png"]))
    except Exception as e:
        st.error(f"No se pudieron extraer algunos elementos del notebook: {e}")


def mostrar_guia_uso():
    st.header("Guía de uso de la aplicación")
    st.write(
        "Esta guía explica cómo usar el predictor, cuándo guardar el valor real "
        "y cómo interpretar la monitorización del modelo."
    )

    mostrar_tarjeta(
        "1. Predicción",
        "Usa la vista Predicción para introducir las condiciones de una zona. "
        "La app devuelve una probabilidad estimada de inundación en porcentaje.",
        color="#EFF6FF",
        borde="#2563EB",
    )
    mostrar_tarjeta(
        "2. Valor real observado",
        "Marca la casilla de valor real solo cuando conozcas el dato real o confirmado. "
        "Por ejemplo, si después se observa que el valor real fue 55%, introdúcelo para comparar.",
        color="#F0FDF4",
        borde="#16A34A",
    )
    mostrar_tarjeta(
        "3. Monitorización",
        "La vista Monitorización compara predicciones con valores reales. "
        "Sin valores reales, la app guarda predicciones, pero no puede calcular errores.",
        color="#FFFBEB",
        borde="#D97706",
    )
    mostrar_tarjeta(
        "4. Datos para reentrenamiento",
        "Cada predicción guarda los valores introducidos. Esto permite construir un histórico "
        "para futuros reentrenamientos del modelo.",
        color="#F5F3FF",
        borde="#7C3AED",
    )

    tab_pred, tab_real, tab_monitor, tab_archivos = st.tabs(
        ["Cómo predecir", "Cuándo guardar valor real", "Cómo leer monitorización", "Qué se guarda"]
    )

    with tab_pred:
        st.subheader("Cómo hacer una predicción")
        st.markdown(
            """
            1. Entra en la vista **Predicción**.
            2. Revisa los controles de cada factor.
            3. Si no conoces un factor, deja el valor recomendado.
            4. Pulsa **Calcular riesgo de inundación**.
            5. La app mostrará una probabilidad estimada, por ejemplo `51.14%`.

            Ese porcentaje es una estimación estadística del modelo, no una alerta oficial.
            """
        )

    with tab_real:
        st.subheader("Qué significa el valor real")
        st.markdown(
            """
            El **valor real** es el dato observado o confirmado después de hacer una predicción.

            Ejemplo:

            - El modelo predice `51%`.
            - Más tarde se confirma que el valor real fue `55%`.
            - La app calcula un error de `4 puntos porcentuales`.

            Marca **Guardar también el valor real observado** solo si tienes ese dato real.
            Si no lo conoces, deja la casilla sin marcar.
            """
        )

    with tab_monitor:
        st.subheader("Cómo interpretar la monitorización")
        st.markdown(
            """
            La vista **Monitorización** muestra:

            - **Predicciones guardadas:** total de usos registrados.
            - **Con valor real:** predicciones que sí pueden compararse contra la realidad.
            - **Sin valor real:** predicciones pendientes de comprobar.
            - **MAE / RMSE:** error acumulado cuando hay valores reales.
            - **R2:** calidad global de ajuste, solo si hay suficientes valores reales.

            Si no hay valores reales, la monitorización puede contar predicciones, pero no medir performance.
            """
        )

    with tab_archivos:
        st.subheader("Qué archivos genera la app")
        st.markdown(
            """
            La aplicación guarda datos locales en dos archivos:

            ```text
            data/feedback/predicciones.csv
            data/new_data/nuevos_registros.csv
            ```

            `predicciones.csv` sirve para monitorizar errores y rendimiento.

            `nuevos_registros.csv` sirve como base para futuros reentrenamientos.

            Estos archivos son locales y están ignorados por Git, por lo que no se suben al repositorio.
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
            st.dataframe(guia, use_container_width=True, hide_index=True)

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
    }
    fila_feedback = fila_base.copy()
    fila_feedback["actual_value"] = valor_real if valor_real is not None else ""
    fila_feedback["error"] = abs(valor_real - prediccion) if valor_real is not None else ""

    guardar_fila_csv(FEEDBACK_PATH, fila_feedback)
    guardar_fila_csv(NEW_DATA_PATH, fila_base)
    if "cargar_feedback" in globals():
        cargar_feedback.clear()
    st.success("Resultado guardado para seguimiento del modelo y futuros reentrenamientos.")


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

    feedback_df = cargar_feedback(FEEDBACK_PATH)
    if feedback_df.empty:
        backups = sorted(FEEDBACK_PATH.parent.glob(f"{FEEDBACK_PATH.stem}_backup_*.csv"))
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
            ok, mensaje = actualizar_valor_real_feedback(
                FEEDBACK_PATH,
                prediction_id_seleccionado,
                valor_real_pendiente_pct / 100,
            )
            if ok:
                st.success(mensaje)
                st.rerun()
            else:
                st.error(mensaje)

    st.subheader("Gestionar registros de feedback")
    st.warning(
        "Esta zona modifica el historico local de feedback. Editar un valor real cambia las metricas. "
        "Eliminar una prediccion la quita del feedback y, si existe, tambien del archivo de nuevos datos "
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
        return f"{fecha} | prediccion {prediccion_pct:.2f}% | {valor_real_txt} | {prediction_id}"

    registro_id = st.selectbox(
        "Selecciona una prediccion guardada",
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
        st.write(f"Prediccion del modelo: {prediccion_registro_pct:.2f}%")
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
            ok, mensaje = actualizar_valor_real_feedback(
                FEEDBACK_PATH,
                registro_id,
                nuevo_valor_real_pct / 100,
            )
            if ok:
                st.success(mensaje)
                st.rerun()
            else:
                st.error(mensaje)

    with st.expander("Eliminar registro seleccionado"):
        st.error(
            "Eliminar este registro borra la prediccion del historico local de feedback. "
            "Tambien se intentara eliminar su fila asociada en nuevos_registros.csv. "
            "Esto puede cambiar metricas, graficas y el conjunto disponible para reentrenamiento."
        )
        st.caption("Para confirmar, escribe exactamente ELIMINAR.")
        confirmacion_eliminar = st.text_input(
            "Confirmacion de borrado",
            key=f"confirmar_eliminar_{registro_id}",
        )
        if st.button("Eliminar definitivamente este registro", type="primary"):
            if confirmacion_eliminar != "ELIMINAR":
                st.error("No se elimino nada. Debes escribir ELIMINAR para confirmar.")
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
    st.dataframe(feedback_display.fillna(""), use_container_width=True, hide_index=True)

    with st.expander("Ubicacion del archivo de feedback"):
        st.code(str(FEEDBACK_PATH), language="text")


def mostrar_datos(num_rows):
    st.header("Datos y exploración")
    st.write(
        "Esta vista permite revisar una muestra del dataset usado por el proyecto. "
        "No es necesaria para usar el predictor, pero ayuda a entender la base de datos."
    )

    if not DATA_PATH.exists():
        st.error(f"No se encontró el archivo de datos en: {DATA_PATH}")
        return

    df_preview = cargar_preview(DATA_PATH, num_rows)
    tab1, tab2 = st.tabs(["Tabla de datos", "Explorador interactivo"])

    with tab1:
        st.write(f"Mostrando las primeras {num_rows} filas del dataset:")
        st.dataframe(df_preview, use_container_width=True)

    with tab2:
        if pyg is None:
            st.warning("PyGWalker no está instalado. La app puede seguir funcionando sin esta vista.")
            st.code("pip install pygwalker", language="bash")
        else:
            import streamlit.components.v1 as components

            pyg_html = pyg.walk(df_preview, output_type="html")
            components.html(pyg_html, height=800, scrolling=True)


st.set_page_config(page_title="Análisis de Inundaciones", layout="wide")

st.sidebar.header("Panel de control")
nombre_usuario = st.sidebar.text_input("Consultor a cargo:", value="Estudiante")
vista = st.sidebar.radio(
    "Vista",
    ["Guía de uso", "Predicción", "Monitorización", "Informes técnicos", "Datos"],
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

st.title("Dashboard de Consultoría: Análisis de Inundaciones")
st.caption(f"Presentación de resultados del Grupo 1. Consultor activo: {nombre_usuario}")

if vista == "Guía de uso":
    mostrar_guia_uso()
elif vista == "Predicción":
    mostrar_prediccion(nombre_usuario)
elif vista == "Monitorización":
    mostrar_monitorizacion()
elif vista == "Informes técnicos":
    mostrar_informes()
else:
    mostrar_datos(num_rows)
