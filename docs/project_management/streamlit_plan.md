# Plan de Streamlit

Este documento define el plan para crear una aplicación Streamlit que productivice el modelo de predicción de inundaciones.

## Objetivo

Crear una aplicación sencilla que permita introducir los valores de las variables predictoras y obtener una predicción de `FloodProbability` usando el modelo baseline entrenado.

Este punto cubre el requisito pendiente del Nivel Esencial:

```text
Una solución que productivice el modelo.
```

## Archivo principal

La aplicación debe crearse en:

```text
app/app.py
```

## Modelo a cargar

El modelo esperado es:

```text
models/flood_baseline_model.joblib
```

Este modelo se genera ejecutando el notebook:

```text
notebooks/02_modeling.ipynb
```

## Variables de entrada

La app debe pedir las 20 variables predictoras usadas en el modelo:

```text
MonsoonIntensity
TopographyDrainage
RiverManagement
Deforestation
Urbanization
ClimateChange
DamsQuality
Siltation
AgriculturalPractices
Encroachments
IneffectiveDisasterPreparedness
DrainageSystems
CoastalVulnerability
Landslides
Watersheds
DeterioratingInfrastructure
PopulationScore
WetlandLoss
InadequatePlanning
PoliticalFactors
```

La columna `id` no debe pedirse al usuario porque no se usa como variable predictora.

## Flujo de la aplicación

1. Cargar el modelo con `joblib`.
2. Mostrar un formulario con las variables predictoras.
3. Recoger los valores introducidos por el usuario.
4. Construir un `DataFrame` con una sola fila.
5. Ejecutar `model.predict()`.
6. Mostrar la predicción de `FloodProbability`.

## Diseño recomendado

La aplicación puede ser sencilla:

- Título del proyecto.
- Breve explicación del objetivo.
- Inputs numéricos para cada variable.
- Botón de predicción.
- Resultado destacado.

No hace falta una interfaz compleja para cumplir el Nivel Esencial.

## Comando de ejecución

Desde la raíz del proyecto:

```bash
streamlit run app/app.py
```

## Criterios de aceptación

- La app se ejecuta con `streamlit run app/app.py`.
- La app carga el modelo desde `models/flood_baseline_model.joblib`.
- La app permite introducir las 20 variables predictoras.
- La app genera una predicción numérica de `FloodProbability`.
- La app muestra el resultado de forma clara.
- El README explica cómo ejecutar la app.

## Rama sugerida

```text
app/streamlit-baseline
```

## Pull Request

El Pull Request debe ir hacia:

```text
base: dev
compare: app/streamlit-baseline
```

## Nota importante

Si el archivo `models/flood_baseline_model.joblib` no existe, debe generarse ejecutando primero:

```text
notebooks/02_modeling.ipynb
```

No se recomienda subir datasets CSV al repositorio.
