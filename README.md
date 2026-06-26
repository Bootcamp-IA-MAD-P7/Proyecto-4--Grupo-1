# Proyecto 4 - Grupo 1

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Regresion-1A7F37?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/App-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Hecho-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Render](https://img.shields.io/badge/Deploy-Render-000000?style=for-the-badge&logo=render&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Persistencia-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)

Proyecto grupal de Machine Learning orientado a resolver un problema de **regresion** con el dataset **Regression with a Flood Prediction Dataset** de Kaggle.

La solucion convierte un modelo entrenado en notebooks en una aplicacion desplegada y usable: permite estimar probabilidad de inundacion, guardar predicciones, recoger valor real observado, monitorizar errores, persistir datos en base de datos y preparar registros validados para futuros reentrenamientos.

## Aplicacion desplegada

URL de la app:

```text
https://flood-risk-app-v7u1.onrender.com/
```

La app esta desplegada en Render como Web Service Docker. En despliegue usa PostgreSQL persistente mediante `DATABASE_URL`; en local usa SQLite como fallback.

## Estado del proyecto

| Bloque | Estado | Evidencia |
|---|---|---|
| Problema de regresion | Hecho | Prediccion numerica de `FloodProbability` |
| EDA | Hecho | `notebooks/01_EDA.ipynb` |
| Modelo baseline | Hecho | `notebooks/02_modeling.ipynb` |
| Ensemble techniques | Hecho | `notebooks/03_ensemble-techniques.ipynb` |
| Validacion cruzada | Hecho | `notebooks/05_cross_validation.ipynb` |
| Optimizacion de hiperparametros | Hecho | `notebooks/04_hyperparameter_optimization.ipynb` |
| App productivizada | Hecho | `app/app.py` |
| Feedback y monitorizacion | Hecho | Vista `Monitorizacion` |
| Pipeline de ingesta | Hecho | Vista `Pipeline de reentrenamiento` y `src/pipeline.py` |
| Feature engineering | Hecho | `src/features.py` |
| Base de datos | Hecho | SQLite local y PostgreSQL en Render |
| Docker | Hecho | `Dockerfile`, `.dockerignore`, `requirements-docker.txt` |
| Despliegue | Hecho | Render Web Service |
| Tests unitarios | Hecho | `tests/` |
| Documentacion | Hecho | `README.md`, `docs/dataset.md`, `docs/dailies/` |
| Jira | Pendiente administrativo | Actualizacion final del tablero |

## Que problema resuelve

El objetivo es predecir `FloodProbability`, una variable numerica que representa la probabilidad estimada de inundacion de una zona a partir de factores como intensidad del monzon, drenaje, gestion de rios, deforestacion, urbanizacion, calidad de presas, vulnerabilidad costera, planificacion, preparacion ante desastres o infraestructura.

Es un problema de regresion porque la salida no es una categoria cerrada, sino un valor continuo. En la app se muestra como porcentaje para facilitar su interpretacion.

## Que hace la aplicacion

La aplicacion Streamlit cierra el ciclo funcional del proyecto:

```text
EDA -> modelo -> app -> prediccion -> feedback -> monitorizacion -> base de datos -> pipeline de ingesta
```

Funciones principales:

1. Recibe las condiciones de una zona mediante controles.
2. Calcula una probabilidad estimada de inundacion.
3. Guarda cada prediccion como registro de seguimiento.
4. Permite incorporar el valor real observado cuando se conozca.
5. Calcula metricas de monitorizacion cuando existen valores reales.
6. Persiste los datos en CSV y base de datos.
7. Prepara registros validados para futuros reentrenamientos.
8. Calcula indicadores de feature engineering para explicar mejor el riesgo.
9. Integra notebooks e inspeccion visual de datos dentro de la app.

## Como interpretar los valores de entrada

Los controles de la vista `Prediccion` no son porcentajes. Son puntuaciones discretas del dataset original. Cada factor usa el rango observado en entrenamiento.

Ejemplos de rangos reales:

| Variable | Minimo | Maximo |
|---|---:|---:|
| `MonsoonIntensity` | 0 | 16 |
| `TopographyDrainage` | 0 | 18 |
| `WetlandLoss` | 0 | 19 |
| `PoliticalFactors` | 0 | 16 |

Interpretacion general:

```text
valor bajo = menor presencia o intensidad del factor
valor alto = mayor presencia o intensidad del factor
```

La app usa 20 variables predictoras, pero eso no significa que cada variable vaya de 0 a 20. La salida `FloodProbability` si se muestra como porcentaje porque representa la probabilidad estimada de inundacion.

## Demo recomendada

Orden sugerido para presentar la aplicacion:

| Paso | Vista | Mensaje clave |
|---|---|---|
| 1 | `Guia del proyecto` | La app convierte el modelo en una herramienta usable |
| 2 | `Prediccion` | Se introducen condiciones de una zona y se obtiene una probabilidad |
| 3 | `Monitorizacion` | Las predicciones guardadas permiten medir errores cuando hay valor real |
| 4 | `Base de datos` | En Render los registros se guardan en PostgreSQL persistente |
| 5 | `Pipeline de reentrenamiento` | Solo los casos con valor real observado entran en el dataset validado |
| 6 | `Datos` | La app permite explorar el dataset o una muestra de demostracion |
| 7 | `Informes tecnicos` | Los notebooks justifican el EDA, el modelado y la evaluacion |

Ejemplo de narracion:

```text
La aplicacion no solo predice. Permite usar el modelo, guardar feedback real,
monitorizar el rendimiento y preparar nuevos datos validados para mejorar futuras
versiones del modelo.
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

Los CSV originales deben descargarse desde Kaggle y colocarse localmente en:

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

Los CSV originales no se suben al repositorio. Si el dataset real no existe en Docker o Render, la app muestra una muestra de demostracion con la misma estructura para que la vista `Datos` siga funcionando durante la demo.

## Modelo productivo

La app usa un modelo baseline de regresion lineal guardado como artefacto `joblib`.

Rutas de busqueda:

```text
models/flood_baseline_model.joblib
data/raw/models/flood_baseline_model.joblib
```

Si el modelo se encuentra en la ruta secundaria, la app lo copia automaticamente a `models/`.

Metricas del modelo activo:

| Modelo | RMSE validation | MAE validation | R2 validation | Overfitting R2 |
|---|---:|---:|---:|---:|
| Linear Regression | 0.0201 | 0.0158 | 0.8449 | 0.077% |

El baseline se mantiene como modelo productivo porque los modelos optimizados y ensemble evaluados no mejoraron su rendimiento global de forma suficiente para sustituirlo.

## Vistas de la app

| Vista | Funcion |
|---|---|
| `Guia del proyecto` | Explica que hace la app, como se usa y como interpretar resultados |
| `Prediccion` | Calcula la probabilidad estimada de inundacion |
| `Monitorizacion` | Revisa feedback, metricas, valores reales y gestion de registros |
| `Base de datos` | Comprueba el guardado estructurado en SQLite local o PostgreSQL en Render |
| `Pipeline de reentrenamiento` | Prepara registros validados para futuros reentrenamientos |
| `Informes tecnicos` | Muestra notebooks del proyecto con contexto |
| `Datos` | Muestra tabla de datos y explorador visual con PyGWalker |

## Flujo practico de uso

1. Entrar en `Prediccion`.
2. Ajustar los factores de riesgo mediante sliders.
3. Pulsar `Calcular riesgo de inundacion`.
4. Revisar el porcentaje estimado y la lectura de riesgo.
5. Si se conoce el valor real observado, marcar la casilla correspondiente y guardarlo.
6. Entrar en `Monitorizacion` para revisar errores y metricas.
7. Entrar en `Base de datos` para comprobar que el registro quedo persistido.
8. Entrar en `Pipeline de reentrenamiento` para generar el dataset validado.
9. Usar `Datos` para explorar visualmente la estructura del dataset.

## Feedback y monitorizacion

Cada prediccion queda guardada. Si el valor real todavia no se conoce, el registro queda pendiente. Cuando el valor real se incorpora, la app compara prediccion y realidad.

Metricas usadas:

| Metrica | Interpretacion |
|---|---|
| MAE | Error absoluto medio entre prediccion y valor real |
| RMSE | Error cuadratico medio; penaliza mas los errores grandes |
| R2 | Proporcion de variabilidad explicada cuando hay suficientes valores reales |

Rutas generadas en local:

```text
data/feedback/predicciones.csv
data/new_data/nuevos_registros.csv
data/processed/retraining_dataset.csv
data/database/flood_app.sqlite
```

Estos archivos son generados por uso de la app y no se suben al repositorio.

## Base de datos

La persistencia esta implementada en:

```text
src/database.py
```

Comportamiento:

| Entorno | Motor | Persistencia |
|---|---|---|
| Local sin `DATABASE_URL` | SQLite | Archivo local `data/database/flood_app.sqlite` |
| Render con `DATABASE_URL` | PostgreSQL | Base persistente gestionada por Render |

Tablas principales:

| Tabla | Contenido |
|---|---|
| `app_predictions` | Predicciones, valores introducidos, modelo, valor real, error y estado |
| `app_events` | Eventos de guardado, actualizacion y borrado |

La vista `Base de datos` muestra:

- motor activo,
- total de predicciones,
- predicciones con valor real,
- predicciones pendientes,
- registros recientes.

Configuracion en Render:

1. Crear una base PostgreSQL.
2. Copiar su `Internal Database URL`.
3. Anadirla al Web Service como variable `DATABASE_URL`.
4. Redeplegar la aplicacion.

Con esta configuracion, los registros sobreviven a reinicios y nuevos despliegues del contenedor.

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

La prediccion del modelo se conserva como referencia, pero no se usa como variable objetivo. Para reentrenar se usa el valor real observado como nueva `FloodProbability`.

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

El modelo productivo actual sigue usando las 20 variables originales para mantener compatibilidad con el artefacto entrenado. La capa de feature engineering queda preparada para entrenar futuras versiones.

## Exploracion visual de datos

La vista `Datos` incluye:

- tabla de muestra del dataset,
- explorador visual integrado con PyGWalker.

PyGWalker permite cruzar columnas, crear graficos rapidos y reforzar el EDA desde la app sin abrir notebooks ni escribir codigo.

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

### Nivel esencial

| Requisito | Estado | Evidencia |
|---|---|---|
| Modelo funcional de regresion | Hecho | `notebooks/02_modeling.ipynb` |
| EDA con visualizaciones | Hecho | `notebooks/01_EDA.ipynb` |
| Overfitting inferior al 5% | Hecho | 0.077% |
| Solucion productivizada | Hecho | `app/app.py` |
| Informe de rendimiento | Hecho | metricas, residuos, prediccion vs real |

### Nivel medio

| Requisito | Estado | Evidencia |
|---|---|---|
| Modelo con tecnicas ensemble | Hecho | `notebooks/03_ensemble-techniques.ipynb` |
| Validacion cruzada | Hecho | `notebooks/05_cross_validation.ipynb` |
| Optimizacion de hiperparametros | Hecho | `notebooks/04_hyperparameter_optimization.ipynb` |
| Feedback para monitorizar performance | Hecho | Vista `Monitorizacion` |
| Recogida de datos nuevos para reentrenamiento | Hecho | Vista `Pipeline de reentrenamiento` |

### Nivel avanzado

| Requisito | Estado | Evidencia |
|---|---|---|
| Version dockerizada del programa | Hecho | `Dockerfile`, `.dockerignore`, `requirements-docker.txt` |
| Guardado en base de datos | Hecho | SQLite local y PostgreSQL en Render |
| Despliegue | Hecho | Render Web Service Docker |
| Inclusion de tests unitarios | Hecho | `tests/` |

## Instalacion local

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

Ejecutar la app:

```bash
streamlit run app/app.py
```

Abrir:

```text
http://localhost:8501
```

## Docker

Construir la imagen:

```bash
docker build -t flood-risk-app .
```

Ejecutar el contenedor:

```bash
docker run --rm -p 8501:8501 flood-risk-app
```

Ejecutar con volumen local para conservar datos generados:

```bash
docker run --rm -p 8501:8501 -v "$(pwd)/data:/app/data" flood-risk-app
```

El `Dockerfile` usa la variable `PORT` si el entorno la proporciona y, en local, mantiene `8501` como valor por defecto.

## Tests

Instalar dependencias de desarrollo:

```bash
pip install -r requirements-dev.txt
```

Ejecutar tests:

```bash
python -m pytest
```

Tests incluidos:

| Test | Objetivo |
|---|---|
| `tests/test_features.py` | Validar indicadores de feature engineering |
| `tests/test_database.py` | Validar ciclo de guardado, actualizacion y borrado en SQLite |
| `tests/test_pipeline.py` | Validar que el dataset de reentrenamiento solo usa registros con valor real |

## Verificaciones realizadas

Comandos usados en la revision final:

```bash
python -m pytest
python -m py_compile app\app.py app\paths.py src\features.py src\database.py src\db_insert.py src\pipeline.py
git diff --check
docker build -t flood-risk-app .
docker run --rm -p 8501:8501 flood-risk-app
```

Resultados:

| Verificacion | Resultado |
|---|---|
| Tests unitarios | `5 passed` |
| Compilacion Python | Correcta |
| Revision de espacios con Git | Correcta |
| Build Docker | Correcto |
| Ejecucion local Docker | Correcta |
| Despliegue Render | Correcto |

## Distribucion de tareas del equipo

La distribucion se presenta para ordenar la defensa y explicar responsabilidades por bloque.

| Participante | Bloque principal | Tareas asignadas | Evidencia |
|---|---|---|---|
| Participante 1 | Analisis exploratorio y datos | Revision del dataset, nulos, distribuciones, correlaciones, visualizaciones iniciales y lectura de variables | `notebooks/01_EDA.ipynb`, `docs/dataset.md` |
| Participante 2 | Modelado baseline y metricas | Separacion train/test, entrenamiento inicial, seleccion del baseline, overfitting, residuos, prediccion vs real y guardado del modelo | `notebooks/02_modeling.ipynb` |
| Participante 3 | Mejora y validacion | Modelos ensemble, comparacion con baseline, validacion cruzada, optimizacion de hiperparametros y explicacion de resultados | `notebooks/03_ensemble-techniques.ipynb`, `notebooks/04_hyperparameter_optimization.ipynb`, `notebooks/05_cross_validation.ipynb` |
| Participante 4 | Productivizacion y cierre | App Streamlit, feedback, monitorizacion, base de datos, pipeline de ingesta, feature engineering, Docker, despliegue, tests y documentacion | `app/app.py`, `src/database.py`, `src/features.py`, `src/pipeline.py`, `Dockerfile`, `tests/`, `README.md` |

Pendiente administrativo:

- Actualizar Jira con el cierre final del proyecto.

## Estructura del proyecto

```text
Proyecto-4--Grupo-1/
|-- app/
|   |-- app.py
|   |-- paths.py
|   |-- style.css
|   |-- assets/
|   `-- notebooks_html/
|-- data/
|   |-- processed/
|   `-- raw/
|       `-- models/
|-- docs/
|   |-- dailies/
|   `-- dataset.md
|-- models/
|-- notebooks/
|-- reports/
|-- src/
|   |-- database.py
|   |-- db_insert.py
|   |-- db_setup.sql
|   |-- features.py
|   `-- pipeline.py
|-- tests/
|-- .dockerignore
|-- .gitignore
|-- Dockerfile
|-- README.md
|-- requirements.txt
|-- requirements-dev.txt
`-- requirements-docker.txt
```

## Documentacion

| Documento | Contenido |
|---|---|
| `README.md` | Documento principal del proyecto |
| `docs/dataset.md` | Informacion especifica del dataset |
| `docs/dailies/` | Registro de dailies |

El documento narrativo interno del equipo queda fuera de Git:

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
| Despliegue | Render |
| Persistencia | SQLite local, PostgreSQL en Render |
| Persistencia de modelo | Joblib |
| Entorno de trabajo | Jupyter Notebook, Google Colab, VS Code |

## Archivos ignorados

No se suben:

- datasets descargados de Kaggle,
- CSV generados por la app,
- bases SQLite locales,
- secretos de Streamlit,
- documentacion interna en `docs/internal/`.

## Flujo de Git

| Rama | Uso |
|---|---|
| `main` | Version final estable |
| `dev` | Rama principal de desarrollo |
| ramas de tarea | Cambios concretos mediante Pull Request |

El flujo de trabajo usa Pull Requests hacia `dev` y, tras validacion final, merge de `dev` hacia `main`.
