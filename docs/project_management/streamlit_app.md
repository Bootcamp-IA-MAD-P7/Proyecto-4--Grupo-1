# Aplicacion Streamlit

## Objetivo

La aplicacion Streamlit productiviza el modelo de prediccion de inundaciones y permite usarlo sin abrir notebooks.

Archivo principal:

```text
app/app.py
```

## Ejecucion

Desde la raiz del proyecto:

```bash
streamlit run app/app.py
```

## Vistas de la aplicacion

La app se organiza en varias vistas desde la barra lateral.

### Prediccion

Permite calcular el riesgo estimado de inundacion.

Incluye:

- Carga automatica del modelo.
- Sliders para las variables predictoras.
- Explicacion de cada variable mediante ayuda contextual.
- Guia rapida para elegir valores.
- Boton para restablecer valores recomendados.
- Resultado en porcentaje.
- Categoria de riesgo: bajo, medio o alto.
- Guardado de feedback y nuevos datos.

### Monitorizacion

Permite revisar el rendimiento del modelo a partir del feedback guardado:

- Total de predicciones guardadas.
- Predicciones con valor real.
- Predicciones pendientes de valor real.
- Metricas acumuladas cuando hay valores reales: MAE, RMSE y R2 cuando aplica.
- Edicion de valores reales ya guardados.
- Eliminacion de registros con confirmacion explicita.

### Pipeline de reentrenamiento

Prepara los registros nuevos recogidos por la aplicacion para futuros reentrenamientos.

Funcionamiento:

- Cada prediccion se guarda en `data/new_data/nuevos_registros.csv`.
- Si la prediccion no tiene valor real, queda como `pending_target`.
- Si se introduce o se completa el valor real, queda como `validated_for_retraining`.
- Solo los registros con valor real pueden usarse como datos supervisados.
- La vista permite generar `data/processed/retraining_dataset.csv`.

El dataset generado contiene las variables predictoras y usa el valor real observado como `FloodProbability`.

La prediccion del modelo se conserva como referencia, pero no se usa como variable objetivo para reentrenar.

### Informes tecnicos

Muestra los notebooks del proyecto con contexto:

- `01_EDA.ipynb`: analisis exploratorio.
- `02_modeling.ipynb`: modelado, metricas y baseline.

### Datos

Muestra una vista previa del dataset y, si esta disponible, el explorador interactivo PyGWalker.

PyGWalker es opcional. Si no esta instalado, la app sigue funcionando.

## Modelo

Ruta principal esperada:

```text
models/flood_baseline_model.joblib
```

Ruta secundaria admitida:

```text
data/raw/models/flood_baseline_model.joblib
```

Si la app encuentra el modelo en la ruta secundaria, lo copia automaticamente a la ruta principal.

## Dataset

Ruta recomendada:

```text
data/raw/train.csv
```

La app usa los rangos reales del dataset para configurar los sliders de entrada.

## Feedback y reentrenamiento

Cada prediccion genera datos locales:

```text
data/feedback/predicciones.csv
data/new_data/nuevos_registros.csv
data/processed/retraining_dataset.csv
```

`predicciones.csv` sirve para monitorizar predicciones y errores cuando se introduce un valor real.

`nuevos_registros.csv` sirve como base para futuros reentrenamientos.

`retraining_dataset.csv` se genera desde la vista Pipeline de reentrenamiento cuando existen registros con valor real.

Estos archivos estan ignorados por Git.

## Limitaciones

- El resultado es una estimacion estadistica, no una alerta oficial.
- Si el modelo devuelve un valor fuera de 0%-100%, la app lo limita al rango valido y muestra un aviso.
- El modelo baseline puede mejorarse en Nivel Medio con ensembles, validacion cruzada y optimizacion de hiperparametros.
