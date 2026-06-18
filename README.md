# Proyecto 4 - Grupo 1

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Regresi%C3%B3n-1A7F37?style=for-the-badge)
![Dataset](https://img.shields.io/badge/Dataset-Kaggle-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)
![Modelo](https://img.shields.io/badge/Modelo-Linear%20Regression-8250DF?style=for-the-badge)
![Estado](https://img.shields.io/badge/Nivel%20Esencial-Casi%20completo-9A6700?style=for-the-badge)

Proyecto grupal de Machine Learning orientado a resolver un problema de regresión usando el dataset **Regression with a Flood Prediction Dataset** de Kaggle.

## Vista rápida

| Área | Estado |
|---|---|
| Problema | Predicción de probabilidad de inundación |
| Tipo de modelo | Regresión |
| Variable objetivo | `FloodProbability` |
| Dataset | Regression with a Flood Prediction Dataset |
| Fuente | Kaggle |
| Nivel Esencial | ![Casi completo](https://img.shields.io/badge/Casi%20completo-9A6700?style=flat-square) |
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
| `notebooks/01_EDA.ipynb` | Carga, revisión inicial, visualizaciones y conclusiones del EDA | ![Hecho](https://img.shields.io/badge/Hecho-1A7F37?style=flat-square) |
| `notebooks/02_modeling.ipynb` | Modelado baseline, métricas, overfitting, residuos e interpretación | ![Hecho](https://img.shields.io/badge/Hecho-1A7F37?style=flat-square) |

### `01_EDA.ipynb`

Incluye carga del dataset, revisión inicial, análisis de nulos y duplicados, distribución de la variable objetivo, visualizaciones relevantes para regresión, correlaciones y conclusiones del EDA.

### `02_modeling.ipynb`

Incluye separación de variables predictoras y objetivo, train/test split, entrenamiento de modelos baseline, métricas RMSE, MAE y R2, control de overfitting, gráficos de predicción vs valor real, análisis de residuos, interpretación mediante coeficientes y guardado del modelo baseline.

## Estado del Nivel Esencial

| Requisito | Estado | Evidencia |
|---|---|---|
| Modelo funcional de regresión | ![Hecho](https://img.shields.io/badge/Hecho-1A7F37?style=flat-square) | `notebooks/02_modeling.ipynb` |
| EDA con visualizaciones | ![Hecho](https://img.shields.io/badge/Hecho-1A7F37?style=flat-square) | `notebooks/01_EDA.ipynb` |
| Overfitting inferior al 5% | ![Hecho](https://img.shields.io/badge/Hecho-1A7F37?style=flat-square) | 0.077% |
| Informe de rendimiento | ![Hecho](https://img.shields.io/badge/Hecho-1A7F37?style=flat-square) | Métricas, residuos, predicción vs real |
| App productivizada | ![Pendiente](https://img.shields.io/badge/Pendiente-9A6700?style=flat-square) | `app/app.py` |

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

## Documentación del proyecto

| Documento | Contenido |
|---|---|
| `docs/dataset.md` | Información del dataset y archivos necesarios |
| `docs/project_management/github_workflow.md` | Flujo de trabajo con ramas, commits y Pull Requests |
| `docs/project_management/essential_level_checklist.md` | Seguimiento del Nivel Esencial |
| `docs/project_management/streamlit_plan.md` | Plan para construir la app de Streamlit |
| `docs/dailies/` | Registro de reuniones diarias |

## Flujo de trabajo

| Rama | Uso |
|---|---|
| `main` | Versiones estables |
| `dev` | Rama principal de desarrollo |
| ramas de tarea | Cambios concretos mediante Pull Request |

Los cambios se integran mediante Pull Requests hacia `dev`. La rama `main` queda reservada para una versión estable del proyecto.
