# Aliases y Productividad en Git

## ¿Qué son los aliases?

Los aliases son atajos para comandos de Git que usas frecuentemente. Se configuran en `~/.gitconfig`.

## Configurar aliases

```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.lg "log --oneline --graph --all --decorate"
```

O editando directamente `~/.gitconfig`:

```ini
[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
    lg = log --oneline --graph --all --decorate
    unstage = reset HEAD --
    last = log -1 HEAD
    visual = !gitk
    amend = commit --amend --no-edit
    wip = !git add -A && git commit -m "wip: trabajo en progreso"
    undo = reset --soft HEAD~1
    branches = branch -a
    tags = tag -l
    contributors = shortlog -sn
```

## Aliases recomendados para principiantes

| Alias | Comando completo | Uso |
|---|---|---|
| `git st` | `git status` | Ver estado rápido |
| `git lg` | `log --oneline --graph --all` | Historial visual |
| `git unstage` | `reset HEAD --` | Quitar archivo de staging |
| `git last` | `log -1 HEAD` | Ver último commit |
| `git amend` | `commit --amend --no-edit` | Agregar al último commit sin cambiar mensaje |
| `git undo` | `reset --soft HEAD~1` | Deshacer último commit conservando cambios |
| `git wip` | `add -A && commit -m "wip..."` | Commit rápido de trabajo en progreso |

## Aliases con shell (prefijo `!`)

Permiten ejecutar comandos de shell, no solo Git:

```bash
# Abrir el repo en el navegador (GitHub)
git config --global alias.open '!gh repo view --web'

# Limpiar ramas ya fusionadas
git config --global alias.cleanup '!git branch --merged | grep -v "main\|develop" | xargs git branch -d'

# Ver tamaño del repo
git config --global alias.size '!git count-objects -vH'
```

## Alias global del sistema operativo (opcional)

En tu `.bashrc` / `.zshrc` / PowerShell profile:

```bash
# Bash/Zsh
alias gs='git status'
alias gl='git log --oneline --graph --all'
alias gp='git push'
alias gpl='git pull'
alias gc='git commit'
alias gco='git checkout'
```

```powershell
# PowerShell
Set-Alias -Name gs -Value git status  # (mejor usar funciones)
function gst { git status }
function glog { git log --oneline --graph --all }
```

## Productividad: comandos que ahorran tiempo

```bash
# Ver cambios de un archivo específico en un commit
git show <hash>:<archivo>

# Buscar en el historial quién modificó una línea
git blame <archivo>

# Buscar un texto en todo el historial
git log -S "texto_buscado" --oneline

# Ver diferencias entre dos ramas
git diff main..feature/login

# Ver archivos cambiados entre dos ramas
git diff --name-only main..feature/login

# Stash rápido con mensaje automático
git stash push -m "wip $(date +%Y%m%d_%H%M)"

# Limpiar archivos untracked (con confirmación)
git clean -n   # dry-run (simula)
git clean -f   # ejecuta
```

## Recomendación

No memorices todo. Empieza con 3-4 aliases que uses a diario y ve agregando. La productividad viene de la repetición, no de la cantidad.