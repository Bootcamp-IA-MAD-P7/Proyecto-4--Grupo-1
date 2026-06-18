# Proyecto 4 - Grupo 1

Proyecto grupal de Machine Learning orientado a resolver un problema de regresión usando el dataset **Regression with a Flood Prediction Dataset** de Kaggle.

## Objetivo

El objetivo del proyecto es construir un modelo capaz de predecir la variable numérica `FloodProbability`, que representa la probabilidad estimada de inundación a partir de diferentes factores de riesgo.

## Dataset

- Fuente: Kaggle
- Competición: Regression with a Flood Prediction Dataset
- URL: https://www.kaggle.com/competitions/playground-series-s4e5
- Archivo principal para EDA y entrenamiento: `train.csv`
- Variable objetivo: `FloodProbability`
- Tipo de problema: Regresión

Los archivos del dataset deben descargarse desde Kaggle y colocarse localmente en:

```text
data/raw/
```

Estructura esperada:

```text
data/
`-- raw/
    |-- train.csv
    |-- test.csv
    `-- sample_submission.csv
```

Los CSV no se suben al repositorio para evitar incluir archivos pesados. Kaggle se mantiene como fuente oficial de los datos.

## Estructura del proyecto

```text
Proyecto-4--Grupo-1/
|-- app/
|-- data/
|   |-- raw/
|   `-- processed/
|-- docs/
|   |-- dailies/
|   |-- project_management/
|   `-- templates/
|-- models/
|-- notebooks/
|-- reports/
|   `-- figures/
|-- src/
|-- .gitignore
|-- README.md
`-- requirements.txt
```

## Tecnologías

- Python
- Jupyter Notebook / Google Colab
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn
- Optuna
- Streamlit
- Joblib

## Instalación

Crear un entorno virtual:

```bash
python -m venv .venv
```

Activarlo en Windows con Git Bash:

```bash
source .venv/Scripts/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Notebooks

Los notebooks principales del proyecto son:

```text
notebooks/01_EDA.ipynb
notebooks/02_modeling.ipynb
```

### 01_EDA.ipynb

Incluye:

- carga y revisión inicial del dataset,
- análisis de nulos y duplicados,
- análisis de la variable objetivo,
- visualizaciones relevantes para regresión,
- correlaciones,
- conclusiones del EDA.

### 02_modeling.ipynb

Incluye:

- separación de variables predictoras y variable objetivo,
- train/test split,
- entrenamiento de modelos baseline,
- métricas RMSE, MAE y R2,
- comparación train/test,
- cálculo de overfitting,
- gráfico de predicción vs valor real,
- análisis de residuos,
- interpretación mediante coeficientes,
- guardado del modelo baseline.

## Estado actual del Nivel Esencial

| Requisito | Estado |
|---|---|
| Modelo funcional de regresión | Hecho |
| EDA con visualizaciones | Hecho |
| Overfitting inferior al 5% | Hecho |
| Informe de rendimiento | Hecho |
| App productivizada | Pendiente |

## Resultado baseline

El mejor modelo baseline identificado hasta el momento es `Linear Regression`.

Resultados principales:

| Modelo | RMSE Validation | MAE Validation | R2 Validation | Overfitting R2 |
|---|---:|---:|---:|---:|
| Linear Regression | 0.0201 | 0.0158 | 0.8449 | 0.077% |

## Próximo paso

El requisito pendiente del Nivel Esencial es la productivización del modelo.

La siguiente tarea será crear:

```text
app/app.py
```

con Streamlit, para cargar el modelo entrenado y permitir obtener predicciones de `FloodProbability` desde una interfaz sencilla.

## Flujo de trabajo

El equipo trabaja con:

```text
main
dev
ramas de tarea
```

La rama `dev` se utiliza como rama principal de desarrollo. Los cambios se integran mediante Pull Requests hacia `dev`.

La rama `main` se reserva para versiones estables del proyecto.
