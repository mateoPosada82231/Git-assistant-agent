# SSH y Autenticación con Repositorios Remotos

## Por qué necesitas autenticación

Para `git push`, `git pull` o `git clone` de repositorios privados, Git necesita verificar tu identidad. Hay dos métodos principales: **HTTPS con Token** y **SSH con llaves**.

## Método 1: HTTPS con Personal Access Token (PAT)

Más simple para principiantes. GitHub ya no acepta contraseñas; usa un token.

### Crear un PAT en GitHub

1. Ve a GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic).
2. Genera un nuevo token con scopes: `repo`, `read:org` (según necesidad).
3. Copia el token (solo se muestra una vez).

### Usar el token

```bash
git clone https://github.com/usuario/repo.git
# Username: tu_usuario
# Password: <pega_tu_token>
```

### Guardar credenciales (para no ingresarlas cada vez)

```bash
# Guardar en memoria por 15 minutos
git config --global credential.helper cache

# Guardar permanentemente en el sistema operativo
git config --global credential.helper store   # Linux/macOS (archivo plano)
git config --global credential.helper manager # Windows (Credential Manager)
```

> **Advertencia:** `store` guarda el token en texto plano en `~/.git-credentials`. Úsalo solo en máquinas personales.

## Método 2: SSH con llaves (recomendado)

Más seguro y cómodo a largo plazo. No requiere ingresar credenciales.

### 1. Generar un par de llaves SSH

```bash
ssh-keygen -t ed25519 -C "tu@email.com"
```

- Presiona Enter para aceptar la ruta por defecto (`~/.ssh/id_ed25519`).
- Opcional: ingresa una passphrase para mayor seguridad.

### 2. Iniciar el agente SSH y agregar la llave privada

```bash
# Linux / macOS
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Windows (PowerShell)
Start-Service ssh-agent
ssh-add $env:USERPROFILE\.ssh\id_ed25519
```

### 3. Copiar la llave pública

```bash
# Linux / macOS
cat ~/.ssh/id_ed25519.pub

# Windows (PowerShell)
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub
```

### 4. Agregar la llave pública a GitHub

1. Ve a GitHub → Settings → SSH and GPG keys → New SSH key.
2. Pega el contenido de la llave pública.
3. Guarda.

### 5. Probar la conexión

```bash
ssh -T git@github.com
# Respuesta esperada: "Hi usuario! You've successfully authenticated..."
```

### 6. Usar URLs SSH en tus repositorios

```bash
# Clonar con SSH
git clone git@github.com:usuario/repo.git

# Cambiar un remoto existente de HTTPS a SSH
git remote set-url origin git@github.com:usuario/repo.git
```

## Verificar y gestionar remotos

```bash
# Ver remotos configurados
git remote -v

# Agregar un remoto
git remote add origin <url>

# Cambiar URL de un remoto
git remote set-url origin <nueva_url>

# Eliminar un remoto
git remote remove upstream
```

## Trabajar con múltiples cuentas (personal y trabajo)

Si usas dos cuentas de GitHub, configura llaves separadas y un archivo `~/.ssh/config`:

```ssh-config
# Cuenta personal
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_personal

# Cuenta de trabajo
Host github-work
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_work
```

Luego clona con el alias:

```bash
git clone git@github-work:empresa/repo.git
```

## Solución a problemas comunes de SSH

| Problema | Solución |
|---|---|
| `Permission denied (publickey)` | Verifica que la llave esté agregada al agente (`ssh-add -l`) y que la pública esté en GitHub. |
| `Could not resolve hostname` | Revisa tu conexión a internet o el archivo `~/.ssh/config`. |
| `Bad permissions` | Corrige permisos: `chmod 600 ~/.ssh/id_ed25519` y `chmod 644 ~/.ssh/id_ed25519.pub`. |
| Agente no inicia en Windows | Ejecuta `Get-Service ssh-agent` y `Set-Service -Name ssh-agent -StartupType Automatic`. |

## Seguridad de llaves

- Nunca compartas tu llave **privada** (`id_ed25519` sin `.pub`).
- Usa passphrase en la llave privada.
- Rota las llaves periódicamente (cada 1-2 años o si sospechas compromiso).
- Revoca llaves antiguas desde GitHub → Settings → SSH and GPG keys.