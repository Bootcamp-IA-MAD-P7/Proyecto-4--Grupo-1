# Checklist Nivel Esencial

Este documento resume los requisitos mínimos que debe cumplir el proyecto para alcanzar el Nivel Esencial.

## 1. Modelo de ML funcional

**Objetivo:** entrenar al menos un modelo capaz de predecir una variable numérica.

Estado:

```text
Pendiente
```

Checklist:

- Separar variables predictoras `X` y variable objetivo `y`.
- Eliminar columnas no predictivas como `id`.
- Crear conjunto de entrenamiento y validación.
- Entrenar al menos un modelo baseline.
- Generar predicciones.
- Calcular métricas de regresión.

## 2. Análisis exploratorio de datos

**Objetivo:** analizar los datos con visualizaciones relevantes para regresión.

Estado:

```text
En progreso
```

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
Pendiente
```

Checklist:

- Calcular métricas en entrenamiento.
- Calcular métricas en validación.
- Comparar resultados de train y validation.
- Calcular diferencia porcentual.
- Ajustar el modelo si la diferencia supera el 5%.

Ejemplo de tabla esperada:

| Modelo | R2 Train | R2 Validation | Diferencia | Estado |
|---|---:|---:|---:|---|
| Random Forest | Pendiente | Pendiente | Pendiente | Pendiente |

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

## 5. Informe del rendimiento del modelo

**Objetivo:** explicar cómo funciona el modelo y evaluar su rendimiento.

Estado:

```text
Pendiente
```

Checklist:

- Calcular RMSE.
- Calcular MAE.
- Calcular R2.
- Comparar modelos si se entrena más de uno.
- Incluir feature importance.
- Incluir gráfico de predicción vs valor real.
- Incluir análisis de residuos.
- Explicar fortalezas y limitaciones del modelo.

## Resumen de estado

| Requisito | Estado |
|---|---|
| Modelo funcional | Pendiente |
| EDA con visualizaciones | En progreso |
| Overfitting inferior al 5% | Pendiente |
| App productivizada | Pendiente |
| Informe de rendimiento | Pendiente |

## Próximo paso recomendado

Una vez completado el EDA, el siguiente paso es preparar el notebook de modelado:

```text
notebooks/02_modeling.ipynb
```

Este notebook debería incluir:

- separación de `X` e `y`,
- train/validation split,
- modelo baseline,
- métricas RMSE, MAE y R2,
- comparación train vs validation,
- análisis de overfitting.
