# Resolución de Conflictos de Merge

## ¿Qué es un conflicto?

Un conflicto ocurre cuando dos ramas modificaron las mismas líneas de un archivo (o archivos adyacentes) de forma incompatible, y Git no puede fusionarlos automáticamente.

## Cómo se ve un conflicto

Al hacer `git merge` o `git pull`, Git detiene el proceso y marca el archivo:

```text
<<<<<<< HEAD
codigo de tu rama actual
=======
codigo de la rama que estas fusionando
>>>>>>> feature/otra-rama
```

- `<<<<<<< HEAD`: inicio del conflicto, tu versión.
- `=======`: separador entre las dos versiones.
- `>>>>>>> feature/otra-rama`: fin del conflicto, versión entrante.

## Flujo de resolución paso a paso

### 1. Identificar los archivos en conflicto

```bash
git status
# Busca "both modified" o "Unmerged paths"
```

### 2. Abrir el archivo y resolver

Edita el archivo manualmente: decide qué código conservar, combina ambas versiones o escribe una nueva. **Elimina todos los marcadores** (`<<<<<<<`, `=======`, `>>>>>>>`).

### 3. Marcar como resuelto (staging)

```bash
git add <archivo_resuelto>
```

### 4. Completar el merge

```bash
git commit   # Git abrirá el editor con un mensaje de merge por defecto
# o
git commit -m "merge: resolver conflicto en modulo de pagos"
```

### 5. Si usas rebase en lugar de merge

```bash
# Durante un rebase con conflicto:
# 1. Resuelve el archivo
# 2. git add <archivo>
# 3. Continúa el rebase
git rebase --continue

# Si quieres abortar y volver al estado anterior
git rebase --abort
```

## Herramientas para resolver conflictos

### Usar un merge tool visual

```bash
# Configurar VS Code como merge tool
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd 'code --wait $MERGED'

# Abrir el merge tool
git mergetool
```

Otras herramientas: Meld, KDiff3, Beyond Compare, IntelliJ.

### Resolver con "ours" o "theirs" (cuando quieres quedarte con una versión completa)

```bash
# Quedarse con TU versión (HEAD)
git checkout --ours <archivo>
git add <archivo>

# Quedarse con LA OTRA versión
git checkout --theirs <archivo>
git add <archivo>
```

> **Cuidado:** Esto descarta la otra versión por completo. Úsalo solo cuando tengas certeza.

## Conflictos en archivos binarios

Git no puede fusionar binarios (imágenes, PDFs). Debes elegir una versión:

```bash
git checkout --ours imagen.png   # tu versión
# o
git checkout --theirs imagen.png  # la otra versión
git add imagen.png
```

## Prevenir conflictos

1. **Ramas cortas y enfocadas:** menos tiempo = menos divergencia.
2. **Pull frecuente:** `git pull --rebase` antes de empezar a trabajar.
3. **Comunicación:** avisa al equipo qué archivos estás tocando.
4. **Evita reformatear archivos enteros** sin coordinación (genera conflictos masivos).
5. **Un commit = un cambio lógico:** facilita la revisión y el merge.

## Conflictos comunes y su causa

| Situación | Causa | Solución |
|---|---|---|
| Conflicto en `package-lock.json` | Ambas ramas actualizaron dependencias | Regenera con `npm install` y commitea el resultado |
| Conflicto en migraciones de BD | Dos migraciones con el mismo timestamp | Renombra una y actualiza el orden |
| Conflicto en `.env.example` | Ambos agregaron variables | Combina ambas listas |
| Conflictos masivos en todo el repo | Rama muy desactualizada | Considera `git merge --squash` o rebase interactivo |

## Rebase interactivo para limpiar historial antes de PR

```bash
# Reescribir los últimos 3 commits
git rebase -i HEAD~3
```

En el editor puedes:
- `pick`: mantener el commit.
- `reword`: cambiar el mensaje.
- `squash`: fusionar con el anterior.
- `fixup`: fusionar descartando el mensaje.
- `drop`: eliminar el commit.

> **Regla estricta:** No reescribas commits ya publicados en ramas compartidas.

## Abortar un merge/rebase

```bash
# Abortar merge en progreso
git merge --abort

# Abortar rebase en progreso
git rebase --abort
```

Esto devuelve el repositorio al estado anterior al intento de fusión.