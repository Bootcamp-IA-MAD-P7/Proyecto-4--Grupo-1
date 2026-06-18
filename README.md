# Proyecto 4 - Grupo 1

Proyecto grupal de Machine Learning orientado a resolver un problema de regresion usando el dataset **Regression with a Flood Prediction Dataset** de Kaggle.

## Objetivo

El objetivo del proyecto es construir un modelo capaz de predecir la variable numerica `FloodProbability`, que representa la probabilidad estimada de inundacion a partir de diferentes factores de riesgo.

## Dataset

- Fuente: Kaggle
- Competicion: Regression with a Flood Prediction Dataset
- URL: https://www.kaggle.com/competitions/playground-series-s4e5
- Archivo principal para EDA y entrenamiento: `train.csv`
- Variable objetivo: `FloodProbability`
- Tipo de problema: Regresion

Los archivos del dataset deben descargarse desde Kaggle y colocarse localmente en:

```text
data/raw/
```

Por defecto, los CSV no se suben al repositorio para evitar incluir datos pesados.

## Estructura del proyecto

```text
Proyecto-4--Grupo-1/
├── app/
├── data/
│   ├── raw/
│   └── processed/
├── docs/
│   ├── dailies/
│   ├── project_management/
│   └── templates/
├── models/
├── notebooks/
├── reports/
│   └── figures/
├── src/
├── .gitignore
├── README.md
└── requirements.txt
```

## Tecnologias

- Python
- Jupyter Notebook / Google Colab
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn
- Optuna
- Streamlit

## Instalacion

Crear un entorno virtual e instalar dependencias:

```bash
pip install -r requirements.txt
```

## Estado actual

- Dataset seleccionado.
- EDA inicial en preparacion.
- Pendiente: modelado baseline, evaluacion, control de overfitting y app de Streamlit.
