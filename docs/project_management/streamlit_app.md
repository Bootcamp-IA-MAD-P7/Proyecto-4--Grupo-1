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

La app se organiza en tres vistas desde la barra lateral.

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
```

`predicciones.csv` sirve para monitorizar predicciones y errores cuando se introduce un valor real.

`nuevos_registros.csv` sirve como base para futuros reentrenamientos.

Ambos archivos estan ignorados por Git.

## Limitaciones

- El resultado es una estimacion estadistica, no una alerta oficial.
- Si el modelo devuelve un valor fuera de 0%-100%, la app lo limita al rango valido y muestra un aviso.
- El modelo baseline puede mejorarse en Nivel Medio con ensembles, validacion cruzada y optimizacion de hiperparametros.
