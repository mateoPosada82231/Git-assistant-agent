# Git Assistant Agent

Asistente basado en RAG (Retrieval-Augmented Generation) que responde preguntas sobre Git usando un dataset propio de documentación, desplegado sobre Databricks con Unity Catalog, Delta Lake, Vector Search y MLflow.

El proyecto recorre el ciclo completo: ingesta de documentos, pipeline Medallion (Bronze → Silver → Gold), indexación vectorial, funciones de Unity Catalog y agente tool-calling registrado y desplegable.

---

## Arquitectura

```
Volumen UC (dataset)
        │
        ▼
1.1A Bronze  →  bronze_docs_raw        (binario + ingestion_time)
        │
        ▼
1.1B Silver  →  silver_docs_parsed     (texto plano; CSV → markdown)
        │
        ▼
1.1C Gold    →  gold_docs_chunked      (chunks + id)
        │
        ▼
1.2 Vector Search  →  git_vs_index     (Delta Sync Index + embeddings)
        │
        ▼
2.3 UC Functions  →  search_git_docs, get_current_user, build_reference
        │
        ▼
2.4 Agente tool-calling  →  git_agent  (MLflow + UC + Vector Search)
```

Infraestructura común: `Includes/Lab_Setup.ipynb` define `ProjectSetup`, que fija catálogo, schema, volumen del dataset, `_cache` y `_checkpoint`.

---

## Estructura del repositorio

```
.
├── Includes/
│   └── Lab_Setup.ipynb              # Configuración común (catálogo, schema, volúmenes)
├── 1- RAG/
│   ├── 1.1A- Data Prep (Bronze).py
│   ├── 1.1B- Data Prep (Silver).py
│   ├── 1.1C- Data Prep (Gold).py
│   └── 1.2- Creating Vector Search.py
├── 2- AI Agents/
│   ├── 2.3- Agents with UC Functions.py
│   └── 2.4- driver (git_agent).py
├── 3- Gen AI Evaluation/
│   └── 3.1- Evaluation Techniques.py
├── dataset/                         # Base de conocimiento (documentación Git)
├── BITACORA.md                      # Bitácora del proyecto
└── README.md
```

---

## Dataset

El dataset vive en el volumen:

```
/Volumes/workspace/git-assistnat-agent/dataset
```

| Carpeta | Contenido | Formato |
|---|---|---|
| `guias/` | 11 documentos de guías de Git (comandos, ramas, commits, SSH, tags, PRs, conflictos, seguridad, stash, aliases) | `.md` y `.txt` |
| `matrices/` | Recetario de situaciones comunes de Git | `.md` |
| `troubleshooting/` | Errores de terminal y sus soluciones | `.csv` |

Total: 13 archivos.

### Índice de documentos

**Guías (`guias/`)**

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

**Matrices (`matrices/`)**

| Archivo | Tema |
|---|---|
| `04_recetario_situaciones_git.md` | Recetario de 14 situaciones comunes con comandos exactos |

**Troubleshooting (`troubleshooting/`)**

| Archivo | Tema |
|---|---|
| `05_errores_terminales_y_soluciones.csv` | 15 errores comunes con causa, solución y advertencia |

---

## Requisitos

- Databricks con Unity Catalog habilitado.
- Un volumen `dataset` en el schema `git-assistnat-agent` (catálogo `workspace`).
- Acceso a los endpoints de Foundation Model:
  - `databricks-gpt-oss-20b` (conversión de CSV a markdown),
  - `databricks-gte-large-en` (embeddings),
  - `databricks-gpt-oss-120b` (agente).
- Permisos para crear tablas, volúmenes, funciones UC, índices de Vector Search y modelos en Unity Catalog.

---

## Cómo ejecutar

1. **`Includes/Lab_Setup.ipynb`**: crea/usa el schema `git-assistnat-agent` y los volúmenes `_cache` y `_checkpoint`.
2. **Fase 1 — RAG** (en orden):
   1. `1.1A- Data Prep (Bronze).py` → `bronze_docs_raw`
   2. `1.1B- Data Prep (Silver).py` → `silver_docs_parsed`
   3. `1.1C- Data Prep (Gold).py` → `gold_docs_chunked`
   4. `1.2- Creating Vector Search.py` → `git_vs_index`
3. **Fase 2 — AI Agents** (requiere el índice ya creado):
   1. `2.3- Agents with UC Functions.py` → funciones UC
   2. `2.4- driver (git_agent).py` → agente, logging, registro y despliegue
4. **Fase 3 — Evaluación** (pendiente): `3.1- Evaluation Techniques.py`.

---

## Artefactos generados

| Artefacto | Tipo | Descripción |
|---|---|---|
| `bronze_docs_raw` | Tabla Delta | Documentos binarios ingeridos + `ingestion_time` |
| `silver_docs_parsed` | Tabla Delta | Texto plano (`path`, `plain_text`) |
| `gold_docs_chunked` | Tabla Delta | Chunks (`path`, `chunk`, `id`) |
| `git_vs_index` | Índice Vector Search | Búsqueda semántica/full-text/híbrida sobre los chunks |
| `search_git_docs` | Función UC | Busca chunks de la documentación Git |
| `get_current_user` | Función UC | Devuelve el usuario de la sesión |
| `build_reference` | Función UC (Python) | Arma una referencia corta de un chunk |
| `git_agent` | Modelo UC | Agente tool-calling registrado y desplegable |

---

## Estado del proyecto

| Fase | Estado |
|---|---|
| 1 — RAG (Bronze → Silver → Gold → Vector Search) | Completada |
| 2 — AI Agents (Funciones UC + agente tool-calling) | Completada |
| 3 — Evaluación | Pendiente |

El detalle de decisiones, problemas y evidencias está en [`BITACORA.md`](BITACORA.md).

---

## Notas

- El schema `git-assistnat-agent` contiene guiones, por lo que todo SQL usa backticks:
  ```sql
  ALTER TABLE `workspace`.`git-assistnat-agent`.gold_docs_chunked
  SET TBLPROPERTIES (delta.enableChangeDataFeed = true)
  ```
- Los documentos `.md` y `.txt` se decodifican directamente a UTF-8. Solo el `.csv` se convierte a tabla markdown con `ai_query`.
- El chunking usa `chunk_size = 1500` y `chunk_overlap = 150`, respetando los separadores `== page ==`.
