# Proyecto 4 - Grupo 1

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Regresion-1A7F37?style=for-the-badge)
![Dataset](https://img.shields.io/badge/Dataset-Kaggle-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)
![Modelo](https://img.shields.io/badge/Modelo-Linear%20Regression-8250DF?style=for-the-badge)
![Estado](https://img.shields.io/badge/Nivel%20Esencial-Hecho-1A7F37?style=for-the-badge)

Proyecto grupal de Machine Learning orientado a resolver un problema de regresion con el dataset **Regression with a Flood Prediction Dataset** de Kaggle.

## Vista rapida

| Area | Estado |
|---|---|
| Problema | Prediccion de probabilidad de inundacion |
| Tipo de modelo | Regresion |
| Variable objetivo | `FloodProbability` |
| Dataset | Regression with a Flood Prediction Dataset |
| Fuente | Kaggle |
| Nivel Esencial | Hecho |
| App | Streamlit productivizado |

## Objetivo

Construir un modelo capaz de predecir `FloodProbability`, una variable numerica que representa la probabilidad estimada de inundacion a partir de distintos factores de riesgo.

## Estado actual

El proyecto ya cuenta con:

- EDA documentado en `notebooks/01_EDA.ipynb`.
- Notebook de modelado en `notebooks/02_modeling.ipynb`.
- Modelo baseline entrenado y reutilizable desde Streamlit.
- Aplicacion Streamlit productivizada para realizar predicciones.
- Sistema local de feedback de predicciones.
- Sistema local de recogida de nuevos registros para futuros reentrenamientos.
- Vista separada para prediccion, informes tecnicos y exploracion de datos.

## Dataset

| Elemento | Valor |
|---|---|
| Fuente | Kaggle |
| Competicion | Regression with a Flood Prediction Dataset |
| URL | https://www.kaggle.com/competitions/playground-series-s4e5 |
| Archivo principal | `train.csv` |
| Variable objetivo | `FloodProbability` |
| Tipo de problema | Regresion |

Los CSV deben descargarse desde Kaggle y colocarse localmente en:

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

## Instalacion

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

## Ejecutar la aplicacion

Desde la raiz del proyecto:

```bash
streamlit run app/app.py
```

La app incluye tres vistas:

- `Prediccion`: calcula el riesgo estimado de inundacion.
- `Informes tecnicos`: muestra y contextualiza los notebooks del proyecto.
- `Datos`: permite revisar una muestra del dataset y, si esta instalado, usar PyGWalker.

## Notebooks

| Notebook | Contenido | Estado |
|---|---|---|
| `notebooks/01_EDA.ipynb` | Carga, revision inicial, visualizaciones y conclusiones del EDA | Hecho |
| `notebooks/02_modeling.ipynb` | Modelado baseline, metricas, overfitting, residuos e interpretacion | Hecho |

## Estado del Nivel Esencial

| Requisito | Estado | Evidencia |
|---|---|---|
| Modelo funcional de regresion | Hecho | `notebooks/02_modeling.ipynb` |
| EDA con visualizaciones | Hecho | `notebooks/01_EDA.ipynb` |
| Overfitting inferior al 5% | Hecho | 0.077% |
| Informe de rendimiento | Hecho | Metricas, residuos, prediccion vs real |
| App productivizada | Hecho | `app/app.py` |

## Resultado baseline

El mejor modelo baseline identificado hasta el momento es `Linear Regression`.

| Modelo | RMSE Validation | MAE Validation | R2 Validation | Overfitting R2 |
|---|---:|---:|---:|---:|
| Linear Regression | 0.0201 | 0.0158 | 0.8449 | 0.077% |

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

## Documentacion del proyecto

| Documento | Contenido |
|---|---|
| `docs/dataset.md` | Informacion del dataset, rutas y archivos generados |
| `docs/project_management/github_workflow.md` | Flujo de trabajo con ramas, commits y Pull Requests |
| `docs/project_management/essential_level_checklist.md` | Seguimiento del Nivel Esencial |
| `docs/project_management/streamlit_app.md` | Funcionamiento actual de la app Streamlit |
| `docs/project_management/streamlit_plan.md` | Plan original de la app Streamlit |
| `docs/dailies/` | Registro de reuniones diarias |

## Tecnologias

| Area | Herramientas |
|---|---|
| Analisis de datos | Pandas, NumPy |
| Visualizacion | Matplotlib, Seaborn |
| Machine Learning | Scikit-learn |
| Productivizacion | Streamlit |
| Persistencia de modelo | Joblib |
| Exploracion opcional | PyGWalker |
| Entorno de trabajo | Jupyter Notebook, Google Colab, VS Code |

## Flujo de trabajo

| Rama | Uso |
|---|---|
| `main` | Versiones estables |
| `dev` | Rama principal de desarrollo |
| ramas de tarea | Cambios concretos mediante Pull Request |

Los cambios se integran mediante Pull Requests hacia `dev`. La rama `main` queda reservada para una version estable del proyecto.
