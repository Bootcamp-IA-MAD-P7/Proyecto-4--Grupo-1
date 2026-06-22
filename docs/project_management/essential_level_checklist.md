# Checklist Nivel Esencial

Este documento resume el estado del Nivel Esencial del proyecto.

## Resumen de estado

| Requisito | Estado | Evidencia |
|---|---|---|
| Modelo funcional | Hecho | `notebooks/02_modeling.ipynb` |
| EDA con visualizaciones | Hecho | `notebooks/01_EDA.ipynb` |
| Overfitting inferior al 5% | Hecho | Comparacion train/validacion en `notebooks/02_modeling.ipynb` |
| Solucion productivizada | Hecho | `app/app.py` |
| Informe de rendimiento | Hecho | Metricas y explicacion en `notebooks/02_modeling.ipynb` |

## 1. Modelo de ML funcional

**Estado:** Hecho

El proyecto cuenta con un modelo baseline de regresion para predecir `FloodProbability`.

Evidencia:

- Notebook: `notebooks/02_modeling.ipynb`
- Modelo usado por la app: `models/flood_baseline_model.joblib`

## 2. Analisis exploratorio de datos

**Estado:** Hecho

El EDA revisa estructura del dataset, variable objetivo, correlaciones y visualizaciones relevantes para regresion.

Evidencia:

- Notebook: `notebooks/01_EDA.ipynb`

## 3. Control de overfitting

**Estado:** Hecho

El notebook de modelado compara resultados de entrenamiento y validacion para controlar que la diferencia sea aceptable.

Metricas usadas:

- RMSE
- MAE
- R2

## 4. Solucion productivizada

**Estado:** Hecho

La aplicacion Streamlit permite usar el modelo fuera del notebook.

Funcionalidades actuales:

- Carga automatica del modelo entrenado.
- Entrada guiada de variables predictoras.
- Ayudas por variable para usuarios no tecnicos.
- Boton para restablecer valores recomendados.
- Resultado expresado como porcentaje de riesgo estimado de inundacion.
- Aviso cuando el modelo extrapola fuera del rango esperado.
- Guardado local de feedback y nuevos registros.
- Vistas separadas para prediccion, informes tecnicos y datos.

Evidencia:

- Archivo principal: `app/app.py`

## 5. Informe del rendimiento del modelo

**Estado:** Hecho

El rendimiento se documenta en el notebook de modelado con metricas de regresion y explicacion del comportamiento del modelo.

Evidencia:

- Notebook: `notebooks/02_modeling.ipynb`

## Relacion con Nivel Medio

La app ya incluye dos bases utiles para el Nivel Medio:

- Sistema de feedback en `data/feedback/predicciones.csv`.
- Sistema de recogida de nuevos datos en `data/new_data/nuevos_registros.csv`.

Estos archivos son locales y estan ignorados por Git.
