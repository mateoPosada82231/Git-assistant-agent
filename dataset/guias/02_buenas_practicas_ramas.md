# Buenas Prácticas en el Manejo de Ramas (Branches)

## Convención de Nombres de Ramas

Usa nombres descriptivos, en minúsculas y separados por guiones medios (`-`), siguiendo el prefijo según el propósito:

- `main`: Rama principal. Contiene únicamente código estable y listo para producción.
- `develop`: Rama de integración donde se unen las nuevas funcionalidades antes de salir a producción.
- `feature/<descripcion-corta>`: Para nuevas funcionalidades (ejemplo: `feature/login-oauth`).
- `bugfix/<descripcion-corta>`: Para corregir errores detectados durante el desarrollo (ejemplo: `bugfix/error-calculo-iva`).
- `hotfix/<descripcion-corta>`: Para correcciones urgentes directamente sobre producción (ejemplo: `hotfix/caida-pasarela-pagos`).

## Comandos Esenciales de Ramas

- **Crear una rama nueva y moverse a ella inmediatamente:**

  ```bash
  git switch -c feature/nueva-funcionalidad
  ```

  _(Alternativa clásica: `git checkout -b feature/nueva-funcionalidad`)_

- **Cambiar entre ramas existentes:**

  ```bash
  git switch develop
  ```

- **Listar ramas locales y remotas:**

  ```bash
  git branch -a
  ```

- **Eliminar una rama local que ya fue fusionada:**
  ```bash
  git branch -d feature/nueva-funcionalidad
  ```

## Reglas de Oro del Equipo

1. **Nunca hagas `git push` directo a `main`:** Todo cambio hacia `main` debe pasar por un Pull Request (PR) o Merge Request revisado.
2. **Mantén las ramas cortas y enfocadas:** Una rama debe resolver una sola tarea o historia de usuario. Ramas de semanas de duración generan conflictos difíciles de resolver.
3. **Actualiza tu rama antes de abrir un Pull Request:** Trae los últimos cambios de `develop` o `main` hacia tu rama para resolver cualquier conflicto localmente antes de pedir revisión.
4. **Borra las ramas después de fusionarlas:** Mantiene limpio el repositorio y evita confusiones sobre qué tareas siguen activas.

## ¿Cuándo usar `git merge` vs `git rebase`?

- **Usa `git merge`:** Cuando vayas a integrar una rama de funcionalidad (`feature/...`) hacia una rama compartida (`develop` o `main`). Conserva el historial real y el contexto de cuándo ocurrió la unión.
  ```bash
  git switch develop
  git merge feature/login-oauth
  ```
- **Usa `git rebase`:** Para actualizar tu rama personal con los últimos cambios de `develop` manteniendo un historial lineal y limpio, antes de abrir un Pull Request.
  ```bash
  git switch feature/login-oauth
  git rebase develop
  ```
- **Regla estricta del rebase:** Nunca ejecutes `git rebase` sobre ramas públicas o compartidas donde otras personas estén trabajando, ya que reescribe los hashes de los commits y rompe el historial de tus compañeros.
