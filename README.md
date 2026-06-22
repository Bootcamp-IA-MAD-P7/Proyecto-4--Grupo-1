# Proyecto 4 - Grupo 1

Proyecto grupal de Machine Learning orientado a resolver un problema de regresion con el dataset **Regression with a Flood Prediction Dataset** de Kaggle.

## Objetivo

Construir un modelo capaz de predecir `FloodProbability`, una variable numerica que representa la probabilidad estimada de inundacion a partir de distintos factores de riesgo.

## Estado actual

El proyecto ya cuenta con:

- EDA inicial documentado en `notebooks/01_EDA.ipynb`.
- Notebook de modelado en `notebooks/02_modeling.ipynb`.
- Modelo baseline entrenado y reutilizable desde Streamlit.
- Aplicacion Streamlit productivizada para realizar predicciones.
- Sistema local de feedback de predicciones.
- Sistema local de recogida de nuevos registros para futuros reentrenamientos.
- Vista separada para prediccion, informes tecnicos y exploracion de datos.

## Dataset

- Fuente: Kaggle
- Competicion: Regression with a Flood Prediction Dataset
- URL: https://www.kaggle.com/competitions/playground-series-s4e5
- Archivo principal para EDA y entrenamiento: `train.csv`
- Variable objetivo: `FloodProbability`
- Tipo de problema: regresion

Los CSV deben descargarse desde Kaggle y colocarse localmente en:

```text
data/raw/
```

Los datos no se suben al repositorio. `.gitignore` excluye los CSV de `data/raw/`.

## Modelo

La aplicacion espera el modelo entrenado en:

```text
models/flood_baseline_model.joblib
```

Si no lo encuentra ahi, Streamlit tambien lo busca en:

```text
data/raw/models/flood_baseline_model.joblib
```

Si lo encuentra en esa ruta secundaria, lo copia automaticamente a `models/`.

## Ejecutar la aplicacion

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar Streamlit desde la raiz del proyecto:

```bash
streamlit run app/app.py
```

La app incluye tres vistas:

- `Prediccion`: calcula el riesgo estimado de inundacion.
- `Informes tecnicos`: muestra y contextualiza los notebooks del proyecto.
- `Datos`: permite revisar una muestra del dataset y, si esta instalado, usar PyGWalker.

## Feedback y nuevos datos

Cuando se realiza una prediccion, la app guarda informacion local en:

```text
data/feedback/predicciones.csv
data/new_data/nuevos_registros.csv
```

Estos CSV son generados por la app y no se suben al repositorio.

## Estructura del proyecto

```text
Proyecto-4--Grupo-1/
|-- app/
|-- data/
|   |-- feedback/
|   |-- new_data/
|   |-- processed/
|   `-- raw/
|-- docs/
|   |-- dailies/
|   `-- project_management/
|-- models/
|-- notebooks/
|-- reports/
|   `-- figures/
|-- src/
|-- .gitignore
|-- README.md
`-- requirements.txt
```

## Tecnologias

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn
- Streamlit
- Joblib
- PyGWalker, opcional para exploracion interactiva
