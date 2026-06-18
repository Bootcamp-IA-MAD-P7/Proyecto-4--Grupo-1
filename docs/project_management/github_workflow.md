# Flujo de Trabajo con GitHub

![Rama estable](https://img.shields.io/badge/main-estable-0969DA?style=for-the-badge)
![Desarrollo](https://img.shields.io/badge/dev-desarrollo-1A7F37?style=for-the-badge)
![Pull Requests](https://img.shields.io/badge/PR-obligatorio-8250DF?style=for-the-badge)
![Datasets](https://img.shields.io/badge/CSV-no%20subir-9A6700?style=for-the-badge)

## Objetivo

Este documento define cómo trabajará el equipo con GitHub durante el proyecto.

El objetivo es evitar conflictos, mantener una rama estable y asegurar que los cambios importantes sean revisados antes de integrarse.

## Ramas principales

| Rama | Uso | Regla |
|---|---|---|
| `main` | Versión estable del proyecto | No se trabaja directamente aquí |
| `dev` | Rama principal de desarrollo | Recibe los Pull Requests del equipo |
| ramas de tarea | Trabajo individual o por bloque | Siempre nacen desde `dev` |

## Rama `main`

La rama `main` se reserva para versiones estables del proyecto.

No se trabajará directamente sobre `main`. Al final del proyecto, cuando `dev` tenga una versión completa y revisada, se podrá crear un Pull Request de:

```text
dev -> main
```

## Rama `dev`

La rama `dev` es la rama principal de desarrollo del equipo.

Todas las tareas se integrarán primero en `dev` mediante Pull Request.

## Ramas de trabajo

Cada tarea o bloque de trabajo debe realizarse en una rama propia creada desde `dev`.

Formato recomendado:

```text
tipo/descripcion-breve
```

Tipos recomendados:

| Tipo | Uso |
|---|---|
| `docs/` | Documentación |
| `data/` | Dataset, limpieza o EDA |
| `notebook/` | Notebooks |
| `model/` | Modelado y métricas |
| `app/` | Aplicación Streamlit |
| `fix/` | Correcciones |
| `chore/` | Estructura o configuración |

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

Añadir cambios:

```bash
git add archivo-o-carpeta
```

Crear commit:

```bash
git commit -m "tipo: descripción del cambio"
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

## Después de mergear un PR

Después de que un Pull Request se haya mergeado en `dev`, cada integrante debe actualizar su rama local:

```bash
git checkout dev
git pull origin dev
```

Si la rama de trabajo ya no se necesita, puede eliminarse:

```bash
git branch -d nombre-rama
```

Si GitHub no la elimina automáticamente, también puede borrarse del remoto:

```bash
git push origin --delete nombre-rama
```

## Criterio para cerrar una tarea en Jira

Una tarea se puede cerrar cuando:

- El trabajo está terminado.
- El código o documentación está subido a GitHub.
- El Pull Request ha sido revisado.
- El Pull Request ha sido mergeado en `dev`.
- No quedan cambios pendientes relacionados con esa tarea.
