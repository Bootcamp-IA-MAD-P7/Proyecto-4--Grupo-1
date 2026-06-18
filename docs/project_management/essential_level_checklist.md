# Checklist Nivel Esencial

Este documento resume los requisitos minimos que debe cumplir el proyecto para alcanzar el Nivel Esencial.

## 1. Modelo de ML funcional

**Objetivo:** entrenar al menos un modelo capaz de predecir una variable numerica.

Estado:

```text
Pendiente
```

Checklist:

- Separar variables predictoras `X` y variable objetivo `y`.
- Eliminar columnas no predictivas como `id`.
- Crear conjunto de entrenamiento y validacion.
- Entrenar al menos un modelo baseline.
- Generar predicciones.
- Calcular metricas de regresion.

## 2. Analisis exploratorio de datos

**Objetivo:** analizar los datos con visualizaciones relevantes para regresion.

Estado:

```text
En progreso
```

Checklist:

- Carga y revision inicial del dataset.
- Revision de dimensiones, tipos de datos, nulos y duplicados.
- Distribucion de la variable objetivo `FloodProbability`.
- Matriz de correlacion.
- Correlaciones con la variable objetivo.
- Scatter plots entre variables relevantes y target.
- Histogramas de variables predictoras.
- Boxplots para revisar dispersion y posibles outliers.
- Conclusiones escritas del EDA.

## 3. Overfitting inferior al 5%

**Objetivo:** comprobar que la diferencia entre entrenamiento y validacion es aceptable.

Estado:

```text
Pendiente
```

Checklist:

- Calcular metricas en entrenamiento.
- Calcular metricas en validacion.
- Comparar resultados de train y validation.
- Calcular diferencia porcentual.
- Ajustar el modelo si la diferencia supera el 5%.

Ejemplo de tabla esperada:

| Modelo | R2 Train | R2 Validation | Diferencia | Estado |
|---|---:|---:|---:|---|
| Random Forest | Pendiente | Pendiente | Pendiente | Pendiente |

## 4. Solucion productivizada

**Objetivo:** crear una aplicacion para usar el modelo fuera del notebook.

Estado:

```text
Pendiente
```

Checklist:

- Guardar el modelo entrenado.
- Crear aplicacion con Streamlit, Gradio, Dash o API.
- Cargar el modelo desde la app.
- Permitir introducir valores de entrada.
- Mostrar la prediccion de `FloodProbability`.
- Documentar como ejecutar la aplicacion.

## 5. Informe del rendimiento del modelo

**Objetivo:** explicar como funciona el modelo y evaluar su rendimiento.

Estado:

```text
Pendiente
```

Checklist:

- Calcular RMSE.
- Calcular MAE.
- Calcular R2.
- Comparar modelos si se entrena mas de uno.
- Incluir feature importance.
- Incluir grafico de prediccion vs valor real.
- Incluir analisis de residuos.
- Explicar fortalezas y limitaciones del modelo.

## Resumen de estado

| Requisito | Estado |
|---|---|
| Modelo funcional | Pendiente |
| EDA con visualizaciones | En progreso |
| Overfitting inferior al 5% | Pendiente |
| App productivizada | Pendiente |
| Informe de rendimiento | Pendiente |

## Proximo paso recomendado

Una vez completado el EDA, el siguiente paso es preparar el notebook de modelado:

```text
notebooks/02_modeling.ipynb
```

Este notebook deberia incluir:

- separacion de `X` e `y`,
- train/validation split,
- modelo baseline,
- metricas RMSE, MAE y R2,
- comparacion train vs validation,
- analisis de overfitting.
