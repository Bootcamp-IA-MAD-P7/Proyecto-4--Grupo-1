# Checklist Nivel Esencial

![Estado](https://img.shields.io/badge/Estado-Hecho-1A7F37?style=for-the-badge)
![Modelo](https://img.shields.io/badge/Modelo-Hecho-1A7F37?style=for-the-badge)
![EDA](https://img.shields.io/badge/EDA-Hecho-1A7F37?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-Hecho-1A7F37?style=for-the-badge)

Este documento resume el estado del Nivel Esencial del proyecto.

## Resumen de estado

| Requisito | Estado | Evidencia |
|---|---|---|
| Modelo funcional | Hecho | `notebooks/02_modeling.ipynb` |
| EDA con visualizaciones | Hecho | `notebooks/01_EDA.ipynb` |
| Overfitting inferior al 5% | Hecho | Diferencia R2: 0.077% |
| Solucion productivizada | Hecho | `app/app.py` |
| Informe de rendimiento | Hecho | Metricas, residuos e interpretacion en `notebooks/02_modeling.ipynb` |

## 1. Modelo de ML funcional

**Objetivo:** entrenar al menos un modelo capaz de predecir una variable numerica.

**Estado:** Hecho

Evidencia:

- Notebook: `notebooks/02_modeling.ipynb`
- Variable objetivo: `FloodProbability`
- Mejor modelo baseline: `Linear Regression`
- Modelo usado por la app: `models/flood_baseline_model.joblib`

## 2. Analisis exploratorio de datos

**Objetivo:** analizar los datos con visualizaciones relevantes para regresion.

**Estado:** Hecho

Evidencia:

- Notebook: `notebooks/01_EDA.ipynb`

El EDA revisa estructura del dataset, variable objetivo, correlaciones y visualizaciones relevantes para regresion.

## 3. Overfitting inferior al 5%

**Objetivo:** comprobar que la diferencia entre entrenamiento y validacion es aceptable.

**Estado:** Hecho

| Modelo | R2 Train | R2 Validation | Diferencia | Estado |
|---|---:|---:|---:|---|
| Linear Regression | 0.8455 | 0.8449 | 0.077% | Cumple |

Metricas usadas:

- RMSE
- MAE
- R2

## 4. Solucion productivizada

**Objetivo:** crear una aplicacion para usar el modelo fuera del notebook.

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

**Objetivo:** explicar como funciona el modelo y evaluar su rendimiento.

**Estado:** Hecho

Evidencia:

- Notebook: `notebooks/02_modeling.ipynb`
- Metricas calculadas: RMSE, MAE y R2.
- Comparacion train/test.
- Prediccion vs valor real.
- Analisis de residuos.
- Interpretacion mediante coeficientes del modelo lineal.

| Modelo | RMSE Validation | MAE Validation | R2 Validation | Overfitting R2 |
|---|---:|---:|---:|---:|
| Linear Regression | 0.0201 | 0.0158 | 0.8449 | 0.077% |

## Relacion con Nivel Medio

La app ya incluye dos bases utiles para el Nivel Medio:

- Sistema de feedback en `data/feedback/predicciones.csv`.
- Sistema de recogida de nuevos datos en `data/new_data/nuevos_registros.csv`.

Estos archivos son locales y estan ignorados por Git.

Quedan pendientes para completar Nivel Medio:

- Modelos ensemble.
- Validacion cruzada.
- Optimizacion de hiperparametros.
