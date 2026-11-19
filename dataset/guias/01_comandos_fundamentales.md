# Comandos Fundamentales de Git

## Inicialización y Clonación

- **Iniciar un repositorio local nuevo:**

  ```bash
  git init
  ```

  Crea la carpeta oculta `.git` en el directorio actual para comenzar el seguimiento de versiones.

- **Clonar un repositorio remoto existente:**
  ```bash
  git clone <url_del_repositorio>
  ```
  Descarga el proyecto completo junto con todo su historial de commits y configura el remoto `origin`.

## Ciclo Básico de Trabajo (Working Directory -> Staging -> Repositorio)

- **Revisar el estado de los archivos:**

  ```bash
  git status
  ```

  Muestra archivos modificados, archivos nuevos sin seguimiento (_untracked_) y archivos listos en el área de preparación (_staging area_).

- **Agregar archivos al área de preparación (Staging):**

  ```bash
  git add <nombre_archivo>
  git add .
  ```

  Usa `git add <archivo>` para incluir cambios específicos o `git add .` para preparar todos los cambios del directorio actual.

- **Guardar cambios en el historial (Commit):**
  ```bash
  git commit -m "feat: agregar validacion de usuario"
  ```
  Crea una instantánea permanente de los archivos que están en _staging_. Siempre debe incluir un mensaje descriptivo con la flag `-m`.

## Inspección del Historial y Diferencias

- **Ver cambios aún no agregados a staging:**
  ```bash
  git diff
  ```
- **Ver cambios que ya están en staging listos para commit:**
  ```bash
  git diff --staged
  ```
- **Consultar el historial de commits resumido:**
  ```bash
  git log --oneline --graph --all
  ```
  Muestra cada commit en una sola línea junto con el árbol visual de ramas y fusiones.

## Sincronización con Repositorios Remotos

- **Descargar información del remoto sin modificar tu código local:**

  ```bash
  git fetch origin
  ```

  Actualiza las referencias remotas para saber si hay cambios nuevos antes de integrarlos.

- **Descargar e integrar cambios de la rama remota actual:**

  ```bash
  git pull origin <nombre_rama>
  ```

  Equivale a ejecutar `git fetch` seguido de `git merge`.

- **Subir tus commits locales al repositorio remoto:**
  ```bash
  git push -u origin <nombre_rama>
  ```
  ## Configuración y Utilidades

- **Configurar identidad (obligatorio antes del primer commit):**
  ```bash
  git config --global user.name "Tu Nombre"
  git config --global user.email "tu@email.com"
  ```

- **Ver configuración actual:**
  ```bash
  git config --list
  ```

- **Descartar cambios en un archivo (volver al último commit):**
  ```bash
  git restore <nombre_archivo>
  ```

- **Quitar un archivo del staging (sin borrar cambios):**
  ```bash
  git restore --staged <nombre_archivo>
  ```

- **Guardar cambios temporalmente (stash):**
  ```bash
  git stash push -m "descripcion del trabajo"
  git stash pop
  ```

- **Ver quién modificó cada línea:**
  ```bash
  git blame <nombre_archivo>
  ```

- **Crear un tag anotado (release):**
  ```bash
  git tag -a v1.0.0 -m "Primera release estable"
  git push origin v1.0.0
  ```

- **Limpiar archivos untracked (simular primero):**
  ```bash
  git clean -n -d   # dry-run
  git clean -fd     # ejecutar
  ```

- **Ver ramas remotas y locales:**
  ```bash
  git branch -a
  ```

- **Eliminar rama local fusionada:**
  ```bash
  git branch -d feature/nueva-funcionalidad
  ```

- **Eliminar referencia a ramas remotas borradas:**
  ```bash
  git fetch --prune
  ```
