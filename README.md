# Proyecto 4 - Grupo 1

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Regresi%C3%B3n-1A7F37?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/App-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Hecho-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Render](https://img.shields.io/badge/Deploy-Render-000000?style=for-the-badge&logo=render&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Persistencia-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)

Proyecto grupal de Machine Learning orientado a resolver un problema de **regresión** con el dataset **Regression with a Flood Prediction Dataset** de Kaggle.

La solución no se queda en notebooks: incluye una aplicación Streamlit desplegada, dockerizada, conectada a base de datos persistente en Render y preparada para recoger feedback real, monitorizar rendimiento y generar datos validados para futuros reentrenamientos.

## App desplegada

URL:

```text
https://flood-risk-app-v7u1.onrender.com/
```

Estado final:

| Bloque | Estado |
|---|---|
| App Streamlit | Hecho |
| Docker | Hecho |
| Despliegue Render | Hecho |
| PostgreSQL persistente | Hecho |
| Feedback y monitorización | Hecho |
| Pipeline de ingesta | Hecho |
| Feature engineering | Hecho |
| Tests unitarios | Hecho |
| README final | Hecho |
| Jira | Pendiente administrativo |

## Resumen ejecutivo

La aplicación permite:

1. Introducir condiciones de una zona.
2. Estimar la probabilidad de inundación con un modelo de regresión.
3. Guardar la predicción y los valores introducidos.
4. Incorporar el valor real observado cuando se conozca.
5. Monitorizar errores y métricas del modelo.
6. Persistir registros en base de datos.
7. Preparar registros validados para futuros reentrenamientos.
8. Mostrar indicadores de feature engineering.
9. Consultar datos, notebooks y documentación técnica desde la propia app.

Flujo funcional:

```text
EDA -> modelo -> app -> predicción -> feedback -> monitorización -> base de datos -> pipeline de ingesta
```

## Arquitectura local y Render

La app está preparada para funcionar en dos contextos.

| Contexto | Base de datos | Datos generados | Uso |
|---|---|---|---|
| Local sin `DATABASE_URL` | SQLite | CSV locales + SQLite local | Desarrollo y pruebas |
| Docker local con volumen | SQLite | Persisten si se monta `data/` | Prueba de contenedor |
| Render con `DATABASE_URL` | PostgreSQL | Persisten fuera del contenedor | Demo y despliegue real |

La variable que decide el modo cloud es:

```text
DATABASE_URL
```

Si existe, la app usa PostgreSQL. Si no existe, usa SQLite local.

Esto permite desarrollar sin servidor de base de datos y, al mismo tiempo, dejar una versión desplegada con persistencia real.

## Por qué PostgreSQL en Render

Render ejecuta la app dentro de un contenedor. Los archivos creados dentro del contenedor pueden perderse al reiniciar o redeplegar. Por eso una base SQLite dentro del contenedor no es suficiente para una demo persistente.

Con PostgreSQL:

- las predicciones sobreviven a redeploys,
- la monitorización no depende de CSV temporales,
- la vista `Base de datos` puede mostrar registros persistentes,
- el pipeline puede leer y marcar registros procesados en la base cloud.

## Configuración de Render

Servicio web:

| Campo | Valor |
|---|---|
| Service type | Web Service |
| Runtime | Docker |
| Branch | `dev` |
| Dockerfile path | `./Dockerfile` |
| Health check path | `/_stcore/health` |

Variable de entorno obligatoria para persistencia cloud:

| Variable | Valor |
|---|---|
| `DATABASE_URL` | `Internal Database URL` de PostgreSQL en Render |

Flujo de configuración:

1. Crear Web Service en Render desde el repositorio.
2. Crear PostgreSQL en Render.
3. Copiar `Internal Database URL`.
4. Añadirla al Web Service como `DATABASE_URL`.
5. Redeplegar la app.
6. Verificar en `Base de datos` que aparece `PostgreSQL - Persistente`.

## Qué problema resuelve

El objetivo es predecir `FloodProbability`, una variable numérica que representa la probabilidad estimada de inundación de una zona.

El modelo usa factores como:

- intensidad del monzón,
- drenaje y topografía,
- gestión de ríos,
- deforestación,
- urbanización,
- cambio climático,
- calidad de presas,
- sedimentación,
- vulnerabilidad costera,
- deslizamientos,
- pérdida de humedales,
- planificación urbana,
- factores políticos.

Es regresión porque la salida es un valor continuo. La app transforma esa salida en porcentaje para que sea más fácil de interpretar.

## Valores de entrada

Los controles de `Predicción` no son porcentajes. Son puntuaciones discretas del dataset.

Interpretación:

```text
valor bajo = menor presencia o intensidad del factor
valor alto = mayor presencia o intensidad del factor
```

La app usa 20 variables predictoras, pero eso no significa que cada variable vaya de 0 a 20. Cada control usa el rango real observado en entrenamiento.

Ejemplos:

| Variable | Mínimo | Máximo |
|---|---:|---:|
| `MonsoonIntensity` | 0 | 16 |
| `TopographyDrainage` | 0 | 18 |
| `WetlandLoss` | 0 | 19 |
| `PoliticalFactors` | 0 | 16 |

La salida `FloodProbability` sí se interpreta como probabilidad y se muestra como porcentaje.

## Flujo de uso completo

1. Entrar en `Predicción`.
2. Ajustar factores de riesgo con sliders.
3. Pulsar `Calcular riesgo de inundación`.
4. Revisar probabilidad estimada.
5. Guardar valor real si se conoce.
6. Entrar en `Monitorización`.
7. Revisar MAE, RMSE, R2 y gráfica de error.
8. Entrar en `Base de datos`.
9. Comprobar motor activo y registros persistidos.
10. Entrar en `Pipeline de reentrenamiento`.
11. Ejecutar pipeline si hay registros con valor real.
12. Descargar la vista previa procesada antes de ejecutar o el dataset procesado acumulado después de ejecutar.

## Vistas de la app

| Vista | Función |
|---|---|
| `Guía del proyecto` | Explica la app, el flujo y la interpretación |
| `Predicción` | Calcula probabilidad estimada de inundación |
| `Monitorización` | Mide errores y gestiona valores reales |
| `Base de datos` | Muestra persistencia, motor activo y registros |
| `Pipeline de reentrenamiento` | Genera dataset validado para futuros entrenamientos |
| `Informes técnicos` | Muestra notebooks del proyecto |
| `Datos` | Muestra tabla y explorador visual |

## Feedback y monitorización

Cada predicción se guarda con:

- identificador,
- fecha,
- consultor,
- modelo,
- versión,
- variables introducidas,
- predicción,
- valor real si existe,
- error si se puede calcular,
- estado del registro.

Estados principales:

| Estado | Significado |
|---|---|
| `pending_target` | Predicción guardada sin valor real |
| `validated_for_retraining` | Registro con valor real, listo para ingesta |
| `ingested_for_retraining` | Registro ya incorporado al dataset procesado |

En local, la vista puede apoyarse en CSV. En Render, cuando existe `DATABASE_URL`, lee desde PostgreSQL para que métricas y gráficas no dependan del sistema de archivos temporal.

Métricas:

| Métrica | Interpretación |
|---|---|
| MAE | Error absoluto medio |
| RMSE | Error cuadrático medio; penaliza errores grandes |
| R2 | Variabilidad explicada por el modelo |

## Base de datos

Implementacion:

```text
src/database.py
```

Tablas:

| Tabla | Contenido |
|---|---|
| `app_predictions` | Predicciones, valores de entrada, modelo, valor real, error y estado |
| `app_events` | Eventos de guardado, actualización, borrado e ingesta |

Funciones principales:

| Función | Uso |
|---|---|
| `save_prediction_record` | Guarda o actualiza una predicción |
| `update_actual_value` | Añade valor real y recalcula error |
| `delete_prediction_record` | Elimina registros |
| `load_monitoring_records` | Alimenta la vista de monitorización |
| `load_pipeline_records` | Alimenta la cola del pipeline |
| `mark_predictions_ingested` | Marca registros procesados por el pipeline |

## Pipeline de ingesta

El pipeline prepara datos nuevos para futuros reentrenamientos.

Flujo:

```text
pending_target -> validated_for_retraining -> ingested_for_retraining
```

Funcionamiento:

1. La app guarda predicciones nuevas.
2. Cuando existe valor real, el registro queda validado.
3. El pipeline toma solo registros validados.
4. Genera `retraining_dataset.csv`.
5. Añade feature engineering.
6. Marca registros como `ingested_for_retraining`.
7. Los registros salen de la cola para evitar reprocesarlos.

Importante:

- El pipeline no reentrena el modelo activo.
- El pipeline prepara datos para una futura versión.
- En Render, la cola se gestiona desde PostgreSQL.
- En local, la cola se gestiona desde CSV/SQLite.
- Si hay registros validados pendientes, la vista permite descargar una vista previa procesada.
- Si ya se ejecutó el pipeline y existe un dataset acumulado, la vista muestra `Descargar dataset procesado`.

Notas de uso:

- Las rutas internas que aparecen en algunos desplegables son informativas. Sirven para saber dónde guarda o lee datos la aplicación, pero no hay que copiarlas para usar la app.
- En la versión desplegada, PostgreSQL es la fuente persistente de feedback, monitorización y cola de pipeline.
- En local, esas rutas apuntan a archivos del proyecto y ayudan a depurar o revisar el flujo durante el desarrollo.
- La app evita mostrar esas rutas como bloques de código porque el botón de copiar no aporta valor para un usuario final.

## Feature engineering

Implementacion:

```text
src/features.py
```

Indicadores:

| Indicador | Interpretación |
|---|---|
| `risk_score_sum` | Suma de factores de riesgo |
| `risk_score_mean` | Riesgo medio general |
| `water_pressure_risk` | Presión hidrológica |
| `environmental_risk` | Riesgo ambiental |
| `infrastructure_risk` | Riesgo de infraestructura |
| `planning_risk` | Riesgo de planificación |
| `exposure_risk` | Exposición y vulnerabilidad |

Uso:

- En `Predicción`, ayuda a explicar el caso introducido.
- En `Pipeline de reentrenamiento`, enriquece el dataset validado.

El modelo productivo actual usa las 20 variables originales para mantener compatibilidad con el artefacto entrenado. Las variables engineered quedan preparadas para futuras versiones.

## Dataset

| Elemento | Valor |
|---|---|
| Fuente | Kaggle |
| Competición | Regression with a Flood Prediction Dataset |
| URL | https://www.kaggle.com/competitions/playground-series-s4e5 |
| Archivo principal | `train.csv` |
| Variable objetivo | `FloodProbability` |
| Tipo | Regresión |

Estructura local esperada:

```text
data/
`-- raw/
    |-- train.csv
    |-- test.csv
    `-- sample_submission.csv
```

Los CSV originales no se suben al repositorio. En Docker/Render, si no existe `train.csv`, la vista `Datos` muestra una muestra sintética con la misma estructura para explicar las columnas sin romper la demo. Esa muestra solo afecta a la vista exploratoria: el predictor usa el modelo entrenado y la persistencia de la app se gestiona con PostgreSQL en Render.

## Modelo productivo

Rutas de búsqueda:

```text
models/flood_baseline_model.joblib
data/raw/models/flood_baseline_model.joblib
```

Si el modelo está en la ruta secundaria, la app lo copia a `models/`.

Métricas:

| Modelo | RMSE validation | MAE validation | R2 validation | Overfitting R2 |
|---|---:|---:|---:|---:|
| Linear Regression | 0.0201 | 0.0158 | 0.8449 | 0.077% |

El baseline se mantiene como modelo productivo porque las alternativas ensemble u optimizadas evaluadas no mejoraron de forma suficiente el rendimiento global.

## Notebooks

| Notebook | Contenido |
|---|---|
| `notebooks/01_EDA.ipynb` | EDA, distribuciones, correlaciones y conclusiones |
| `notebooks/02_modeling.ipynb` | Baseline, métricas, residuos y modelo productivo |
| `notebooks/03_ensemble-techniques.ipynb` | Comparación con modelos ensemble |
| `notebooks/04_hyperparameter_optimization.ipynb` | GridSearch, RandomSearch y Optuna |
| `notebooks/05_cross_validation.ipynb` | Validación cruzada K-Fold |
| `notebooks/06_retraining_pipeline.ipynb` | Documentación técnica del pipeline |

## Cumplimiento del briefing

### Nivel esencial

| Requisito | Estado | Evidencia |
|---|---|---|
| Modelo funcional de regresión | Hecho | `notebooks/02_modeling.ipynb` |
| EDA con visualizaciones | Hecho | `notebooks/01_EDA.ipynb` |
| Overfitting inferior al 5% | Hecho | 0.077% |
| Solución productivizada | Hecho | `app/app.py` |
| Informe de rendimiento | Hecho | métricas, residuos y predicción vs real |

### Nivel medio

| Requisito | Estado | Evidencia |
|---|---|---|
| Modelo con técnicas ensemble | Hecho | `notebooks/03_ensemble-techniques.ipynb` |
| Validación cruzada | Hecho | `notebooks/05_cross_validation.ipynb` |
| Optimización de hiperparámetros | Hecho | `notebooks/04_hyperparameter_optimization.ipynb` |
| Feedback para monitorizar performance | Hecho | Vista `Monitorización` |
| Pipeline de ingesta | Hecho | Vista `Pipeline de reentrenamiento` |

### Nivel avanzado

| Requisito | Estado | Evidencia |
|---|---|---|
| Versión dockerizada | Hecho | `Dockerfile`, `.dockerignore`, `requirements-docker.txt` |
| Guardado en base de datos | Hecho | SQLite local y PostgreSQL en Render |
| Despliegue | Hecho | Render Web Service Docker |
| Tests unitarios | Hecho | `tests/` |

## Instalación local

Crear entorno:

```bash
python -m venv .venv
```

Activar en Windows con Git Bash:

```bash
source .venv/Scripts/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar:

```bash
streamlit run app/app.py
```

URL local:

```text
http://localhost:8501
```

## Docker

Build:

```bash
docker build -t flood-risk-app .
```

Run:

```bash
docker run --rm -p 8501:8501 flood-risk-app
```

Run con volumen local:

```bash
docker run --rm -p 8501:8501 -v "$(pwd)/data:/app/data" flood-risk-app
```

El `Dockerfile` usa `PORT` si el entorno lo proporciona. En local usa `8501`.

## Tests

Instalar dependencias de desarrollo:

```bash
pip install -r requirements-dev.txt
```

Ejecutar:

```bash
python -m pytest
```

Tests:

| Test | Objetivo |
|---|---|
| `tests/test_features.py` | Validar feature engineering |
| `tests/test_database.py` | Validar ciclo de base de datos |
| `tests/test_pipeline.py` | Validar filtrado e ingesta del pipeline |

Resultado final:

```text
6 passed
```

## Verificaciones finales

Comandos ejecutados:

```bash
python -m pytest
python -m py_compile app\app.py app\paths.py src\features.py src\database.py src\db_insert.py src\pipeline.py
git diff --check
docker build -t flood-risk-app .
docker run --rm -p 8501:8501 flood-risk-app
```

Checklist:

| Verificación | Resultado |
|---|---|
| Tests unitarios | Correcto |
| Compilación Python | Correcto |
| Revisión de espacios | Correcto |
| Docker build | Correcto |
| Docker run local | Correcto |
| Render deploy | Correcto |
| PostgreSQL conectado | Correcto |
| Monitorización desde PostgreSQL | Correcto |
| Pipeline con salida de cola | Correcto |

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

## Distribución de tareas

| Participante | Bloque principal | Tareas | Evidencia |
|---|---|---|---|
| Participante 1 | Análisis exploratorio | Revisión del dataset, nulos, distribuciones, correlaciones y visualizaciones | `notebooks/01_EDA.ipynb`, `docs/dataset.md` |
| Participante 2 | Modelado baseline | Train/test, baseline, métricas, residuos, predicción vs real y guardado del modelo | `notebooks/02_modeling.ipynb` |
| Participante 3 | Mejora y validación | Ensemble, validación cruzada, hiperparámetros y comparación de modelos | `notebooks/03_ensemble-techniques.ipynb`, `notebooks/04_hyperparameter_optimization.ipynb`, `notebooks/05_cross_validation.ipynb` |
| Participante 4 | Productivización | App, feedback, monitorización, base de datos, pipeline, Docker, Render, tests y README | `app/app.py`, `src/`, `Dockerfile`, `tests/`, `README.md` |

Pendiente administrativo:

- Actualizar Jira con el cierre final.

## Documentación

| Documento | Contenido |
|---|---|
| `README.md` | Documento principal del proyecto |
| `docs/dataset.md` | Información del dataset |
| `docs/dailies/` | Registro de dailies |

El documento narrativo interno del equipo queda fuera de Git:

```text
docs/internal/
```

## Archivos ignorados

No se suben:

- datasets originales descargados de Kaggle,
- CSV generados por uso de la app,
- bases SQLite locales,
- secretos de Streamlit,
- documentación interna en `docs/internal/`.

## Flujo de Git

| Rama | Uso |
|---|---|
| `main` | Versión final estable |
| `dev` | Rama principal de desarrollo |
| ramas de tarea | Cambios por Pull Request |

Flujo final recomendado:

```text
docs/final-readme -> dev -> main
```

Una vez mergeado en `dev`, redeplegar Render con `Deploy latest commit`. Tras validar la URL desplegada, mergear `dev` hacia `main`.
