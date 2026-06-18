# Checklist Nivel Esencial

Este documento resume los requisitos mínimos que debe cumplir el proyecto para alcanzar el Nivel Esencial y el estado actual de cada punto.

## 1. Modelo de ML funcional

**Objetivo:** entrenar al menos un modelo capaz de predecir una variable numérica.

Estado:

```text
Hecho
```

Evidencia:

- Notebook: `notebooks/02_modeling.ipynb`
- Variable objetivo: `FloodProbability`
- Mejor modelo baseline: `Linear Regression`

Checklist:

- Separar variables predictoras `X` y variable objetivo `y`.
- Eliminar columnas no predictivas como `id`.
- Crear conjunto de entrenamiento y validación.
- Entrenar modelos baseline.
- Generar predicciones.
- Calcular métricas de regresión.

## 2. Análisis exploratorio de datos

**Objetivo:** analizar los datos con visualizaciones relevantes para regresión.

Estado:

```text
Hecho
```

Evidencia:

- Notebook: `notebooks/01_EDA.ipynb`

Checklist:

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

Estado:

```text
Hecho
```

Evidencia:

| Modelo | R2 Train | R2 Validation | Diferencia | Estado |
|---|---:|---:|---:|---|
| Linear Regression | 0.8455 | 0.8449 | 0.077% | Cumple |

Checklist:

- Calcular métricas en entrenamiento.
- Calcular métricas en validación.
- Comparar resultados de train y validation.
- Calcular diferencia porcentual.
- Verificar que la diferencia es inferior al 5%.

## 4. Solución productivizada

**Objetivo:** crear una aplicación para usar el modelo fuera del notebook.

Estado:

```text
Pendiente
```

Checklist:

- Guardar el modelo entrenado.
- Crear aplicación con Streamlit, Gradio, Dash o API.
- Cargar el modelo desde la app.
- Permitir introducir valores de entrada.
- Mostrar la predicción de `FloodProbability`.
- Documentar cómo ejecutar la aplicación.

Próximo paso:

```text
Crear app/app.py con Streamlit.
```

## 5. Informe del rendimiento del modelo

**Objetivo:** explicar cómo funciona el modelo y evaluar su rendimiento.

Estado:

```text
Hecho
```

Evidencia:

- Notebook: `notebooks/02_modeling.ipynb`
- Métricas calculadas: RMSE, MAE y R2.
- Incluye comparación train/test.
- Incluye predicción vs valor real.
- Incluye análisis de residuos.
- Incluye interpretación mediante coeficientes del modelo lineal.

Resultados principales:

| Modelo | RMSE Validation | MAE Validation | R2 Validation | Overfitting R2 |
|---|---:|---:|---:|---:|
| Linear Regression | 0.0201 | 0.0158 | 0.8449 | 0.077% |

Checklist:

- Calcular RMSE.
- Calcular MAE.
- Calcular R2.
- Comparar modelos.
- Incluir feature importance o interpretación equivalente.
- Incluir gráfico de predicción vs valor real.
- Incluir análisis de residuos.
- Explicar fortalezas y limitaciones del modelo.

## Resumen de estado

| Requisito | Estado |
|---|---|
| Modelo funcional | Hecho |
| EDA con visualizaciones | Hecho |
| Overfitting inferior al 5% | Hecho |
| App productivizada | Pendiente |
| Informe de rendimiento | Hecho |

## Próximo paso recomendado

El único requisito pendiente del Nivel Esencial es la productivización del modelo.

El siguiente paso es crear:

```text
app/app.py
```

La aplicación deberá cargar el modelo guardado, permitir introducir valores para las variables predictoras y mostrar la predicción de `FloodProbability`.
