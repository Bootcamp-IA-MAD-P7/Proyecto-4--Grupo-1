# Dataset

## Nombre

Regression with a Flood Prediction Dataset

## Fuente

El dataset procede de una competición de Kaggle:

https://www.kaggle.com/competitions/playground-series-s4e5

## Objetivo del dataset

El objetivo es predecir la variable `FloodProbability`, que representa la probabilidad estimada de inundación a partir de diferentes factores de riesgo.

Como la variable objetivo es numérica, el problema se aborda como una tarea de regresión.

## Archivos necesarios

Los archivos principales del dataset son:

```text
train.csv
test.csv
sample_submission.csv
```

Para el análisis exploratorio y el entrenamiento del modelo se utiliza principalmente:

```text
train.csv
```

## Ubicación local de los datos

Los archivos CSV deben descargarse manualmente desde Kaggle y colocarse en:

```text
data/raw/
```

La estructura esperada es:

```text
data/
`-- raw/
    |-- train.csv
    |-- test.csv
    `-- sample_submission.csv
```

## Por qué no se suben los datos al repositorio

Los archivos CSV no se suben a GitHub porque:

- Pueden ser pesados.
- Kaggle ya funciona como fuente oficial de los datos.
- Es mejor mantener el repositorio centrado en código, notebooks, documentación y modelos reproducibles.

Por este motivo, `.gitignore` excluye los CSV dentro de `data/raw/`.

## Variable objetivo

La variable objetivo es:

```text
FloodProbability
```

Esta variable es numérica continua, por lo que se evaluará el modelo con métricas de regresión como:

- RMSE
- MAE
- R2

## Variables predictoras

El dataset incluye diferentes variables numéricas relacionadas con factores de riesgo de inundación, como:

- intensidad del monzón,
- drenaje del terreno,
- gestión de ríos,
- deforestación,
- urbanización,
- cambio climático,
- calidad de presas,
- vulnerabilidad costera,
- deslizamientos,
- planificación inadecuada,
- factores políticos.

## Uso en el proyecto

El dataset se utilizará para:

1. Realizar análisis exploratorio de datos.
2. Entrenar modelos de regresión.
3. Evaluar el rendimiento con métricas de regresión.
4. Productivizar el modelo mediante una aplicación.

## Nota sobre `id`

La columna `id`, si está presente, funciona como identificador único de cada registro. No debe utilizarse como variable predictora durante el entrenamiento del modelo.
