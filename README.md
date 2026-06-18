# Proyecto 4 - Grupo 1

<p>
  <span style="color: #0969da;"><strong>Machine Learning</strong></span> ·
  <span style="color: #1a7f37;"><strong>Regresión</strong></span> ·
  <span style="color: #8250df;"><strong>Kaggle</strong></span> ·
  <span style="color: #9a6700;"><strong>Streamlit pendiente</strong></span>
</p>

Proyecto grupal de Machine Learning orientado a resolver un problema de regresión usando el dataset **Regression with a Flood Prediction Dataset** de Kaggle.

## Resumen

| Campo | Descripción |
|---|---|
| Problema | Predicción de probabilidad de inundación |
| Tipo de modelo | Regresión |
| Variable objetivo | `FloodProbability` |
| Dataset | Regression with a Flood Prediction Dataset |
| Fuente | Kaggle |
| Estado Nivel Esencial | Casi completo |
| Pendiente principal | App productivizada con Streamlit |

## Objetivo

Construir un modelo capaz de predecir la variable numérica `FloodProbability`, que representa la probabilidad estimada de inundación a partir de diferentes factores de riesgo.

## Dataset

| Elemento | Valor |
|---|---|
| Fuente | Kaggle |
| Competición | Regression with a Flood Prediction Dataset |
| URL | https://www.kaggle.com/competitions/playground-series-s4e5 |
| Archivo principal | `train.csv` |
| Variable objetivo | `FloodProbability` |
| Tipo de problema | Regresión |

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

| Área | Herramientas |
|---|---|
| Análisis de datos | Pandas, NumPy |
| Visualización | Matplotlib, Seaborn |
| Machine Learning | Scikit-learn |
| Optimización | Optuna |
| Productivización | Streamlit |
| Persistencia de modelo | Joblib |
| Entorno de trabajo | Jupyter Notebook, Google Colab, VS Code |

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

| Notebook | Contenido | Estado |
|---|---|---|
| `notebooks/01_EDA.ipynb` | Carga, revisión inicial, visualizaciones y conclusiones del EDA | <span style="color: #1a7f37;"><strong>Hecho</strong></span> |
| `notebooks/02_modeling.ipynb` | Modelado baseline, métricas, overfitting, residuos e interpretación | <span style="color: #1a7f37;"><strong>Hecho</strong></span> |

### `01_EDA.ipynb`

Incluye:

- carga y revisión inicial del dataset,
- análisis de nulos y duplicados,
- análisis de la variable objetivo,
- visualizaciones relevantes para regresión,
- correlaciones,
- conclusiones del EDA.

### `02_modeling.ipynb`

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

| Requisito | Estado | Evidencia |
|---|---|---|
| Modelo funcional de regresión | <span style="color: #1a7f37;"><strong>Hecho</strong></span> | `notebooks/02_modeling.ipynb` |
| EDA con visualizaciones | <span style="color: #1a7f37;"><strong>Hecho</strong></span> | `notebooks/01_EDA.ipynb` |
| Overfitting inferior al 5% | <span style="color: #1a7f37;"><strong>Hecho</strong></span> | 0.077% |
| Informe de rendimiento | <span style="color: #1a7f37;"><strong>Hecho</strong></span> | Métricas, residuos, predicción vs real |
| App productivizada | <span style="color: #9a6700;"><strong>Pendiente</strong></span> | `app/app.py` |

## Resultado baseline

El mejor modelo baseline identificado hasta el momento es `Linear Regression`.

| Modelo | RMSE Validation | MAE Validation | R2 Validation | Overfitting R2 |
|---|---:|---:|---:|---:|
| Linear Regression | 0.0201 | 0.0158 | 0.8449 | 0.077% |

## Próximo paso

El requisito pendiente del Nivel Esencial es la **productivización del modelo**.

La siguiente tarea será crear:

```text
app/app.py
```

con Streamlit, para cargar el modelo entrenado y permitir obtener predicciones de `FloodProbability` desde una interfaz sencilla.

## Flujo de trabajo

| Rama | Uso |
|---|---|
| `main` | Versiones estables |
| `dev` | Rama principal de desarrollo |
| ramas de tarea | Cambios concretos mediante Pull Request |

Los cambios se integran mediante Pull Requests hacia `dev`. La rama `main` queda reservada para una versión estable del proyecto.
