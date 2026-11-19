# Documentación Git — Etapa Bronce

Esta carpeta contiene la documentación de Git para la etapa de bronce del bootcamp de IA.

## Índice de documentos

### Guías (`guias/`)

| Archivo | Tema |
|---|---|
| `01_comandos_fundamentales.md` | Comandos básicos: init, clone, add, commit, diff, log, push, pull, fetch |
| `02_buenas_practicas_ramas.md` | Convención de nombres de ramas, comandos, reglas de oro, merge vs rebase |
| `03_convencion_commits.txt` | Conventional Commits: estructura, tipos, reglas, breaking changes |
| `06_configuracion_inicial_y_gitignore.md` | Configuración inicial de Git, .gitignore, patrones, plantillas |
| `07_ssh_y_autenticacion.md` | HTTPS con PAT, SSH con llaves, múltiples cuentas, troubleshooting |
| `08_tags_y_releases.md` | Tags ligeros/anotados, Semantic Versioning, releases en GitHub |
| `09_flujo_colaborativo_y_pull_requests.md` | Fork, PR, code review, merge strategies, branch protection |
| `10_resolucion_conflictos.md` | Conflictos de merge, resolución paso a paso, rebase interactivo |
| `11_seguridad_y_secretos.md` | Prevención, rotación de secretos, BFG, GPG, buenas prácticas |
| `12_git_stash.md` | Guardar trabajo temporal, stash parcial, buenas prácticas |
| `13_aliases_y_productividad.md` | Aliases, productividad, comandos que ahorran tiempo |

### Matrices (`matrices/`)

| Archivo | Tema |
|---|---|
| `04_recetario_situaciones_git.md` | Recetario de 14 situaciones comunes con comandos exactos |

### Troubleshooting (`troubleshooting/`)

| Archivo | Tema |
|---|---|
| `05_errores_terminales_y_soluciones.csv` | 15 errores comunes con causa, solución y advertencia |

## Ruta de aprendizaje sugerida (bronce)

1. **Configuración** → `06_configuracion_inicial_y_gitignore.md` + `07_ssh_y_autenticacion.md`
2. **Comandos básicos** → `01_comandos_fundamentales.md`
3. **Ramas** → `02_buenas_practicas_ramas.md`
4. **Commits** → `03_convencion_commits.txt`
5. **Colaboración** → `09_flujo_colaborativo_y_pull_requests.md`
6. **Conflictos** → `10_resolucion_conflictos.md`
7. **Stash y tags** → `12_git_stash.md` + `08_tags_y_releases.md`
8. **Seguridad** → `11_seguridad_y_secretos.md`
9. **Productividad** → `13_aliases_y_productividad.md`
10. **Referencia rápida** → `04_recetario_situaciones_git.md` + `05_errores_terminales_y_soluciones.csv`

## Convenciones de la documentación

- Los comandos están en bloques de código bash.
- Las advertencias importantes están marcadas con `> **Advertencia:**`.
- Los archivos CSV usan coma como separador y comillas para campos con comas.
- Todo el contenido está en español neutro/profesional.