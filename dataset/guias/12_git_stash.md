# Git Stash: Guardar Trabajo Temporal

## ¿Qué es stash?

`git stash` guarda temporalmente tus cambios (modificados y en staging) sin commitearlos, dejando tu working directory limpio. Ideal para cambiar de contexto rápidamente.

## Comandos básicos

```bash
# Guardar cambios con mensaje descriptivo
git stash push -m "trabajo en progreso: formulario de login"

# Guardar incluyendo archivos untracked
git stash push -u -m "incluye archivos nuevos"

# Listar stashes guardados
git stash list
# stash@{0}: On feature/login: trabajo en progreso...
# stash@{1}: On main: experimento...

# Recuperar el último stash (y eliminarlo de la lista)
git stash pop

# Recuperar un stash específico sin eliminarlo
git stash apply stash@{1}

# Eliminar un stash
git stash drop stash@{0}

# Eliminar todos los stashes
git stash clear
```

## Ver contenido de un stash

```bash
# Ver diff del stash
git stash show -p stash@{0}

# Ver archivos afectados
git stash show stash@{0}
```

## Crear una rama desde un stash

Útil si el stash creció demasiado:

```bash
git stash branch feature/nueva-rama stash@{0}
```

Esto crea una rama nueva, aplica el stash y lo elimina de la lista si no hay conflictos.

## Stash parcial (solo algunos archivos)

```bash
# Guardar solo archivos específicos
git stash push -m "solo css" -- src/styles.css

# Guardar interactivamente (elegir hunks)
git stash push -p
```

## Buenas prácticas

1. **Siempre usa `-m`** con un mensaje descriptivo; `stash@{0}` sin contexto es inútil.
2. **No abuses del stash:** si el trabajo lleva más de un día, haz un commit en una rama (puede ser `wip:`).
3. **Limpia stashes viejos** regularmente con `git stash list` y `git stash drop`.
4. **Prefiere ramas** sobre stash para trabajo que no esté listo: `git switch -c wip/mi-trabajo`.

## Cuándo usar stash vs commit en rama

| Situación | Usa |
|---|---|
| Cambio rápido de contexto (< 1 hora) | `git stash` |
| Trabajo que retomarás mañana | Commit en rama `wip/` |
| Experimento que puede descartarse | `git stash` o rama desechable |
| Necesitas compartir el trabajo | Commit + push en rama |