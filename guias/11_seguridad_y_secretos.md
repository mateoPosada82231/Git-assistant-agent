# Seguridad y Manejo de Secretos

## Por qué es crítico

Subir un secreto (token, contraseña, clave privada) a un repositorio, incluso privado, es un riesgo grave. Una vez en el historial, persiste aunque lo borres en un commit posterior.

## Prevención (lo más importante)

### 1. .gitignore desde el inicio

Antes del primer commit, asegúrate de tener `.gitignore` con:

```gitignore
.env
.env.*
*.pem
*.key
*.p12
secrets/
config/secrets.yml
```

### 2. Variables de entorno

Nunca hardcodees secretos en el código. Usa variables de entorno:

```bash
# .env (ignorado por git)
DATABASE_URL=postgres://user:pass@host/db
API_KEY=sk-abc123
```

```python
# codigo
import os
api_key = os.environ.get("API_KEY")
```

Proporciona un `.env.example` (sin valores reales) para que otros sepan qué variables configurar:

```bash
# .env.example (este SÍ se commitea)
DATABASE_URL=
API_KEY=
```

### 3. Herramientas de escaneo preventivo

Instala hooks o herramientas que detectan secretos antes del commit:

```bash
# git-secrets (AWS)
git secrets --install
git secrets --register-aws

# gitleaks (general)
gitleaks detect --source . --verbose

# truffleHog
trufflehog git file://. --only-verified
```

### 4. Pre-commit hooks

Crea `.git/hooks/pre-commit` (o usa `pre-commit` framework):

```bash
#!/bin/sh
# Bloquear commits que contengan patrones de secretos
if git diff --cached | grep -E "(API_KEY|PASSWORD|SECRET)" ; then
  echo "ERROR: posible secreto detectado. Revisa el diff."
  exit 1
fi
```

## Si ya subiste un secreto: plan de acción

### Paso 1: Rotar el secreto INMEDIATAMENTE

El secreto ya está comprometido. Genera uno nuevo en el proveedor (GitHub, AWS, base de datos, etc.) y revoca el anterior. **No esperes.**

### Paso 2: Eliminar del historial

Opción A — BFG Repo-Cleaner (más simple):

```bash
# Instalar: https://rtyley.github.io/bfg-repo-cleaner/
java -jar bfg.jar --delete-files .env
java -jar bfg.jar --replace-text passwords.txt
cd repo
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

Opción B — git filter-repo (recomendado por Git):

```bash
pip install git-filter-repo
git filter-repo --path .env --invert-paths
# o reemplazar texto
git filter-repo --replace-text <(echo 'secreto_antiguo==>***REMOVED***')
```

### Paso 3: Forzar push (con precaución)

```bash
git push origin --force --all
git push origin --force --tags
```

> **Advertencia:** Reescribir historial en repos compartidos rompe el trabajo de otros. Coordina con el equipo y avisa antes.

### Paso 4: Verificar

```bash
# Buscar el secreto en todo el historial
git log -p -S "secreto_comprometido" --all
```

## Firmar commits (GPG)

La firma GPG verifica que el commit fue hecho por quien dice serlo.

### Configurar GPG

```bash
# Generar llave GPG
gpg --full-generate-key

# Listar llaves
gpg --list-secret-keys --keyid-format=long

# Configurar Git para firmar
git config --global user.signingkey <KEY_ID>
git config --global commit.gpgsign true
```

### Agregar la llave pública a GitHub

```bash
gpg --armor --export <KEY_ID>
# Copia la salida y agrégala en GitHub → Settings → SSH and GPG keys
```

### Verificar firma

```bash
git log --show-signature -1
git verify-commit HEAD
```

## Buenas prácticas de seguridad

1. **Principio de mínimo privilegio:** da solo los permisos necesarios a tokens y colaboradores.
2. **Rota secretos periódicamente** (cada 90 días o ante sospecha).
3. **Usa gestores de secretos** en producción (AWS Secrets Manager, HashiCorp Vault, GitHub Secrets para CI).
4. **Revisa dependencias** con `npm audit`, `pip-audit`, `dependabot`.
5. **Habilita 2FA** en tu cuenta de GitHub/GitLab.
6. **Protege la rama `main`** con branch protection rules.
7. **No guardes secretos en issues, PRs ni comentarios.**
8. **Audita el acceso** a repositorios privados periódicamente.