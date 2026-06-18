# Flujo de Trabajo con GitHub

## Objetivo

Este documento define como trabajara el equipo con GitHub durante el proyecto.

El objetivo es evitar conflictos, mantener una rama estable y asegurar que los cambios importantes sean revisados antes de integrarse.

## Ramas principales

El proyecto utiliza dos ramas principales:

```text
main
dev
```

## Rama `main`

La rama `main` se reserva para versiones estables del proyecto.

No se trabajara directamente sobre `main`.

Al final del proyecto, cuando `dev` tenga una version completa y revisada, se podra crear un Pull Request de:

```text
dev -> main
```

## Rama `dev`

La rama `dev` es la rama principal de desarrollo del equipo.

Todas las tareas se integraran primero en `dev` mediante Pull Request.

## Ramas de trabajo

Cada tarea o bloque de trabajo debe realizarse en una rama propia creada desde `dev`.

Formato recomendado:

```text
tipo/descripcion-breve
```

Tipos recomendados:

```text
docs/      documentacion
data/      dataset, limpieza o EDA
notebook/  notebooks
model/     modelado y metricas
app/       aplicacion Streamlit
fix/       correcciones
chore/     estructura o configuracion
```

Ejemplos:

```text
chore/setup-project-structure
notebook/add-eda
docs/project-documentation
model/baseline-model
app/streamlit-app
```

## Flujo recomendado

Antes de empezar una tarea:

```bash
git checkout dev
git pull origin dev
```

Crear una rama nueva desde `dev`:

```bash
git checkout -b tipo/descripcion-breve
```

Trabajar en los cambios y revisar el estado:

```bash
git status
```

Anadir cambios:

```bash
git add .
```

Crear commit:

```bash
git commit -m "tipo: descripcion del cambio"
```

Subir la rama:

```bash
git push -u origin tipo/descripcion-breve
```

Crear Pull Request en GitHub:

```text
base: dev
compare: tipo/descripcion-breve
```

## Reglas del equipo

- No trabajar directamente sobre `main`.
- Evitar trabajar directamente sobre `dev`.
- Crear una rama por tarea o bloque de trabajo.
- Abrir Pull Request hacia `dev`.
- Revisar el Pull Request antes de hacer merge.
- No subir datasets pesados al repositorio.
- No mezclar cambios no relacionados en el mismo Pull Request.

## Cuando un PR se mergea

Despues de que un Pull Request se haya mergeado en `dev`, cada integrante debe actualizar su rama local:

```bash
git checkout dev
git pull origin dev
```

Si la rama de trabajo ya no se necesita, puede eliminarse:

```bash
git branch -d nombre-rama
```

Si GitHub no la elimina automaticamente, tambien puede borrarse del remoto:

```bash
git push origin --delete nombre-rama
```

## Criterio para cerrar una tarea en Jira

Una tarea se puede cerrar cuando:

- El trabajo esta terminado.
- El codigo o documentacion esta subido a GitHub.
- El Pull Request ha sido revisado.
- El Pull Request ha sido mergeado en `dev`.
- No quedan cambios pendientes relacionados con esa tarea.
