# Dataset

## Nombre

Regression with a Flood Prediction Dataset

## Fuente

El dataset procede de una competicion de Kaggle:

https://www.kaggle.com/competitions/playground-series-s4e5

## Objetivo del dataset

El objetivo es predecir `FloodProbability`, que representa la probabilidad estimada de inundacion a partir de diferentes factores de riesgo.

Como la variable objetivo es numerica, el problema se aborda como una tarea de regresion.

## Archivos necesarios

Los archivos principales del dataset son:

```text
train.csv
test.csv
sample_submission.csv
```

Para el analisis exploratorio, entrenamiento y configuracion de la app se utiliza principalmente:

```text
train.csv
```

## Ubicacion local de los datos

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

## Por que no se suben los datos al repositorio

Los archivos CSV no se suben a GitHub porque:

- Pueden ser pesados.
- Kaggle ya funciona como fuente oficial de los datos.
- Es mejor mantener el repositorio centrado en codigo, notebooks y documentacion.

Por este motivo, `.gitignore` excluye los CSV dentro de `data/raw/`.

## Variable objetivo

La variable objetivo es:

```text
FloodProbability
```

Esta variable es numerica continua, por lo que se evalua el modelo con metricas de regresion como:

- RMSE
- MAE
- R2

En la app, el resultado se muestra como porcentaje de riesgo estimado de inundacion.

## Variables predictoras

El dataset incluye variables numericas relacionadas con factores de riesgo de inundacion:

- intensidad del monzon,
- drenaje del terreno,
- gestion de rios,
- deforestacion,
- urbanizacion,
- cambio climatico,
- calidad de presas,
- vulnerabilidad costera,
- deslizamientos,
- perdida de humedales,
- planificacion inadecuada,
- factores politicos.

La app usa los rangos reales observados en `train.csv` para configurar los sliders de entrada.

## Uso en el proyecto

El dataset se utiliza para:

1. Realizar analisis exploratorio de datos.
2. Entrenar modelos de regresion.
3. Evaluar el rendimiento con metricas de regresion.
4. Productivizar el modelo mediante Streamlit.
5. Dar contexto a los controles de entrada de la app.
6. Guardar nuevas observaciones generadas desde la app para futuros reentrenamientos.

## Modelo entrenado

Ruta principal esperada por la app:

```text
models/flood_baseline_model.joblib
```

Ruta secundaria admitida:

```text
data/raw/models/flood_baseline_model.joblib
```

Si la app encuentra el modelo en la ruta secundaria, lo copia automaticamente a `models/`.

## Datos generados por la app

La aplicacion puede generar archivos locales:

```text
data/feedback/predicciones.csv
data/new_data/nuevos_registros.csv
```

Estos archivos no se suben al repositorio porque son datos generados durante el uso de la aplicacion.

## Nota sobre `id`

La columna `id`, si esta presente, funciona como identificador unico de cada registro. No debe utilizarse como variable predictora durante el entrenamiento del modelo.
