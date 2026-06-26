# Proyecto 4 - Grupo 1

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Regresion-1A7F37?style=for-the-badge)
![Dataset](https://img.shields.io/badge/Dataset-Kaggle-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)
![App](https://img.shields.io/badge/App-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Estado](https://img.shields.io/badge/Nivel%20Medio-Hecho-1A7F37?style=for-the-badge)

Proyecto grupal de Machine Learning orientado a resolver un problema de **regresion** con el dataset **Regression with a Flood Prediction Dataset** de Kaggle.

La solucion no se limita a entrenar un modelo en notebooks: tambien incluye una aplicacion Streamlit para usar el modelo, guardar feedback, monitorizar resultados, persistir datos en SQLite y preparar nuevos registros para futuros reentrenamientos.

## Resumen ejecutivo

| Area | Estado | Evidencia principal |
|---|---|---|
| Problema de regresion | Hecho | Prediccion numerica de `FloodProbability` |
| EDA | Hecho | `notebooks/01_EDA.ipynb` |
| Modelo baseline | Hecho | `notebooks/02_modeling.ipynb` |
| Ensemble techniques | Hecho | `notebooks/03_ensemble-techniques.ipynb` |
| Optimizacion | Hecho | `notebooks/04_hyperparameter_optimization.ipynb` |
| Validacion cruzada | Hecho | `notebooks/05_cross_validation.ipynb` |
| Productivizacion | Hecho | `app/app.py` |
| Feedback y monitorizacion | Hecho | Vista `Monitorizacion` |
| Pipeline de ingesta | Hecho | Vista `Pipeline de reentrenamiento` |
| Base de datos | Hecho | `src/database.py` y vista `Base de datos` |
| Feature engineering | Hecho | `src/features.py` |
| Exploracion visual | Hecho | PyGWalker en vista `Datos` |

## Que problema resuelve

El objetivo es predecir `FloodProbability`, una variable numerica que representa la probabilidad estimada de inundacion de una zona a partir de factores como intensidad del monzon, drenaje, deforestacion, urbanizacion, calidad de presas, vulnerabilidad costera, planificacion o infraestructura.

Es un problema de regresion porque la salida no es una clase cerrada, sino un valor continuo. En la aplicacion se muestra como porcentaje para que sea mas interpretable.

## Que hace la aplicacion

La aplicacion Streamlit convierte el trabajo tecnico del proyecto en una herramienta usable:

1. Recibe condiciones de una zona mediante controles.
2. Calcula una probabilidad estimada de inundacion.
3. Guarda cada prediccion como registro de seguimiento.
4. Permite incorporar el valor real observado cuando se conozca.
5. Calcula metricas de monitorizacion cuando hay valores reales.
6. Guarda la informacion en CSV y tambien en SQLite.
7. Prepara un dataset validado para futuros reentrenamientos.
8. Muestra indicadores de feature engineering para explicar mejor el riesgo.
9. Permite revisar notebooks y explorar datos desde la propia app.

La idea funcional es cerrar el ciclo:

```text
EDA -> modelo -> app -> prediccion -> feedback -> monitorizacion -> datos validados -> pipeline de ingesta
```

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

## Instalacion

Crear entorno virtual:

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

La aplicacion se abre normalmente en:

```text
http://localhost:8501
```

## Ejecutar con Docker

El proyecto incluye una version dockerizada de la aplicacion Streamlit.

Archivos principales:

```text
Dockerfile
.dockerignore
requirements-docker.txt
```

Construir la imagen desde la raiz del proyecto:

```bash
docker build -t flood-risk-app .
```

Ejecutar el contenedor:

```bash
docker run --rm -p 8501:8501 flood-risk-app
```

Abrir la aplicacion:

```text
http://localhost:8501
```

La imagen usa `python:3.11-slim`, instala las dependencias necesarias para ejecutar la app y expone el puerto `8501`.

Para ejecucion local con datos persistentes, se puede montar la carpeta `data/` como volumen:

```bash
docker run --rm -p 8501:8501 -v "$(pwd)/data:/app/data" flood-risk-app
```

Esto permite conservar feedback, nuevos registros y la base SQLite fuera del ciclo de vida del contenedor.

## Despliegue en Render

La app esta preparada para desplegarse en Render como servicio Docker.

Configuracion recomendada:

| Campo | Valor |
|---|---|
| Service type | Web Service |
| Runtime / Language | Docker |
| Branch | `dev` |
| Dockerfile path | `./Dockerfile` |
| Health check path | `/_stcore/health` |

El `Dockerfile` usa la variable `PORT` si Render la proporciona y, en local, mantiene `8501` como valor por defecto.

Render construye la imagen desde el `Dockerfile` del repositorio y publica una URL web para la aplicacion. Los datos generados dentro del contenedor pueden no persistir entre reinicios si no se configura almacenamiento persistente externo.

## Ejecutar tests unitarios

El proyecto incluye tests unitarios minimos para validar feature engineering, persistencia SQLite y construccion del dataset de reentrenamiento.

Instalar dependencias de desarrollo:

```bash
pip install -r requirements-dev.txt
```

Ejecutar tests:

```bash
python -m pytest
```

## Modelo productivo

La app espera el modelo entrenado en:

```text
models/flood_baseline_model.joblib
```

Si no lo encuentra ahi, tambien lo busca en:

```text
data/raw/models/flood_baseline_model.joblib
```

Si lo encuentra en esa ruta secundaria, lo copia automaticamente a `models/`.

Modelo activo:

| Modelo | RMSE validation | MAE validation | R2 validation | Overfitting R2 |
|---|---:|---:|---:|---:|
| Linear Regression | 0.0201 | 0.0158 | 0.8449 | 0.077% |

El baseline se mantiene como modelo productivo porque los modelos optimizados evaluados no mejoraron su rendimiento global.

## Vistas de la app

| Vista | Funcion |
|---|---|
| `Guia del proyecto` | Explica que hace la app, como se usa y como interpretar sus resultados |
| `Prediccion` | Calcula la probabilidad estimada de inundacion |
| `Monitorizacion` | Revisa feedback, metricas, valores reales y gestion de registros |
| `Base de datos` | Comprueba el guardado estructurado de predicciones en SQLite |
| `Pipeline de reentrenamiento` | Prepara registros validados para futuros reentrenamientos |
| `Informes tecnicos` | Muestra notebooks del proyecto con contexto |
| `Datos` | Muestra muestra del dataset y explorador visual con PyGWalker |

## Flujo practico de uso

1. Entrar en `Prediccion`.
2. Ajustar los factores de riesgo mediante sliders.
3. Pulsar `Calcular riesgo de inundacion`.
4. Revisar el porcentaje estimado y la lectura de riesgo.
5. Si se conoce el valor real observado, guardarlo.
6. Entrar en `Monitorizacion` para revisar errores y metricas.
7. Entrar en `Base de datos` para comprobar que la prediccion quedo persistida.
8. Entrar en `Pipeline de reentrenamiento` para preparar datos validados.
9. Usar `Datos` para explorar visualmente el dataset.

## Feedback, monitorizacion y valor real

Cada prediccion se guarda localmente. Si el valor real todavia no se conoce, el registro queda pendiente. Cuando el valor real se incorpora, la app puede comparar prediccion contra realidad.

Metricas usadas en monitorizacion:

| Metrica | Que indica |
|---|---|
| MAE | Error absoluto medio entre prediccion y valor real |
| RMSE | Error cuadratico medio, penaliza mas los errores grandes |
| R2 | Proporcion de variabilidad explicada cuando hay suficientes valores reales |

Rutas generadas por la app:

```text
data/feedback/predicciones.csv
data/new_data/nuevos_registros.csv
data/processed/retraining_dataset.csv
data/database/flood_app.sqlite
```

Estos archivos son generados localmente y no se suben al repositorio.

## Base de datos

La app guarda datos en una base SQLite local para demostrar persistencia estructurada sin depender de un servidor externo.

Archivo generado:

```text
data/database/flood_app.sqlite
```

Implementacion:

```text
src/database.py
```

Tablas principales:

| Tabla | Contenido |
|---|---|
| `app_predictions` | Predicciones, valores introducidos, modelo, valor real, error y estado |
| `app_events` | Eventos de guardado, actualizacion y borrado |

La vista `Base de datos` permite ver:

- estado de la base,
- total de predicciones,
- predicciones con valor real,
- predicciones pendientes,
- registros recientes.

Tambien se conserva `src/db_setup.sql` como referencia de esquema para una posible migracion futura a PostgreSQL.

## Pipeline de ingesta para reentrenamiento

El pipeline de ingesta esta integrado en la app porque los nuevos datos nacen durante el uso de Streamlit.

Flujo implementado:

1. El usuario realiza una prediccion.
2. La app guarda los valores introducidos y la prediccion.
3. Si no hay valor real, el registro queda como `pending_target`.
4. Cuando existe valor real, pasa a `validated_for_retraining`.
5. El pipeline filtra solo registros con valor real.
6. Se genera `data/processed/retraining_dataset.csv`.

El boton `Ejecutar pipeline de ingesta`:

- aparece en la vista `Pipeline de reentrenamiento`,
- se muestra bloqueado si no hay datos validos,
- se activa cuando existe al menos un registro con valor real,
- genera el dataset de reentrenamiento,
- no cambia el modelo activo.

La prediccion del modelo se conserva como referencia, pero no se usa como target. Para reentrenar se usa el valor real observado como nueva `FloodProbability`.

## Feature engineering

La capa de feature engineering vive en:

```text
src/features.py
```

Indicadores generados:

| Indicador | Interpretacion |
|---|---|
| `risk_score_sum` | Suma total de factores de riesgo |
| `risk_score_mean` | Riesgo medio general |
| `water_pressure_risk` | Presion hidrologica |
| `environmental_risk` | Riesgo ambiental |
| `infrastructure_risk` | Riesgo de infraestructura |
| `planning_risk` | Riesgo de planificacion |
| `exposure_risk` | Exposicion y vulnerabilidad |

Uso actual:

- En `Prediccion`, los indicadores ayudan a explicar el caso introducido.
- En `Pipeline de reentrenamiento`, enriquecen el dataset validado.

El modelo baseline actual sigue usando las 20 variables originales para mantener compatibilidad con el artefacto entrenado. La capa de feature engineering queda preparada para entrenar futuras versiones.

## Exploracion visual de datos

La vista `Datos` incluye:

- tabla de muestra del dataset,
- explorador visual integrado con PyGWalker.

PyGWalker permite cruzar columnas, crear graficos rapidos y reforzar el EDA desde la app sin abrir notebooks ni escribir codigo.

Si el CSV original de Kaggle no esta disponible en un entorno Docker o cloud, la app muestra una muestra de demostracion con la misma estructura de columnas. Esto evita que la vista falle durante una demo o despliegue, sin sustituir al dataset real cuando este disponible localmente.

## Notebooks

| Notebook | Contenido | Estado |
|---|---|---|
| `notebooks/01_EDA.ipynb` | Carga, revision inicial, visualizaciones y conclusiones del EDA | Hecho |
| `notebooks/02_modeling.ipynb` | Modelado baseline, metricas, overfitting, residuos e interpretacion | Hecho |
| `notebooks/03_ensemble-techniques.ipynb` | Comparacion de modelos ensemble frente al baseline | Hecho |
| `notebooks/04_hyperparameter_optimization.ipynb` | GridSearchCV, RandomizedSearchCV y Optuna | Hecho |
| `notebooks/05_cross_validation.ipynb` | Validacion cruzada K-Fold sobre modelos candidatos | Hecho |
| `notebooks/06_retraining_pipeline.ipynb` | Documentacion tecnica del pipeline de datos nuevos | Hecho |

## Cumplimiento del briefing

### Nivel Esencial

| Requisito | Estado | Evidencia |
|---|---|---|
| Modelo funcional de regresion | Hecho | `notebooks/02_modeling.ipynb` |
| EDA con visualizaciones | Hecho | `notebooks/01_EDA.ipynb` |
| Overfitting inferior al 5% | Hecho | 0.077% |
| Solucion productivizada | Hecho | `app/app.py` |
| Informe de rendimiento | Hecho | metricas, residuos, prediccion vs real |

### Nivel Medio

| Requisito | Estado | Evidencia |
|---|---|---|
| Modelo con tecnicas ensemble | Hecho | `notebooks/03_ensemble-techniques.ipynb` |
| Validacion cruzada | Hecho | `notebooks/05_cross_validation.ipynb` |
| Optimizacion de hiperparametros | Hecho | `notebooks/04_hyperparameter_optimization.ipynb` |
| Feedback para monitorizar performance | Hecho | vista `Monitorizacion` |
| Recogida de datos nuevos para reentrenamiento | Hecho | vista `Pipeline de reentrenamiento` |

### Nivel Avanzado abordado

| Requisito | Estado | Evidencia |
|---|---|---|
| Guardado en base de datos | Hecho | SQLite en `src/database.py` |
| Version dockerizada del programa | Hecho | `Dockerfile`, `.dockerignore`, `requirements-docker.txt` |
| Inclusion de tests unitarios | Hecho | `tests/` |
| Despliegue | Preparado | Render Web Service con Docker |

## Distribucion de tareas del equipo

La distribucion se presenta por participante para que la defensa del proyecto tenga una narrativa clara y ordenada.

| Participante | Bloque principal | Tareas asignadas | Evidencia |
|---|---|---|---|
| Participante 1 | Analisis exploratorio y datos | Revision del dataset, analisis de nulos, distribuciones, correlaciones, visualizaciones iniciales y lectura de variables | `notebooks/01_EDA.ipynb`, `docs/dataset.md` |
| Participante 2 | Modelado baseline y metricas | Separacion train/test, entrenamiento de modelos iniciales, seleccion del baseline, analisis de overfitting, residuos, prediccion vs real y guardado del modelo | `notebooks/02_modeling.ipynb` |
| Participante 3 | Mejora y validacion del modelo | Modelos ensemble, comparacion con baseline, validacion cruzada, optimizacion de hiperparametros y explicacion de por que se mantiene el baseline | `notebooks/03_ensemble-techniques.ipynb`, `notebooks/04_hyperparameter_optimization.ipynb`, `notebooks/05_cross_validation.ipynb` |
| Participante 4 | Productivizacion y cierre funcional | App Streamlit, feedback, monitorizacion, base de datos SQLite, pipeline de ingesta, feature engineering, explorador visual, documentacion final y preparacion de despliegue | `app/app.py`, `src/database.py`, `src/features.py`, `notebooks/06_retraining_pipeline.ipynb`, `README.md` |

Trabajo transversal pendiente o coordinado por el equipo:

- Preparacion de presentacion final.
- Revision de narrativa de defensa.
- Dockerizacion de la aplicacion.
- Despliegue.
- Revision final de documentacion y Pull Request hacia `dev`.

## Estructura del proyecto

```text
Proyecto-4--Grupo-1/
|-- app/
|   |-- app.py
|   |-- paths.py
|   |-- style.css
|   `-- assets/
|-- data/
|   |-- feedback/
|   |-- new_data/
|   |-- processed/
|   `-- raw/
|-- docs/
|   |-- dailies/
|   `-- dataset.md
|-- models/
|-- notebooks/
|-- src/
|   |-- database.py
|   |-- db_setup.sql
|   |-- db_insert.py
|   `-- features.py
|-- .gitignore
|-- README.md
`-- requirements.txt
```

## Documentacion del proyecto

| Documento | Contenido |
|---|---|
| `README.md` | Documento principal del proyecto: objetivo, app, modelo, pipeline, base de datos, feature engineering, tareas y ejecucion |
| `docs/dataset.md` | Informacion especifica del dataset, rutas y archivos generados |
| `docs/dailies/` | Registro de reuniones diarias |

El documento narrativo interno del equipo queda fuera de Git en:

```text
docs/internal/
```

## Tecnologias

| Area | Herramientas |
|---|---|
| Analisis de datos | Pandas, NumPy |
| Visualizacion | Matplotlib, Seaborn, PyGWalker |
| Machine Learning | Scikit-learn, XGBoost, LightGBM, Optuna |
| Productivizacion | Streamlit |
| Contenerizacion | Docker |
| Persistencia | SQLite |
| Persistencia de modelo | Joblib |
| Entorno de trabajo | Jupyter Notebook, Google Colab, VS Code |

## Archivos ignorados

No se suben:

- datasets descargados de Kaggle,
- CSV generados por la app,
- bases SQLite locales,
- secretos de Streamlit,
- modelos binarios locales si se generan en `models/`,
- documentacion interna de trabajo en `docs/internal/`.

## Verificaciones realizadas

Comandos usados para revisar el estado antes de merge:

```bash
python -m py_compile app\app.py app\paths.py src\features.py src\database.py src\db_insert.py
python -m pip check
git diff --check
python -m pytest
docker build -t flood-risk-app .
docker run --rm -p 8501:8501 flood-risk-app
```

Tambien se comprobo la carga local de Streamlit en `http://localhost:8501`, tanto en ejecucion local como dentro del contenedor Docker.

## Flujo de Git

| Rama | Uso |
|---|---|
| `main` | Versiones estables |
| `dev` | Rama principal de desarrollo |
| ramas de tarea | Cambios concretos mediante Pull Request |

Los cambios se integran mediante Pull Requests hacia `dev`. La rama `main` queda reservada para versiones estables.
