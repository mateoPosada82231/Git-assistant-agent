# Flujo Colaborativo y Pull Requests

## El flujo básico de colaboración

```
1. Fork / Clone del repositorio
2. Crear una rama de trabajo
3. Hacer cambios y commits
4. Push de la rama al remoto
5. Abrir un Pull Request (PR)
6. Revisión de código (Code Review)
7. Ajustes según feedback
8. Merge del PR
9. Limpiar ramas
```

## Fork vs Clone

- **Clone:** Copia local de un repo al que tienes acceso de escritura (tu propio repo o de tu organización).
- **Fork:** Copia del repo en tu propia cuenta de GitHub. Usado para contribuir a proyectos de terceros.

```bash
# Clonar
git clone https://github.com/usuario/repo.git

# Fork (desde la UI de GitHub) + clonar tu fork
git clone https://github.com/tu_usuario/repo.git

# Agregar el repo original como 'upstream' para sincronizar
git remote add upstream https://github.com/original/repo.git
```

## Sincronizar tu fork con el original

```bash
git fetch upstream
git switch main
git merge upstream/main
git push origin main
```

## Abrir un Pull Request

### Desde la terminal con GitHub CLI

```bash
# Instalar gh: https://cli.github.com
gh pr create --title "feat: agregar login con OAuth" --body "Descripcion del cambio" --base main --head feature/login-oauth
```

### Desde la UI de GitHub

1. Push tu rama: `git push -u origin feature/login-oauth`
2. Ve al repositorio en GitHub → aparecerá un banner "Compare & pull request".
3. Completa título, descripción, reviewers y labels.
4. Crea el PR.

## Buenas prácticas para un buen PR

1. **Título claro** siguiendo Conventional Commits.
2. **Descripción completa:** qué cambió, por qué y cómo probarlo.
3. **PRs pequeños y enfocados:** idealmente < 400 líneas cambiadas.
4. **Un PR = una tarea:** no mezcles funcionalidades no relacionadas.
5. **Incluye tests** y actualiza documentación si aplica.
6. **Self-review antes de pedir revisión:** revisa tu propio diff.
7. **Responde al feedback** con commits adicionales o comentarios.

### Plantilla de PR (crear `.github/pull_request_template.md`)

```markdown
## Descripción
[Qué cambió y por qué]

## Tipo de cambio
- [ ] Bug fix
- [ ] Nueva funcionalidad
- [ ] Breaking change
- [ ] Documentación

## ¿Cómo probar?
[Pasos para verificar el cambio]

## Checklist
- [ ] Mi código sigue las convenciones del proyecto
- [ ] Agregué tests que cubren mi cambio
- [ ] Actualicé la documentación
- [ ] No hay warnings nuevos
```

## Code Review: buenas prácticas

### Como autor del PR
- Responde a todos los comentarios (resuelve o explica).
- No tomes el feedback de forma personal.
- Marca conversaciones como resueltas solo cuando se atiendan.

### Como reviewer
- Sé específico y constructivo.
- Distingue entre "bloqueante" (debe cambiar) y "sugerencia" (opcional).
- Usa prefijos: `nit:`, `suggestion:`, `question:`, `blocking:`.
- Aprueba cuando el cambio es correcto, aunque tengas sugerencias menores.

## Merge strategies

- **Merge commit:** Conserva todos los commits y crea un commit de merge. Historial completo.
- **Squash and merge:** Combina todos los commits del PR en uno solo. Historial lineal y limpio. **Recomendado para feature branches.**
- **Rebase and merge:** Reaplica los commits sobre la rama base sin commit de merge. Historial lineal preservando commits individuales.

### Configurar en GitHub
Settings → General → Pull Requests → elige la estrategia por defecto.

## Protección de ramas (Branch Protection)

Configura en GitHub: Settings → Branches → Add rule para `main`:

- Require a pull request before merging
- Require approvals (mínimo 1)
- Require status checks to pass (CI/CD)
- Require branches to be up to date
- Do not allow bypassing the above settings
- (Opcional) Require signed commits

## Limpiar después del merge

```bash
# Borrar rama local
git branch -d feature/login-oauth

# Borrar rama remota
git push origin --delete feature/login-oauth

# Limpiar referencias remotas obsoletas
git fetch --prune
```

## Flujo de trabajo para equipos: GitHub Flow (recomendado para bronce)

1. `main` siempre está listo para producción.
2. Crea una rama desde `main` para cada cambio.
3. Haz commits y push a tu rama.
4. Abre un PR hacia `main`.
5. Revisa, ajusta y mergea.
6. Despliega desde `main`.

> **Git Flow** (con `develop`, `release`, `hotfix`) es más complejo; resérvalo para proyectos con ciclos de release formales. Para la etapa bronce, GitHub Flow es suficiente.