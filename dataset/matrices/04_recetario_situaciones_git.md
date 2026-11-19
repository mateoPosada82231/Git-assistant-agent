# Recetario de Situaciones Comunes en Git

## Situación 1: Hice un commit en `main` por error y debía ir en una rama nueva

- **Diagnóstico:** El commit quedó registrado en la rama equivocada, pero aún no se ha subido a remoto (o necesitas moverlo a una rama de trabajo).
- **Comandos exactos:**

  ```bash
  # 1. Crea la nueva rama apuntando al commit actual (sin cambiar de rama aun)
  git branch feature/mi-cambio

  # 2. Retrocede main al commit anterior manteniendo tus archivos intactos
  git reset --hard HEAD~1

  # 3. Muevete a la nueva rama donde si quedo guardado tu commit
  git switch feature/mi-cambio
  ```

- **Advertencia:** Ejecuta `git reset --hard` solo si estás seguro de que ya creaste la nueva rama en el paso 1 y no has subido ese commit a `origin/main`.

## Situación 2: Necesito cambiar de rama urgente, pero tengo cambios sin terminar

- **Diagnóstico:** Git no te permite cambiar de rama porque tus modificaciones locales entrarían en conflicto con la rama destino, y aún no están listas para un commit.
- **Comandos exactos:**

  ```bash
  # 1. Guarda temporalmente tus cambios modificados y en staging
  git stash push -m "trabajo en progreso formulario"

  # 2. Cambia a la rama urgente
  git switch hotfix/error-produccion

  # 3. Cuando regreses a tu rama original, recupera tus cambios
  git switch feature/formulario
  git stash pop
  ```

## Situación 3: Me equivoqué en el mensaje del último commit o olvidé incluir un archivo

- **Diagnóstico:** El último commit es correcto en esencia, pero le falta un archivo o tiene un error tipográfico en el mensaje.
- **Comandos exactos:**

  ```bash
  # Si olvidaste un archivo, agregalo primero:
  git add archivo_olvidado.py

  # Modifica el ultimo commit sin crear uno nuevo:
  git commit --amend -m "fix(login): corregir validacion de contrasena"
  ```

- **Advertencia:** No uses `--amend` si ese commit ya fue subido a una rama compartida con otros desarrolladores.

## Situación 4: Quiero deshacer el último commit pero conservar el código para editarlo

- **Diagnóstico:** Hiciste commit demasiado pronto y quieres volver a tener esos cambios en el área de preparación (_staging_).
- **Comandos exactos:**
  ```bash
  git reset --soft HEAD~1
  ```
  _(Si quieres que los archivos queden modificados pero fuera de staging, usa `git reset --mixed HEAD~1`)_

## Situación 5: Necesito deshacer un commit que ya fue subido a una rama compartida (`main` o `develop`)

- **Diagnóstico:** No puedes borrar el historial con `reset` porque otros ya descargaron ese commit. Debes crear un commit nuevo que invierta los cambios.
- **Comandos exactos:**

  ```bash
  # 1. Identifica el hash del commit problemático
  git log --oneline -n 5

  # 2. Crea un commit inverso seguro
  git revert <hash_del_commit>
  git push origin main
  ```

## Situación 6: Borré una rama por error o perdí commits después de un `reset --hard`

- **Diagnóstico:** Git conserva un registro interno de todos los movimientos del puntero `HEAD` durante al menos 30 días.
- **Comandos exactos:**

  ```bash
  # 1. Consulta el historial de movimientos de HEAD
  git reflog

  # 2. Identifica el hash justo antes del error (ej. HEAD@{2}) y restaura
  git switch -c rama-recuperada <hash_encontrado>
  ```

## Situación 8: Quiero aplicar un commit específico de otra rama a mi rama actual

- **Diagnóstico:** Necesitas un fix o feature que ya existe en otra rama, pero no quieres fusionar toda la rama.
- **Comandos exactos:**

  ```bash
  # 1. Identifica el hash del commit deseado
  git log --oneline feature/otra-rama -n 5

  # 2. Aplica ese commit en tu rama actual
  git cherry-pick <hash_del_commit>
  ```

- **Advertencia:** Si hay conflictos, resuélvelos y ejecuta `git cherry-pick --continue`. Para abortar: `git cherry-pick --abort`.

## Situación 9: Quiero encontrar qué commit introdujo un bug (bisect)

- **Diagnóstico:** Sabes que hace 2 semanas todo funcionaba, pero ahora hay un bug. Quieres encontrar el commit exacto que lo causó.
- **Comandos exactos:**

  ```bash
  # 1. Inicia el bisect
  git bisect start

  # 2. Marca el commit actual como malo
  git bisect bad

  # 3. Marca un commit antiguo como bueno (donde funcionaba)
  git bisect good <hash_commit_bueno>

  # 4. Git hace checkout a un commit intermedio. Prueba y marca:
  git bisect good   # si funciona
  git bisect bad    # si falla

  # Repite hasta que Git identifique el commit culpable.

  # 5. Finaliza
  git bisect reset
  ```

- **Tip:** Puedes automatizar con un script de prueba:
  ```bash
  git bisect run npm test
  ```

## Situación 10: Hice push de un commit con un mensaje incorrecto y ya está en remoto

- **Diagnóstico:** El commit ya fue subido y otras personas pueden haberlo descargado. No puedes usar --amend de forma segura.
- **Comandos exactos:**

  ```bash
  # Opcion segura: crea un commit nuevo que corrige
  git revert <hash_del_commit>
  git push origin main

  # Si eres el unico que trabajo en esa rama y nadie la descargo:
  git commit --amend -m "mensaje corregido"
  git push --force-with-lease origin <rama>
  ```

- **Advertencia:** `--force-with-lease` es más seguro que `--force` porque falla si alguien más subió cambios.

## Situación 11: Quiero ver quién modificó cada línea de un archivo

- **Diagnóstico:** Necesitas saber quién escribió o modificó una línea específica para entender el contexto.
- **Comandos exactos:**

  ```bash
  git blame <archivo>
  git blame -L 10,25 <archivo>   # solo líneas 10 a 25
  ```

## Situación 12: Tengo cambios en staging y quiero moverlos a otra rama sin commitear

- **Diagnóstico:** Preparaste archivos en staging pero te diste cuenta de que deberían ir en otra rama.
- **Comandos exactos:**

  ```bash
  # 1. Guarda los cambios en staging
  git stash push --staged -m "cambios para otra rama"

  # 2. Cambia a la rama destino
  git switch feature/destino

  # 3. Recupera los cambios
  git stash pop
  ```

## Situación 13: Quiero limpiar archivos untracked y carpetas vacías

- **Diagnóstico:** Tienes archivos sin seguimiento que quieres eliminar (ej. archivos generados por error).
- **Comandos exactos:**

  ```bash
  # Simular primero (dry-run)
  git clean -n -d

  # Eliminar archivos untracked
  git clean -f

  # Eliminar archivos untracked y carpetas vacías
  git clean -fd

  # Eliminar también archivos ignorados (cuidado)
  git clean -fdx
  ```

- **Advertencia:** `git clean` es irreversible. Usa siempre `-n` primero para verificar.

## Situación 14: Quiero comparar dos ramas y ver qué archivos difieren

- **Diagnóstico:** Antes de hacer merge, quieres revisar qué cambió entre ramas.
- **Comandos exactos:**

  ```bash
  # Ver archivos que difieren
  git diff --name-status main..feature/login

  # Ver estadísticas de cambios
  git diff --stat main..feature/login

  # Ver diff completo
  git diff main..feature/login
  ```
