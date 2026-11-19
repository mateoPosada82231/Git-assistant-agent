# Configuración Inicial y .gitignore

## Configuración Inicial de Git (obligatoria antes del primer commit)

Antes de usar Git por primera vez en una máquina, configura tu identidad. Estos datos aparecerán en cada commit.

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

Verifica la configuración aplicada:

```bash
git config --list
git config user.name
git config user.email
```

Configuraciones recomendadas para principiantes:

```bash
# Usar 'main' como nombre de rama por defecto
git config --global init.defaultBranch main

# Mostrar colores en la terminal
git config --global color.ui auto

# Editor por defecto (ejemplo: VS Code)
git config --global core.editor "code --wait"

# Rebase por defecto al hacer pull (historial lineal)
git config --global pull.rebase true

# Push solo la rama actual
git config --global push.default current
```

Niveles de configuración (de mayor a menor prioridad):
- `--local` (solo este repositorio, archivo `.git/config`)
- `--global` (tu usuario, archivo `~/.gitconfig`)
- `--system` (toda la máquina, requiere administrador)

## El archivo .gitignore

`.gitignore` le dice a Git qué archivos o carpetas NO deben rastrearse. Es esencial para no subir archivos generados, dependencias o secretos.

### Crear un .gitignore

Crea un archivo llamado `.gitignore` en la raíz del repositorio:

```bash
touch .gitignore
```

### Patrones comunes

```gitignore
# Dependencias
node_modules/
vendor/
.venv/
__pycache__/

# Archivos de build / compilación
dist/
build/
*.o
*.class
*.exe

# Variables de entorno y secretos
.env
.env.local
*.pem
*.key
secrets/

# Archivos del sistema operativo
.DS_Store
Thumbs.db
desktop.ini

# Archivos de IDE / editores
.vscode/
.idea/
*.swp
*.swo

# Logs
*.log
logs/

# Archivos temporales
tmp/
temp/
*.tmp
```

### Reglas de sintaxis de .gitignore

- `archivo.txt` → ignora ese archivo en cualquier directorio.
- `/archivo.txt` → ignora solo en la raíz.
- `carpeta/` → ignora toda la carpeta.
- `*.log` → ignora todos los archivos con esa extensión.
- `!importante.log` → excepción: NO ignorar este archivo aunque coincida con un patrón anterior.
- `**/logs` → ignora cualquier carpeta `logs` en cualquier nivel.
- `doc/*.txt` → ignora `.txt` solo dentro de `doc/`.

### Ignorar archivos ya rastreados

Si un archivo ya fue commiteado y luego lo agregas a `.gitignore`, Git seguirá rastreándolo. Para dejar de rastrearlo sin borrarlo del disco:

```bash
git rm --cached <archivo>
git commit -m "chore: dejar de rastrear archivo sensible"
```

### Plantillas de .gitignore

GitHub ofrece plantillas oficiales por lenguaje/framework en:
https://github.com/github/gitignore

También puedes generarlas con herramientas como `gitignore.io` o el comando:

```bash
npx gitignore node python
```

## Archivos que NUNCA deben subirse

- Claves privadas (`.pem`, `.key`, `id_rsa`)
- Variables de entorno (`.env`, `.env.local`)
- Credenciales de bases de datos
- Tokens de API
- Archivos de configuración personal (`.vscode/settings.json` con rutas locales)

> **Regla de oro:** Si un secreto ya fue subido a un repositorio público, considéralo comprometido. Rótalo inmediatamente y reescribe el historial con `git filter-repo` o BFG Repo-Cleaner.

## Verificación rápida

```bash
# Ver qué archivos están siendo ignorados y por qué
git check-ignore -v <archivo>

# Ver archivos ignorados en el repositorio
git status --ignored
```