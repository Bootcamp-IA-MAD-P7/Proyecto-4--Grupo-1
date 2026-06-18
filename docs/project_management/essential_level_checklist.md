# Checklist Nivel Esencial

![Estado](https://img.shields.io/badge/Estado-Casi%20completo-9A6700?style=for-the-badge)
![Modelo](https://img.shields.io/badge/Modelo-Hecho-1A7F37?style=for-the-badge)
![EDA](https://img.shields.io/badge/EDA-Hecho-1A7F37?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-Pendiente-9A6700?style=for-the-badge)

Este documento resume los requisitos mínimos que debe cumplir el proyecto para alcanzar el Nivel Esencial y el estado actual de cada punto.

## Resumen de estado

| Requisito | Estado | Evidencia |
|---|---|---|
| Modelo funcional | ![Hecho](https://img.shields.io/badge/Hecho-1A7F37?style=flat-square) | `notebooks/02_modeling.ipynb` |
| EDA con visualizaciones | ![Hecho](https://img.shields.io/badge/Hecho-1A7F37?style=flat-square) | `notebooks/01_EDA.ipynb` |
| Overfitting inferior al 5% | ![Hecho](https://img.shields.io/badge/Hecho-1A7F37?style=flat-square) | Diferencia R2: 0.077% |
| App productivizada | ![Pendiente](https://img.shields.io/badge/Pendiente-9A6700?style=flat-square) | `app/app.py` |
| Informe de rendimiento | ![Hecho](https://img.shields.io/badge/Hecho-1A7F37?style=flat-square) | Métricas, residuos e interpretación |

## 1. Modelo de ML funcional

**Objetivo:** entrenar al menos un modelo capaz de predecir una variable numérica.

**Estado:** ![Hecho](https://img.shields.io/badge/Hecho-1A7F37?style=flat-square)

**Evidencia:**

- Notebook: `notebooks/02_modeling.ipynb`
- Variable objetivo: `FloodProbability`
- Mejor modelo baseline: `Linear Regression`

**Checklist:**

- Separar variables predictoras `X` y variable objetivo `y`.
- Eliminar columnas no predictivas como `id`.
- Crear conjunto de entrenamiento y validación.
- Entrenar modelos baseline.
- Generar predicciones.
- Calcular métricas de regresión.

## 2. Análisis exploratorio de datos

**Objetivo:** analizar los datos con visualizaciones relevantes para regresión.

**Estado:** ![Hecho](https://img.shields.io/badge/Hecho-1A7F37?style=flat-square)

**Evidencia:**

- Notebook: `notebooks/01_EDA.ipynb`

**Checklist:**

- Carga y revisión inicial del dataset.
- Revisión de dimensiones, tipos de datos, nulos y duplicados.
- Distribución de la variable objetivo `FloodProbability`.
- Matriz de correlación.
- Correlaciones con la variable objetivo.
- Scatter plots entre variables relevantes y target.
- Histogramas de variables predictoras.
- Boxplots para revisar dispersión y posibles outliers.
- Conclusiones escritas del EDA.

## 3. Overfitting inferior al 5%

**Objetivo:** comprobar que la diferencia entre entrenamiento y validación es aceptable.

**Estado:** ![Hecho](https://img.shields.io/badge/Hecho-1A7F37?style=flat-square)

| Modelo | R2 Train | R2 Validation | Diferencia | Estado |
|---|---:|---:|---:|---|
| Linear Regression | 0.8455 | 0.8449 | 0.077% | Cumple |

**Checklist:**

- Calcular métricas en entrenamiento.
- Calcular métricas en validación.
- Comparar resultados de train y validation.
- Calcular diferencia porcentual.
- Verificar que la diferencia es inferior al 5%.

## 4. Solución productivizada

**Objetivo:** crear una aplicación para usar el modelo fuera del notebook.

**Estado:** ![Pendiente](https://img.shields.io/badge/Pendiente-9A6700?style=flat-square)

**Checklist:**

- Guardar el modelo entrenado.
- Crear aplicación con Streamlit, Gradio, Dash o API.
- Cargar el modelo desde la app.
- Permitir introducir valores de entrada.
- Mostrar la predicción de `FloodProbability`.
- Documentar cómo ejecutar la aplicación.

**Próximo paso:**

```text
Crear app/app.py con Streamlit.
```

## 5. Informe del rendimiento del modelo

**Objetivo:** explicar cómo funciona el modelo y evaluar su rendimiento.

**Estado:** ![Hecho](https://img.shields.io/badge/Hecho-1A7F37?style=flat-square)

**Evidencia:**

- Notebook: `notebooks/02_modeling.ipynb`
- Métricas calculadas: RMSE, MAE y R2.
- Comparación train/test.
- Predicción vs valor real.
- Análisis de residuos.
- Interpretación mediante coeficientes del modelo lineal.

| Modelo | RMSE Validation | MAE Validation | R2 Validation | Overfitting R2 |
|---|---:|---:|---:|---:|
| Linear Regression | 0.0201 | 0.0158 | 0.8449 | 0.077% |

## Próximo paso recomendado

El único requisito pendiente del Nivel Esencial es la productivización del modelo.

La aplicación deberá cargar el modelo guardado, permitir introducir valores para las variables predictoras y mostrar la predicción de `FloodProbability`.
