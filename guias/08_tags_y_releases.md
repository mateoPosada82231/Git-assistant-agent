# Tags y Releases

## ¿Qué es un tag?

Un **tag** (etiqueta) es un puntero inmutable a un commit específico, usado para marcar versiones importantes (releases, hitos). A diferencia de las ramas, los tags no se mueven.

## Tipos de tags

- **Lightweight (ligero):** Solo un puntero al commit, sin metadata.
- **Annotated (anotado):** Objeto completo con autor, fecha, mensaje y firma. **Recomendado para releases.**

## Crear tags

### Tag ligero

```bash
git tag v1.0.0
```

### Tag anotado (recomendado)

```bash
git tag -a v1.0.0 -m "Release version 1.0.0: primera version estable"
```

### Tag sobre un commit específico (no el actual)

```bash
git tag -a v0.9.0 <hash_commit> -m "Version beta"
```

## Listar y consultar tags

```bash
# Listar todos los tags
git tag

# Filtrar por patrón
git tag -l "v1.*"

# Ver detalles de un tag anotado
git show v1.0.0

# Ver el commit al que apunta un tag
git rev-list -n 1 v1.0.0
```

## Subir tags al remoto

Por defecto, `git push` NO sube tags. Debes hacerlo explícitamente:

```bash
# Subir un tag específico
git push origin v1.0.0

# Subir todos los tags
git push origin --tags

# Subir tags y commits juntos
git push origin main --follow-tags
```

## Eliminar tags

```bash
# Eliminar tag local
git tag -d v1.0.0

# Eliminar tag remoto
git push origin --delete v1.0.0
# o
git push origin :refs/tags/v1.0.0
```

## Checkout de un tag (estado detached HEAD)

```bash
git checkout v1.0.0
```

> **Advertencia:** Esto te deja en "detached HEAD". Si quieres modificar código, crea una rama: `git switch -c fix-desde-v1.0.0`.

## Semantic Versioning (SemVer)

Formato estándar: `MAJOR.MINOR.PATCH`

- **MAJOR** (1.x.x): Cambios incompatibles (breaking changes).
- **MINOR** (x.1.x): Nuevas funcionalidades compatibles hacia atrás.
- **PATCH** (x.x.1): Correcciones de bugs compatibles.

Ejemplos:
- `v1.0.0` → Primera release estable.
- `v1.1.0` → Nueva funcionalidad sin romper compatibilidad.
- `v1.1.1` → Fix de bug.
- `v2.0.0` → Cambio incompatible (breaking change).

Sufijos opcionales: `v1.0.0-rc.1`, `v1.0.0-beta`, `v1.0.0-alpha`.

## Crear un Release en GitHub

1. Ve a tu repositorio en GitHub → Releases → "Draft a new release".
2. Selecciona o crea el tag (ej. `v1.0.0`).
3. Escribe el título y las notas de la release (changelog).
4. Adjunta binarios si aplica (ej. `.zip`, `.exe`).
5. Publica.

### Automatizar releases con GitHub CLI

```bash
# Instalar gh: https://cli.github.com
gh release create v1.0.0 --title "v1.0.0" --notes "Primera release estable"
```

## Buenas prácticas con tags

1. Usa siempre tags **anotados** para releases públicas.
2. Sigue **Semantic Versioning** de forma consistente.
3. Escribe notas de release claras (qué cambió, qué se arregló, breaking changes).
4. No reutilices un tag ya publicado; crea uno nuevo.
5. Prefija con `v` (ej. `v1.2.3`) por convención.
6. Automatiza la generación del changelog cuando sea posible.